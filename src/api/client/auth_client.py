from http.client import responses
from typing import Dict, Any
from src.api.api_client import APIClient
import requests


class LoginSuccessResponse(TypeError):
    token: str
    expires_in: int


class AuthClient(APIClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        self.login_endpoint = "/auth/login"
        self.logout_endpoint = "/auth/logout"

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        标准化登录接口
        :return: {
            "status_code": int,
            "data": LoginSuccessResponse,  # 成功时
            "error": str                  # 失败时
        }
        """
        # try:
        #     return self.post("/auth/login", json={"username": username, "password": password})
        # except requests.HTTPError as e:
        #     return {"error": str(e), "status_code": e.response.status_code}
        try:
            # response = self.post("/auth/login", json={"username": username, "password": password})
            response = self.post(
                self.login_endpoint,
                json={"username": username, "password": password}
            )
            return {
                # "success": True,
                # "data": response,
                "status_code": 200,
                "data": {
                    "token": response["access_token"],
                    "expires_in": response["expires_in"]
                }
            }
        except requests.HTTPError as e:
            return {
                # "success": False,
                # "error": str(e),
                "status_code": e.response.status_code,
                "error": e.response.json().get("message", "Login failed")
            }

    def logout(self) -> dict[str, Any]:
        """标准化登出接口"""
        try:
            # response = self.post("/auth/logout")
            self.post(self.logout_endpoint)
            return {"status_code": 200}
            # return self.post("/auth/logout").get("success", False)
        except requests.HTTPError as e:
            return {
                # "success": False,
                "error": str(e),
                "status_code": e.response.status_code
            }
