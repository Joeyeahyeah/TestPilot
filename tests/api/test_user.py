import pytest
from src.api.clients.auth_client import AuthClient
from src.api.clients.user_client import UserClient

"""
专门测试用户管理接口（需要依赖登录态）
"""

@pytest.fixture
def user_client(auth_client: AuthClient) -> UserClient:
    # 先确保登录
    auth_client.login("admin", "admin123")
    # 创建依赖登录态的客户端
    return UserClient("https://api.example.com", auth_client)


def test_user_lifecycle(user_client: UserClient):
    """测试用户创建->查询->更新全流程"""
    # 1. 创建用户
    new_user = {
        "name": "测试用户",
        "email": "test@example.com",
        "role": "member"
    }
    create_res = user_client.create_user(new_user)
    user_id = create_res["id"]

    # 2. 查询用户
    get_res = user_client.get_user(user_id)
    assert get_res["email"] == "test@example.com"

    # 3. 更新用户
    update_res = user_client.update_user(user_id, {"role": "admin"})
    assert update_res["role"] == "admin"

    # 4. 验证更新
    get_res = user_client.get_user(user_id)
    assert get_res["role"] == "admin"