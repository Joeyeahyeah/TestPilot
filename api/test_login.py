import pytest
from typing import Optional, Dict, Any
from api.api_client import APIClient

class AuthClient(APIClient):
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """登录接口封装"""
        return self.post("/auth/login", json={"username": username, "password": password})

    def logout(self) -> bool:
        """登出接口封装"""
        return self.post("/auth/logout").get("success", False)

# @pytest.fixture(scope="module")
# def api():
#     return APIClient("https://api.demo.com")
#
# @pytest.mark.parametrize("username, password, expected_code",
#                          [("admin", "123456", 200),
#                           ("test", "wrong_pwd", 401)])
#
# def test_login(api, username, password, expected_code):
#     resp = api.post("/login", json={"user": username, "pwd": password})
#     assert resp.status_code == expected_code

@pytest.fixture
def auth_client() -> AuthClient:
    """返回已初始化的AuthClient实例"""
    return AuthClient("https://api.demo.com")

# 测试数据分离到单独变量或文件
TEST_CASES = [
    ("admin", "123456", 200),  # 正确密码
    ("test", "wrong_pwd", 401)  # 错误密码
]

@pytest.mark.parametrize("username, password, expected_code", TEST_CASES)
def test_login(auth_client: AuthClient, username: str, password: str, expected_code: int):
    """测试登录接口的多种场景"""
    response = auth_client.login(username, password)
    assert response["status_code"] == expected_code