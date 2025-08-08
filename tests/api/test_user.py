import time
import pytest
# from src.api.clients.auth_client import AuthClient
from typing import Dict, Any, Optional
from src.api import UserClient

"""
专门测试用户管理接口（需要依赖登录态）
"""

# @pytest.fixture
# def user_client(auth_client: AuthClient) -> UserClient:
#     # 先确保登录
#     auth_client.login("admin", "admin123")
#     # 创建依赖登录态的客户端
#     return UserClient("https://api.example.com", auth_client)
# ----------------------------- origin ---------------------------------
# def test_user_lifecycle(user_client: UserClient):
#     """测试用户创建->查询->更新全流程"""
#     # 1. 准备测试数据
#     test_user_data = {
#         "name": "测试用户",
#         "email": f"test_{int(time.time())}@example.com",
#         "role": "member"
#     }
#
#     # 2. 创建用户对象
#     create_response = user_client.create_user(test_user_data)
#     # 验证创建响应
#     assert create_response["status_code"] == 201, \
#         f"创建用户失败，状态码：{create_response['status_code']}"
#     assert "data" in create_response, "创建响应缺少data字段"
#     user_id = create_response["data"]["id"]
#     assert user_id, "创建的用户未返回ID"
#
#     # 3. 查询用户详情
#     get_res = user_client.get_user(user_id)
#     # 验证查询响应
#     # assert get_res["email"] == "test@example.com"
#     assert get_res["status_code"] == 200, \
#         f"查询用户失败，状态码：{get_res['status_code']}"
#     assert "data" in get_res, "查询响应缺少data字段"
#     user_data = get_res["data"]
#     # 验证用户数据正确性
#     assert user_data["name"] == test_user_data["name"], "用户名不匹配"
#     assert user_data["email"] == test_user_data["email"], "邮箱不匹配"
#     assert user_data["role"] == test_user_data["role"], "角色不匹配"
#
#     # 3. 更新用户信息
#     update_data = {
#         "name": "更新后的测试用户",
#         "role": "admin"
#     }
#     update_response = user_client.update_user(user_id, update_data)
#     #验证更新响应
#     assert update_response["status_code"] == 200, \
#         f"更新用户失败，状态码: {update_response['status_code']}"
#     assert "data" in update_response, "更新响应缺少data字段"
#     assert update_response["data"]["name"] == update_data["name"], "名称更新失败"
#     assert update_response["data"]["role"] == update_data["role"], "角色更新失败"
#
#     # 5. 再次查询验证更新结果
#     get_updated_response = user_client.get_user(user_id)
#     assert get_updated_response["status_code"] == 200, "更新后查询失败"
#     updated_user_data = get_updated_response["data"]
#     assert updated_user_data["name"] == update_data["name"], "更新后名称不匹配"
#     assert updated_user_data["role"] == update_data["role"], "更新后角色不匹配"
#
# def test_create_user_with_invalid_data(user_client: UserClient):
#     """测试使用无效数据创建用户"""
#     # 测试用例：缺少必填字段
#     invalid_data = {
#         "name": "无效用户"  # 缺少email等必填字段
#     }
#     response = user_client.create_user(invalid_data)
#
#     # 验证错误响应
#     assert response["status_code"] in [400, 422], \
#         f"预期错误状态码，实际得到: {response['status_code']}"
#     assert "error" in response or "detail" in response["data"], \
#         "错误响应缺少错误信息"
#
# def test_get_non_existent_user(user_client: UserClient):
#     """测试查询不存在的用户"""
#     non_existent_user_id = "999999"  # 假设这个ID不存在
#     response = user_client.get_user(non_existent_user_id)
#
#     # 验证错误响应
#     assert response["status_code"] == 404, \
#         f"查询不存在用户应返回404，实际得到: {response['status_code']}"
#
# def test_update_user_with_invalid_data(user_client: UserClient):
#     """测试使用无效数据更新用户"""
#     # 先创建一个正常用户
#     create_response = user_client.create_user({
#         "name": "待更新用户",
#         "email": f"update_test_{int(time.time())}@example.com",
#         "role": "member"
#     })
#     user_id = create_response["data"]["id"]
#
#     # 使用无效数据更新
#     invalid_update = {
#         "email": "invalid-email"  # 无效的邮箱格式
#     }
#     response = user_client.update_user(user_id, invalid_update)
#
#     # 验证错误响应
#     assert response["status_code"] in [400, 422], \
#         f"预期错误状态码，实际得到: {response['status_code']}"
#
# # 添加参数化测试，覆盖更多场景
# @pytest.mark.parametrize("user_role,expected_status", [
#     ("admin", 201),  # 有效角色
#     ("editor", 201),  # 有效角色
#     ("invalid", 400)  # 无效角色
# ])
#
# def test_create_user_with_different_roles(user_client: UserClient, user_role: str, expected_status: int):
#     """测试创建不同角色的用户（参数化测试）"""
#     response = user_client.create_user({
#         "name": f"角色测试用户_{user_role}",
#         "email": f"role_{user_role}_{int(time.time())}@example.com",
#         "role": user_role
#     })
#     assert response["status_code"] == expected_status, \
#         f"角色为{user_role}时，预期状态码{expected_status}，实际{response['status_code']}"

# ----------------------------- Reqres ---------------------------------
def test_user_lifecycle(user_client: UserClient, test_user_data: dict):
    # 1. 创建用户
    create_response = user_client.create_user(test_user_data)
    assert create_response["status_code"] == 201

    # Reqres返回创建的用户数据，但没有持久化存储
    created_data = create_response["data"]
    assert created_data["name"] == test_user_data["name"]
    assert created_data["job"] == test_user_data["job"]
    # user_id = created_data["id"]
    assert "id" in created_data

    # 2. 模拟更新用户
    user_id = created_data["id"]
    update_data = {"name": "Updated Name", "job": "Updated Job"}
    update_response = user_client.update_user(user_id, update_data)
    assert update_response["status_code"] == 200
    assert update_response["data"]["name"] == update_data["name"]
    assert update_response["data"]["job"] == update_data["job"]

def test_create_user(user_client: UserClient):
    """测试创建用户（模拟）"""
    test_data = {
        "name": "Test User",
        "job": "Tester"
    }
    response = user_client.create_user(test_data)
    assert response["status_code"] == 201
    assert response["data"]["name"] == test_data["name"]

def test_get_user(user_client: UserClient):
    # Reqres预定义用户ID
    response = user_client.get_user("2")

    # print(f"完整响应数据: {response}")  # 调试用
    # assert response["status_code"] == 200
    # assert "data" in response
    # assert response["data"]["id"] == 2
    # assert "email" in response["data"]

    assert response["status_code"] == 200
    assert "data" in response, f"响应中缺少data字段: {response}"
    assert "data" in response["data"], f"外层data中缺少内层data字段: {response['data']}"
    assert "id" in response["data"]["data"], f"内层data中缺少id字段: {response['data']['data']}"
    assert response["data"]["data"]["id"] == 2


def test_get_nonexistent_user(user_client: UserClient):
    response = user_client.get_user("999")
    assert response["status_code"] == 404


@pytest.mark.parametrize("bad_data", [
    {},  # 空数据
    {"invalid_field": "value"},  # 无效字段
    {"name": "", "job": ""},  # 空值
])
def test_create_invalid_user(user_client: UserClient, bad_data: dict):
    response = user_client.create_user(bad_data)
    # 修正：Reqres对任何POST /users都返回201
    assert response["status_code"] == 201
    # 可选：验证返回数据包含默认字段（如id、createdAt）
    assert "id" in response["data"]
    assert "createdAt" in response["data"]
# ----------------------------- Reqres ---------------------------------