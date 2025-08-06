from typing import Dict, Any, Optional


'''
封装通用断言
    例如，检查状态码、响应字段存在性等
'''
def assert_status_code(response: Dict[str, Any], expected_code: int):
    assert response["status_code"] == expected_code, \
        f"Expected status code {expected_code}, but got {response['status_code']}"

def assert_field_exists(response: Dict[str, Any], field: str) -> None:
    assert field in response["data"], \
        f"Field '{field}' does not exist in response data"