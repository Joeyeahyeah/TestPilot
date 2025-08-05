from http.client import responses
from typing import Dict, Any, TypedDict
from ..api_client import APIClient
import requests
import logging
"""
认证相关接口（登录/登出）的业务封装
login(), logout(), refresh_token()
"""

class LoginSuccessResponse(TypedDict):
    token: str
    expires_in: int


class AuthClient(APIClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
        # 认证专用端点
        self.LOGIN_ENDPOINT = "/auth/login"
        self.LOGOUT_ENDPOINT = "/auth/logout"
        self.logger = logging.getLogger(__name__)

    def _handle_error(self, e: requests.HTTPError) -> Dict[str, Any]:
        """统一错误处理"""
        self.logger.error(f"API Error: {e.response.status_code} {e.response.text}")
        return {
            "status_code": e.response.status_code,
            "error": responses.get(e.response.status_code, "Unknown Error"),
            "detail": e.response.json().get("detail","")
        }

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        标准化登录接口
        :return: {
            "status_code": int,             # 实际HTTP状态码
            "token": Optional[str], # 成功时返回
            "error": Optional[str]  # 失败时返回
            "data": LoginSuccessResponse,   # 成功时返回
            "error": str                    # 失败时返回
        }
        返回包含token的响应
        """
        self.logger.info(f"Login attempt: {username}")
        try:
            resp = self.post(
                self.LOGIN_ENDPOINT,
                json={"username": username, "password": password}
            )
            token = resp["access_token"]

            # 关键：存储token到session
            self.session.headers["Authorization"] = f"Bearer {token}"

            return {
                "status_code": resp.status_code,
                "token": token,
                "expires_in": resp["expires_in"]

            }
        except requests.HTTPError as e:
            return self._handle_error(e)
            # return {
            #     "status_code": e.resp.status_code,
            #     "error": e.resp.json().get("message", "Login failed")
            # }

    def logout(self) -> dict[str, Any]:
        """
        清除登录状态
        """
        try:
            resp = self.post(self.LOGOUT_ENDPOINT)
            self.session.headers.pop("Authorization", None)
            # self.post(self.LOGOUT_ENDPOINT)
            return {"status_code": resp.status_code}
        except requests.HTTPError as e:
            return self._handle_error(e)
            # return {
            #     "status_code": e.response.status_code,
            #     "error": str(e)
            # }
