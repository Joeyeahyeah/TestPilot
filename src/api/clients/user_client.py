from ..api_client import APIClient
from .auth_client import AuthClient  # 需要依赖认证
import requests
"""
用户管理相关接口（增删改查）的业务封装
create_user(), get_user(), update_user()
"""
class UserClient(APIClient):
    # 用户管理端点
    USER_ENDPOINT = "/users"

    def __init__(self, base_url: str, auth_client: AuthClient):
        super().__init__(base_url)
        # 复用已登录的auth_client的session
        self.session = auth_client.session

    def create_user(self, user_data: dict) -> dict:
        return self.post(self.USER_ENDPOINT, json=user_data)

    def get_user(self, user_id: str) -> dict:
        return self.get(f"{self.USER_ENDPOINT}/{user_id}")

    def update_user(self, user_id: str, update_data: dict) -> dict:
        return self.put(f"{self.USER_ENDPOINT}/{user_id}", json=update_data)