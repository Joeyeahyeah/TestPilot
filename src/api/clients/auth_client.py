# from http.client import responses
from typing import Dict, Any, TypedDict
from src.api.api_client import APIClient
# import requests
import logging

"""
认证相关接口（登录/登出）的业务封装
login(), logout(), refresh_token()
"""


class LoginSuccessResponse(TypedDict):
    token: str
    expires_in: int


class AuthClient(APIClient):
    # 不再需要专门的登录方法，因为使用API key认证
    def check_health(self) -> bool:
        """检查API是否可用"""
        try:
            # 直接使用基础的_get方法，避免认证干扰
            resp = self.get("users/2")  # ReqRes的这个端点不需要认证
            # 明确检查响应状态码
            if resp.get("status_code") == 200:
                return True
            self.logger.warning(f"Health check returned status code: {resp.get('status_code')}")
            return False
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False
        # 原代码
        # try:
        #     response = self.get("users/1")
        #     return 200 <= response.get("status_code", 0) < 300
        # except Exception as e:
        #     self.logger.error(f"Check health failed: {str(e)}")
        #     return False



    def __init__(self, base_url: str):
        super().__init__(base_url)
        # 认证端点
        # self.LOGIN_ENDPOINT = "/auth/login"
        # self.LOGOUT_ENDPOINT = "/auth/logout"

        # ReqRes 认证端点
        self.LOGIN_ENDPOINT = "login"
        self.LOGOUT_ENDPOINT = "logout"
        self.logger = logging.getLogger(__name__)

    # def _handle_error(self, e: requests.HTTPError) -> Dict[str, Any]:
    #     """统一错误处理"""
    #     self.logger.error(f"API Error: {e.response.status_code} {e.response.text}")
    #     return {
    #         "status_code": e.response.status_code,
    #         "error": responses.get(e.response.status_code, "Unknown Error"),
    #         "detail": e.response.json().get("detail","")
    #     }

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        标准化登录接口
        :return: {
            "status_code": int,       # 状态码（必选）
            "data": Optional[dict],   # 成功时的业务数据（可选，失败为None）
            "error": Optional[str],   # 失败时的错误信息（可选，成功为None）
            "headers": Optional[dict] # 响应头（可选）
        }
        返回包含token的响应
        """
        try:
            self.logger.info(f"Login attempt: {username}")
            response = self.post(
                self.LOGIN_ENDPOINT,
                json={"email": username, "password": password}
            )
            # if response["status_code"] == 200 and not response["error"]:
            if response["status_code"] == 200:
                token = response["data"].get("token")
                # token = response["data"].get("token") or response["data"].get("id")  # Reqres
                # 关键：存储token到session
                if token:
                    self.session.headers["Authorization"] = f"Bearer {token}"
                    return {
                        "status_code": response["status_code"],
                        "data": {"token": token},  # 统一嵌套在 data 中
                        "error": None
                    }
            # 错误处理
            error_msg = response["error"]["message"] if response["error"] else "Unknown Error"
            self.logger.error(f"Login failed: {error_msg}")
            return {
                "status_code": response["status_code"],
                "data": None,
                "error": error_msg
            }
        except Exception as e:
            self.logger.error(f"Login failed: {str(e)}")
            return {
                "status_code": 500,
                "data": None,
                "error": str(e)
            }
        # 原代码
        # try:
        #     response = self.post(
        #         self.LOGIN_ENDPOINT,
        #         json={"email": username, "password": password}
        #     )
        #     # token = response["data"]["token"]
        #     token = response["data"].get("token") or response["data"].get("id") # Reqres
        #     # 关键：存储token到session
        #     self.session.headers["Authorization"] = f"Bearer {token}"
        #
        #     return {
        #         "status_code": response["status_code"],
        #         "data": {"token": token},  # 统一嵌套在 data 中
        #         "error": None
        #     }
        # except KeyError as e:
        #     # 添加更详细的错误信息
        #     self.logger.error(f"Token key missing in response: {response['data']}")
        #     return {
        #         "status_code": 500,
        #         "data": None,
        #         "error": f"Token key missing: {str(e)}"
        #     }
        # except requests.HTTPError as e:
        #     error_resp = self._handle_error(e)
        #     return {
        #         "status_code": error_resp["status_code"],
        #         "data": None,
        #         "error": error_resp["error"]
        #     }

    def logout(self) -> dict[str, Any]:
        """
        清除登录状态
        """
        response = self.post(self.LOGOUT_ENDPOINT)
        self.session.headers.pop("Authorization", None)
        return {
            "status_code": response["status_code"],
            "error": response["error"]["message"] if response["error"] else None
        }
        # try:
        #     response = self.post(self.LOGOUT_ENDPOINT)
        #     self.session.headers.pop("Authorization", None)
        #     # self.post(self.LOGOUT_ENDPOINT)
        #     return {"status_code": response["status_code"]}
        # except requests.HTTPError as e:
        #     return self._handle_error(e)
        # return {
        #     "status_code": e.response.status_code,
        #     "error": str(e)
        # }
