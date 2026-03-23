#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
# from __future__ import unicode_literals


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import logging
import pathlib
import time
import hmac
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

import aiofiles
import pymysql
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, conint, EmailStr, Field, validator
from dataclasses import dataclass, field


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 数据模型定义
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

@dataclass
class UserInfo:
    """数据库用户信息（内部使用）"""
    host: str = field(default=None)
    port: int = field(default=0)
    user: str = field(default=None)
    password: str = field(default="")
    database: str = field(default=None)
    charset: str = field(default='utf8mb4')
    cursorclass: pymysql.cursors = field(default=pymysql.cursors.DictCursor)


class UserModel(BaseModel):
    """用户模型（API 传输使用）"""
    name: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=8, description="密码，至少8位")
    phone: str = Field(default="", description="手机号")
    company: str = Field(default="", description="公司名称")
    is_active: conint(ge=0, le=1) = 1

    @validator('password')
    def password_strength(cls, v):
        """验证密码强度"""
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含数字")
        if not any(c.isalpha() for c in v):
            raise ValueError("密码必须包含字母")
        return v


class LoginModel(BaseModel):
    """登录模型"""
    email: EmailStr
    password: str


class TokenModel(BaseModel):
    """Token 模型"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 数据库操作类
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++#

class MySQLHandler:
    """
    MySQL 数据库操作类

    封装了常见的数据库操作，如连接、查询、插入、更新、删除等。
    """

    def __init__(self, user_info: UserInfo = None):
        """
        初始化 MySQLHandler 类。

        Args:
            user_info: 用户信息对象，包含数据库连接所需的参数。
        """
        self._user_info = user_info
        self._connection: Optional[pymysql.Connection] = None
        if self._user_info:
            self.connection = user_info

    @property
    def connection(self) -> Optional[pymysql.Connection]:
        """
        获取数据库连接对象。

        Returns:
            数据库连接对象，如果未连接则返回 None。
        """
        return self._connection

    @connection.setter
    def connection(self, user_info: UserInfo):
        """
        设置数据库连接。

        Args:
            user_info: 用户信息对象，包含数据库连接所需的参数。
        """
        self.close_connection()
        self._connection = pymysql.connect(
            host=user_info.host,
            port=user_info.port,
            user=user_info.user,
            password=user_info.password,
            database=user_info.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("数据库连接已开启")
        self._user_info = user_info

    @connection.deleter
    def connection(self):
        """删除数据库连接，关闭连接。"""
        self.close_connection()

    def close_connection(self):
        """关闭数据库连接。"""
        if self._connection:
            self._connection.close()
            logger.info("数据库连接已关闭")

    def _execute_sql(self, sql: str, args: Optional[Tuple] = None) -> str:
        """
        执行 SQL 语句（如 INSERT, UPDATE, DELETE）。

        Args:
            sql: 要执行的 SQL 语句。
            args: SQL 语句中的参数。

        Returns:
            执行结果信息。
        """
        if not self._connection:
            raise pymysql.MySQLError("数据库未连接!")
        with self._connection.cursor() as cursor:
            cursor.execute(sql, args)
            self._connection.commit()
        return "执行成功"

    def _query_sql(self, sql: str, args: Optional[Tuple] = None, get_all: bool = True) -> List[Dict[str, Any]]:
        """
        执行 SQL 查询语句（如 SELECT）。

        Args:
            sql: 要执行的 SQL 查询语句。
            args: SQL 语句中的参数。
            get_all: 是否获取所有结果，如果为 False 则只获取第一条结果。

        Returns:
            查询结果列表（字典形式）。
        """
        if not self._connection:
            raise pymysql.MySQLError("数据库未连接!")
        with self._connection.cursor() as cursor:
            cursor.execute(sql, args)
            result = cursor.fetchall() if get_all else cursor.fetchone()
        return result


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 服务层
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++#

class UserService:
    """
    用户服务类

    提供用户的增删改查操作。
    """

    def __init__(self, db_handler: MySQLHandler):
        """
        初始化用户服务。

        Args:
            db_handler: 数据库处理器
        """
        self._db = db_handler
        self._SECRET_KEY = "your-secret-key"
        self._ALGORITHM = "HS256"
        self._ACCESS_TOKEN_EXPIRE_DAYS = 7
        logger.info("用户服务初始化完成")

    @property
    def db(self):
        """获取数据库处理器"""
        return self._db

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        根据邮箱获取用户信息。

        Args:
            email: 用户邮箱

        Returns:
            用户信息字典，如果不存在返回 None
        """
        try:
            sql = "SELECT * FROM users WHERE email = %s"
            result = self.db._query_sql(sql, args=(email,), get_all=False)
            logger.info(f"成功获取用户: {email}")
            return result
        except Exception as e:
            logger.error(f"获取用户失败: {e}", exc_info=True)
            return None

    def create_user(self, user_model: UserModel) -> Tuple[bool, str]:
        """
        创建新用户。

        Args:
            user_model: 用户模型

        Returns:
            (成功状态, 结果消息)
        """
        try:
            # 检查邮箱是否已存在
            existing = self.get_user_by_email(user_model.email)
            if existing:
                return False, "邮箱已被注册"

            # 创建用户
            sql = """
            INSERT INTO users (name, email, password, phone, company, is_active, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            args = (
                user_model.name,
                user_model.email,
                user_model.password,
                user_model.phone,
                user_model.company,
                user_model.is_active,
                datetime.now()
            )
            self.db._execute_sql(sql, args)
            logger.info(f"成功创建用户: {user_model.email}")
            return True, "用户创建成功"

        except Exception as e:
            logger.error(f"创建用户失败: {e}", exc_info=True)
            return False, f"创建用户失败: {str(e)}"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码（简化版，实际应使用 bcrypt）。

        Args:
            plain_password: 明文密码
            hashed_password: 哈希密码

        Returns:
            验证结果
        """
        # 实际应用中应使用 bcrypt 或类似库
        return plain_password == hashed_password

    def authenticate_user(self, login_model: LoginModel) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        验证用户身份。

        Args:
            login_model: 登录模型

        Returns:
            (验证结果, 用户信息)
        """
        user = self.get_user_by_email(login_model.email)
        if not user:
            return False, None

        if not self.verify_password(login_model.password, user['password']):
            return False, None

        return True, user

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """
        创建 JWT 访问令牌。

        Args:
            data: 要编码的数据
            expires_delta: 过期时间增量

        Returns:
            JWT 令牌
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self._ACCESS_TOKEN_EXPIRE_DAYS)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._SECRET_KEY, algorithm=self._ALGORITHM)
        return encoded_jwt

    def login(self, login_model: LoginModel) -> Tuple[bool, str]:
        """
        用户登录。

        Args:
            login_model: 登录模型

        Returns:
            (成功状态, Token或错误消息)
        """
        try:
            success, user = self.authenticate_user(login_model)
            if not success or not user:
                return False, "邮箱或密码不正确"

            if not user.get('is_active'):
                return False, "账户已被禁用"

            # 生成 Token
            access_token = self.create_access_token(data={"sub": user['email'], "user_id": user['id']})
            logger.info(f"用户登录成功: {login_model.email}")
            return True, access_token

        except Exception as e:
            logger.error(f"登录失败: {e}", exc_info=True)
            return False, f"登录失败: {str(e)}"


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 文件操作工具
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++#

class FileHandler:
    """文件处理类"""

    @staticmethod
    async def upload_file_init(base_dir: pathlib.Path, asset_name: str, asset_version: str, flag: str) -> pathlib.Path:
        """
        初始化文件上传。

        Args:
            base_dir: 基础目录
            asset_name: 资产名称
            asset_version: 资产版本
            flag: 文件扩展名

        Returns:
            最终文件路径
        """
        fin_file = base_dir / f"{asset_name} - {asset_version}.{flag}"
        if fin_file.exists():
            fin_file.unlink()
        return fin_file

    @staticmethod
    async def _async_copyfileobj(fsrc, fdst, length: int = 1024 * 1024 * 5):
        """
        异步复制文件对象的内容。

        Args:
            fsrc: 源文件
            fdst: 目标文件
            length: 每次复制的字节数
        """
        while True:
            buf = await fsrc.read(length)
            if not buf:
                break
            await fdst.write(buf)

    @staticmethod
    async def merge_chunks(base_dir: pathlib.Path, asset_name: str, asset_version: str,
                         total_chunks: int, flag: str) -> pathlib.Path:
        """
        按块合并文件。

        Args:
            base_dir: 基础目录
            asset_name: 资产名称
            asset_version: 资产版本
            total_chunks: 总块数
            flag: 文件扩展名

        Returns:
            合并后的文件路径
        """
        fin_file = base_dir / f"{asset_name} - {asset_version}.{flag}"
        logger.info(f"开始合并文件: {fin_file}")

        try:
            async with aiofiles.open(fin_file, "wb") as final_file:
                for i in range(total_chunks):
                    part_file_path = base_dir / f"{asset_name} - {asset_version}.part{i}"
                    async with aiofiles.open(part_file_path, "rb") as part_file:
                        await FileHandler._async_copyfileobj(part_file, final_file)
        except Exception as e:
            logger.error(f"文件合并失败: {e}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"文件保存出错了：{e}")
        else:
            # 删除分块文件
            for i in range(total_chunks):
                part_file_path = base_dir / f"{asset_name} - {asset_version}.part{i}"
                if part_file_path.exists():
                    part_file_path.unlink()

            logger.info(f"文件合并成功: {fin_file}")
            return fin_file

    @staticmethod
    def calculate_file_hash(file_path: pathlib.Path) -> str:
        """
        计算文件 SHA256 哈希值。

        Args:
            file_path: 文件路径

        Returns:
            哈希值
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 签名验证工具
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++#

class SignatureHandler:
    """签名处理类"""

    def __init__(self, secret_key: str):
        """
        初始化签名处理器。

        Args:
            secret_key: 密钥
        """
        self._secret_key = secret_key

    def generate_signed_url(self, path: str) -> str:
        """
        生成签名 URL。

        Args:
            path: 路径

        Returns:
            签名 URL
        """
        timestamp = int(time.time())
        signature = hmac.new(
            self._secret_key.encode(),
            f"{path}{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()
        return f"{path}?timestamp={timestamp}&signature={signature}"

    def verify_signature(self, url: str, timestamp: int, signature: str) -> bool:
        """
        验证签名是否合法。

        Args:
            url: URL
            timestamp: 时间戳
            signature: 签名

        Returns:
            验证结果
        """
        expected_signature = hmac.new(
            self._secret_key.encode(),
            f"{url}{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 单例日志类
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++#

class MyLogger:
    """单例日志类"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.__logger = None
            self.__handler = None
            self.__log_file = ''
            self.initialized = True

    @property
    def logfile(self) -> str:
        """获取日志文件路径"""
        return self.__log_file

    @logfile.setter
    def logfile(self, val: str):
        """设置日志文件路径"""
        folder = pathlib.Path(val).parent
        try:
            folder.mkdir(exist_ok=True, parents=True)
        except Exception as e:
            raise ValueError(f"创建日志目录失败: {folder}") from e
        self.__log_file = str(val)

    @property
    def logger(self):
        """获取日志对象"""
        return self.__logger

    @logger.setter
    def logger(self, val_and_level: tuple = ("default_logger", logging.INFO)):
        """设置日志对象"""
        val, level = val_and_level
        self.__logger = logging.getLogger(val)
        self.__logger.setLevel(level)

    def close(self):
        """关闭日志"""
        if self.__logger:
            for handler in self.__logger.handlers:
                try:
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    pass
                self.__logger.removeHandler(handler)
            self.__logger.disabled = True

    def __del__(self):
        """析构函数"""
        self.close()


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 主程序
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++#

if __name__ == "__main__":
    # 示例：使用日志
    logger.info("Web Backend 示例启动")

    # 示例：使用单例日志
    my_logger = MyLogger()
    my_logger.logger = ("my_app", logging.INFO)
    my_logger.logfile = "logs/app.log"

    logger.info("示例代码运行完成")
