from .api_client import APIClient  # 相对导入在包内有效

if __name__ == "__main__":
    client = APIClient("https://api.example.com")
    print("测试 API 客户端初始化成功")