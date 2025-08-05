import pytest
from src.api.client.auth_client import AuthClient


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

# @pytest.fixture
# def auth_client() -> AuthClient:
#     """返回已初始化的AuthClient实例"""
#     return AuthClient("https://api.demo.com")
#
#
# # 测试数据分离到单独变量或文件
# TEST_CASES = [
#     ("admin", "123456", 200),  # 正确密码
#     ("test", "wrong_pwd", 401)  # 错误密码
# ]
#
#
# @pytest.mark.parametrize("username, password, expected_code", TEST_CASES)
# def test_login(auth_client: AuthClient, username: str, password: str, expected_code: int):
#     """测试登录接口的多种场景"""
#     response = auth_client.login(username, password)
#     assert response["status_code"] == expected_code

@pytest.fixture
def auth_client() -> AuthClient:
    """返回配置好基础URL的AuthClient"""
    return AuthClient("https://api.demo.com")


class TestAuth:
    @pytest.mark.parametrize("username, password, expected_status", [
        ("admin", "correct_pwd", 200),  # 正常用例
        ("admin", "wrong_pwd", 401),  # 密码错误
        ("", "any_pwd", 400),  # 空用户名
    ])
    def test_login(self, auth_client: AuthClient, username: str, password: str, expected_status: int):
        """测试登录接口的各种场景"""
        result = auth_client.login(username, password)

        # 公共断言
        assert result["status_code"] == expected_status

        # 成功时的额外断言
        if expected_status == 200:
            assert "token" in result["data"]
            assert isinstance(result["data"]["expires_in"], int)
        # 失败时的额外断言
        else:
            assert "error" in result
            assert len(result["error"]) > 0

    def test_logout(self, auth_client: AuthClient):
        """测试登出功能"""
        # 先登录获取cookie/token
        login_res = auth_client.login("admin", "correct_pwd")
        assert login_res["status_code"] == 200

        # 执行登出
        logout_res = auth_client.logout()
        assert logout_res["status_code"] == 200
