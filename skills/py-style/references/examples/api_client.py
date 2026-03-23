"""
API 客户端模块

提供与 RESTful API 交互的客户端功能，支持请求重试、认证和错误处理。
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import requests


logger = logging.getLogger(__name__)


class HTTPMethod(Enum):
    """HTTP 方法枚举"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class APIResponse:
    """API 响应数据类

    Attributes:
        status_code: HTTP 状态码
        data: 响应数据
        headers: 响应头
        success: 是否成功
    """

    status_code: int
    data: Optional[Dict[str, Any]]
    headers: Dict[str, str]
    success: bool

    @property
    def is_client_error(self) -> bool:
        """是否为客户端错误 (4xx)"""
        return 400 <= self.status_code < 500

    @property
    def is_server_error(self) -> bool:
        """是否为服务器错误 (5xx)"""
        return 500 <= self.status_code < 600


class APIError(Exception):
    """API 错误基类"""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(APIError):
    """认证错误"""

    pass


class RateLimitError(APIError):
    """速率限制错误"""

    pass


class APIClient:
    """
    RESTful API 客户端

    提供统一的 API 请求接口，支持认证、重试和错误处理。

    Attributes:
        base_url: API 基础 URL
        api_key: API 密钥
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
        session: requests.Session 实例

    Examples:
        >>> client = APIClient("https://api.example.com", api_key="secret")
        >>> response = client.get("/users/123")
        >>> print(response.data)
    """

    DEFAULT_TIMEOUT = 30
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_RETRY_DELAY = 1.0

    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES
    ):
        """
        初始化 API 客户端

        Args:
            base_url: API 基础 URL
            api_key: API 密钥（可选）
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()

        # 设置默认请求头
        self._setup_default_headers()

        logger.info(f"APIClient initialized for {self.base_url}")

    def _setup_default_headers(self) -> None:
        """设置默认请求头"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        """
        构建完整的 URL

        Args:
            endpoint: API 端点

        Returns:
            完整的 URL
        """
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}"

    def _handle_response(self, response: requests.Response) -> APIResponse:
        """
        处理 API 响应

        Args:
            response: requests.Response 对象

        Returns:
            APIResponse 对象

        Raises:
            AuthenticationError: 认证失败
            RateLimitError: 速率限制
            APIError: API 错误
        """
        status_code = response.status_code
        headers = dict(response.headers)

        try:
            data = response.json() if response.content else None
        except json.JSONDecodeError:
            logger.warning("Failed to parse response as JSON")
            data = None

        # 处理错误状态码
        if status_code == 401:
            raise AuthenticationError("Authentication failed", status_code)
        elif status_code == 429:
            raise RateLimitError("Rate limit exceeded", status_code)
        elif status_code >= 400:
            error_message = data.get("error", "API request failed") if data else "API request failed"
            raise APIError(error_message, status_code)

        success = 200 <= status_code < 300

        return APIResponse(
            status_code=status_code,
            data=data,
            headers=headers,
            success=success
        )

    def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        retry: bool = True
    ) -> APIResponse:
        """
        发送 API 请求

        Args:
            method: HTTP 方法
            endpoint: API 端点
            params: 查询参数
            data: 请求体数据
            retry: 是否启用重试

        Returns:
            APIResponse 对象

        Raises:
            APIError: 请求失败且重试次数用尽
        """
        url = self._build_url(endpoint)
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                logger.debug(
                    f"Request: {method.value} {url} "
                    f"(Attempt {attempt + 1}/{self.max_retries + 1})"
                )

                response = self.session.request(
                    method=method.value,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout
                )

                return self._handle_response(response)

            except requests.Timeout:
                last_exception = APIError("Request timeout")
                logger.warning(f"Request timeout: {url}")

            except requests.ConnectionError as e:
                last_exception = APIError(f"Connection error: {str(e)}")
                logger.warning(f"Connection error: {url}")

            except (AuthenticationError, RateLimitError) as e:
                # 这些错误不需要重试
                raise

            except Exception as e:
                last_exception = APIError(f"Unexpected error: {str(e)}")
                logger.error(f"Unexpected error: {str(e)}")

            # 如果不是最后一次尝试，等待后重试
            if attempt < self.max_retries and retry:
                logger.debug(f"Retrying in {self.DEFAULT_RETRY_DELAY}s...")
                import time
                time.sleep(self.DEFAULT_RETRY_DELAY)

        # 所有重试都失败
        if last_exception:
            raise last_exception

        raise APIError("Request failed")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        发送 GET 请求

        Args:
            endpoint: API 端点
            params: 查询参数

        Returns:
            APIResponse 对象

        Examples:
            >>> client = APIClient("https://api.example.com")
            >>> response = client.get("/users", params={"page": 1})
            >>> print(response.data)
        """
        return self.request(HTTPMethod.GET, endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Dict[str, Any]
    ) -> APIResponse:
        """
        发送 POST 请求

        Args:
            endpoint: API 端点
            data: 请求数据

        Returns:
            APIResponse 对象

        Examples:
            >>> client = APIClient("https://api.example.com")
            >>> response = client.post("/users", data={"name": "John"})
            >>> print(response.data)
        """
        return self.request(HTTPMethod.POST, endpoint, data=data)

    def put(
        self,
        endpoint: str,
        data: Dict[str, Any]
    ) -> APIResponse:
        """
        发送 PUT 请求

        Args:
            endpoint: API 端点
            data: 请求数据

        Returns:
            APIResponse 对象
        """
        return self.request(HTTPMethod.PUT, endpoint, data=data)

    def patch(
        self,
        endpoint: str,
        data: Dict[str, Any]
    ) -> APIResponse:
        """
        发送 PATCH 请求

        Args:
            endpoint: API 端点
            data: 请求数据

        Returns:
            APIResponse 对象
        """
        return self.request(HTTPMethod.PATCH, endpoint, data=data)

    def delete(self, endpoint: str) -> APIResponse:
        """
        发送 DELETE 请求

        Args:
            endpoint: API 端点

        Returns:
            APIResponse 对象
        """
        return self.request(HTTPMethod.DELETE, endpoint)

    def close(self) -> None:
        """关闭客户端"""
        self.session.close()
        logger.info("APIClient closed")

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
        return False


# 使用示例
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 使用上下文管理器
    with APIClient("https://jsonplaceholder.typicode.com") as client:
        try:
            # GET 请求
            response = client.get("/posts/1")
            print(f"GET /posts/1: {response.data}")

            # POST 请求
            new_post = {
                "title": "Test Post",
                "body": "This is a test post",
                "userId": 1
            }
            response = client.post("/posts", data=new_post)
            print(f"POST /posts: {response.data}")

            # GET 请求带参数
            response = client.get("/posts", params={"userId": 1})
            print(f"GET /posts?userId=1: Found {len(response.data)} posts")

        except APIError as e:
            logger.error(f"API Error: {e.message}")
