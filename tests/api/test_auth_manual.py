# test_auth_manual.py
from src.api import AuthClient

client = AuthClient("https://reqres.in/api")
response = client.login("eve.holt@reqres.in", "cityslicka")

print("Login Response:")
print(f"Status: {response['status_code']}")
print(f"Token: {response.get('token')}")
print(f"Error: {response.get('error')}")
print(f"Detail: {response.get('detail')}")