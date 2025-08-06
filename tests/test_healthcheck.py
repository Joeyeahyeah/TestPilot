from src.api import AuthClient


def test_api_health(auth_client: AuthClient):
    """测试API基础可用性"""
    assert auth_client.check_health()