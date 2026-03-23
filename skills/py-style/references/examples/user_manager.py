"""
用户管理模块

本模块提供用户管理的核心功能，包括用户创建、查询、更新和删除操作。

示例:
    >>> manager = UserManager()
    >>> user = manager.create_user("john", "john@example.com")
    >>> print(user.id)
    123
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass


logger = logging.getLogger(__name__)


@dataclass
class User:
    """用户数据类

    Attributes:
        id: 用户 ID
        username: 用户名
        email: 邮箱地址
        is_active: 是否激活
        created_at: 创建时间
    """

    id: int
    username: str
    email: str
    is_active: bool = True
    created_at: Optional[datetime] = None


class UserNotFoundError(Exception):
    """用户未找到异常"""

    pass


class InvalidEmailError(Exception):
    """无效邮箱异常"""

    pass


class UserManager:
    """
    用户管理器

    负责用户的增删改查操作，提供统一的用户管理接口。

    Attributes:
        _users: 用户存储字典
        _next_id: 下一个可用的用户 ID

    Examples:
        >>> manager = UserManager()
        >>> user = manager.create_user("john", "john@example.com")
        >>> manager.delete_user(user.id)
    """

    def __init__(self):
        """初始化用户管理器"""
        self._users: Dict[int, User] = {}
        self._next_id: int = 1
        logger.info("UserManager initialized")

    def create_user(self, username: str, email: str) -> User:
        """
        创建新用户

        Args:
            username: 用户名，长度 3-20 个字符
            email: 邮箱地址，必须符合邮箱格式

        Returns:
            创建的用户对象

        Raises:
            ValueError: 当用户名长度不符合要求时
            InvalidEmailError: 当邮箱格式无效时

        Examples:
            >>> manager = UserManager()
            >>> user = manager.create_user("john", "john@example.com")
            >>> print(user.username)
            'john'
        """
        # 验证用户名
        if not (3 <= len(username) <= 20):
            raise ValueError("Username must be between 3 and 20 characters")

        # 验证邮箱
        if not self._is_valid_email(email):
            raise InvalidEmailError(f"Invalid email format: {email}")

        # 创建用户
        user = User(
            id=self._next_id,
            username=username,
            email=email,
            created_at=datetime.now()
        )

        self._users[user.id] = user
        self._next_id += 1

        logger.info(f"Created user: {user.username} (ID: {user.id})")
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        """
        获取用户信息

        Args:
            user_id: 用户 ID

        Returns:
            用户对象，如果用户不存在则返回 None

        Examples:
            >>> manager = UserManager()
            >>> user = manager.create_user("john", "john@example.com")
            >>> found_user = manager.get_user(user.id)
            >>> found_user is not None
            True
        """
        user = self._users.get(user_id)
        if user:
            logger.debug(f"Retrieved user: {user.username}")
        else:
            logger.debug(f"User not found: ID {user_id}")
        return user

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱获取用户

        Args:
            email: 邮箱地址

        Returns:
            用户对象，如果用户不存在则返回 None
        """
        for user in self._users.values():
            if user.email == email:
                logger.debug(f"Retrieved user by email: {user.username}")
                return user

        logger.debug(f"User not found with email: {email}")
        return None

    def get_all_users(self, include_deleted: bool = False) -> List[User]:
        """
        获取所有用户

        Args:
            include_deleted: 是否包含已删除的用户，默认为 False

        Returns:
            用户列表
        """
        users = list(self._users.values())

        if not include_deleted:
            users = [user for user in users if user.is_active]

        logger.info(f"Retrieved {len(users)} users")
        return users

    def update_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None
    ) -> User:
        """
        更新用户信息

        Args:
            user_id: 用户 ID
            username: 新的用户名（可选）
            email: 新的邮箱地址（可选）

        Returns:
            更新后的用户对象

        Raises:
            UserNotFoundError: 当用户不存在时
            InvalidEmailError: 当邮箱格式无效时

        Examples:
            >>> manager = UserManager()
            >>> user = manager.create_user("john", "john@example.com")
            >>> updated = manager.update_user(user.id, username="johnny")
            >>> updated.username
            'johnny'
        """
        user = self._users.get(user_id)

        if user is None:
            raise UserNotFoundError(f"User not found: ID {user_id}")

        # 更新用户名
        if username is not None:
            if not (3 <= len(username) <= 20):
                raise ValueError("Username must be between 3 and 20 characters")
            user.username = username

        # 更新邮箱
        if email is not None:
            if not self._is_valid_email(email):
                raise InvalidEmailError(f"Invalid email format: {email}")
            user.email = email

        logger.info(f"Updated user: {user.username} (ID: {user.id})")
        return user

    def delete_user(self, user_id: int, permanent: bool = False) -> bool:
        """
        删除用户

        Args:
            user_id: 用户 ID
            permanent: 是否永久删除，默认为 False（软删除）

        Returns:
            是否删除成功

        Raises:
            UserNotFoundError: 当用户不存在时

        Examples:
            >>> manager = UserManager()
            >>> user = manager.create_user("john", "john@example.com")
            >>> manager.delete_user(user.id)
            True
            >>> manager.get_user(user.id).is_active
            False
        """
        user = self._users.get(user_id)

        if user is None:
            raise UserNotFoundError(f"User not found: ID {user_id}")

        if permanent:
            # 永久删除
            del self._users[user_id]
            logger.info(f"Permanently deleted user: {user.username} (ID: {user_id})")
        else:
            # 软删除
            user.is_active = False
            logger.info(f"Soft deleted user: {user.username} (ID: {user_id})")

        return True

    def search_users(
        self,
        keyword: str,
        field: str = "username"
    ) -> List[User]:
        """
        搜索用户

        Args:
            keyword: 搜索关键词
            field: 搜索字段 ('username', 'email')

        Returns:
            匹配的用户列表

        Raises:
            ValueError: 当字段名称无效时
        """
        if field not in ["username", "email"]:
            raise ValueError(f"Invalid field: {field}")

        keyword_lower = keyword.lower()

        matching_users = [
            user for user in self._users.values()
            if getattr(user, field, "").lower().startswith(keyword_lower)
        ]

        logger.info(f"Found {len(matching_users)} users matching '{keyword}' in {field}")
        return matching_users

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        验证邮箱格式

        Args:
            email: 邮箱地址

        Returns:
            是否为有效的邮箱格式
        """
        if not email:
            return False

        # 简单的邮箱验证
        if "@" not in email or "." not in email:
            return False

        local_part, domain = email.split("@", 1)

        if len(local_part) == 0 or len(domain) == 0:
            return False

        if "." not in domain:
            return False

        return True

    def get_user_count(self, include_inactive: bool = False) -> int:
        """
        获取用户数量

        Args:
            include_inactive: 是否包含未激活的用户，默认为 False

        Returns:
            用户数量
        """
        if include_inactive:
            count = len(self._users)
        else:
            count = len([u for u in self._users.values() if u.is_active])

        logger.debug(f"User count: {count}")
        return count

    def __repr__(self) -> str:
        """字符串表示"""
        active_count = len([u for u in self._users.values() if u.is_active])
        return f"UserManager(users={active_count}, total={len(self._users)})"


if __name__ == "__main__":
    # 示例用法
    logging.basicConfig(level=logging.INFO)

    manager = UserManager()

    # 创建用户
    user1 = manager.create_user("john", "john@example.com")
    user2 = manager.create_user("jane", "jane@example.com")

    print(f"Created users: {user1.username}, {user2.username}")

    # 获取用户
    found_user = manager.get_user(user1.id)
    print(f"Found user: {found_user.username}")

    # 搜索用户
    results = manager.search_users("jo", "username")
    print(f"Search results: {[u.username for u in results]}")

    # 更新用户
    updated_user = manager.update_user(user1.id, username="johnny")
    print(f"Updated user: {updated_user.username}")

    # 获取所有用户
    all_users = manager.get_all_users()
    print(f"All users: {[u.username for u in all_users]}")
