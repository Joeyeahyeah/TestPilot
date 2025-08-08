# 避免循环依赖
from __future__ import annotations
from http.client import responses
from typing import Dict, Any, Optional
import requests
import logging

from src.api.clients.auth_client import AuthClient
from src.api.api_client import APIClient

"""
用户管理相关接口（增删改查）的业务封装
create_user(), get_user(), update_user()
"""


class UserClient(APIClient):
    # 用户管理端点
    USER_ENDPOINT = "users"

    def __init__(self, base_url: str, auth_client: AuthClient):
        super().__init__(base_url)
        self.logger = logging.getLogger(__name__)
        self.auth_client = auth_client
        # 复用已登录的auth_client的session
        self.session = auth_client.session

    def create_user(self, user_data: dict) -> dict:
        """创建用户，无需认证"""
        return self.post(self.USER_ENDPOINT, json=user_data)

    def get_user(self, user_id: str) -> dict:
        """获取用户信息，需要认证"""
        if not self.auth_client.check_health():
            return {
                "status_code": 401,
                "data": None,
                "error": "用户认证失败，请重新登录"
            }
        return self.get(f"{self.USER_ENDPOINT}/{user_id}")

    def update_user(self, user_id: str, update_data: dict) -> dict:
        """更新用户信息，需要认证"""
        return self.put(f"{self.USER_ENDPOINT}/{user_id}", json=update_data)
