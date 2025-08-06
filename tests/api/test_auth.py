import time
import pytest
from src.api import AuthClient

"""
专门测试认证接口
"""

@pytest.fixture
def auth_client() -> AuthClient:
    """返回配置好基础URL的AuthClient"""
    return AuthClient("https://api.example.com")

class TestAuth:
    # @pytest.mark.parametrize("username, password, expected_status", [
    #     ("admin", "correct_pwd", 200),  # 正常用例
    #     ("admin", "wrong_pwd", 401),    # 密码错误
    #     ("", "any_pwd", 400),           # 空用户名
    #     ("invalid_user", "", 422)       #无效用户
    # ])

    # ------------------------------------Reqres----------------------------------------
    @pytest.mark.parametrize("email, password, expected_status", [
        ("eve.holt@reqres.in", "cityslicka", 200),  # 有效
        ("invalid@reqres.in", "password", 400),  # 无效邮箱
        ("eve.holt@reqres.in", "", 400),  # 空密码
    ])

    def test_login_scenarios(self, auth_client: AuthClient, email, password, expected_status):
        result = auth_client.login(email, password)
        assert result["status_code"] == expected_status

        if expected_status == 200:
            assert "token" in result
            assert len(result["token"]) > 5  # Reqres的token较短
            # # 验证Authorization头
            # assert "Authorization" in auth_client.session.headers
        else:
            assert "error" in result or "detail" in result

    # ------------------------------------Reqres----------------------------------------
    # def test_login_scenarios(self, auth_client: AuthClient, username: str, password: str, expected_status: int):
    #     """测试登录接口的各种场景"""
    #     result = auth_client.login(username, password)
    #     # 公共断言
    #     assert result["status_code"] == expected_status
    #
    #     # 成功时的额外断言
    #     if expected_status == 200:
    #         assert "token" in result
    #         assert isinstance(result["token"], str)
    #         assert len(result["token"]) > 30
    #         assert "expires_in" in result
    #         assert isinstance(result["expires_in"], int)
    #         # 验证状态管理
    #         assert "Authorization" in auth_client.session.headers
    #         assert "Bearer" in auth_client.session.headers["Authorization"]
    #     # 失败时的额外断言
    #     else:
    #         assert "error" in result
    #         assert len(result["error"]) > 0
    #         assert "detail" in result
    #         assert len(result["detail"]) > 0

    def test_logout(self, auth_client: AuthClient):
        """测试登出功能"""
        # 先登录获取cookie/token
        login_res = auth_client.login("admin", "correct_pwd")
        assert login_res["status_code"] == 200
        assert "Authorization" in auth_client.session.headers

        # 执行登出
        logout_res = auth_client.logout()

        #验证响应
        assert logout_res["status_code"] == 200

        #验证状态清除
        assert "Authorization" not in auth_client.session.headers

    def test_login_performance(auth_client):
        """测试登录接口性能"""
        test_cases = [
            ("admin", "correct_pwd", 200),
            ("test_user", "Password", 200)
        ]
        for username, paswword, expected_status in test_cases:
            start = time.perf_counter()
            result = auth_client.login(username, paswword)
            elapsed = time.perf_counter() - start

            assert  result["status_code"] == expected_status
            assert elapsed < 1.0, f"登录耗时 {elapsed:.2f}s 超过1秒限制"  # 响应时间应小于1秒