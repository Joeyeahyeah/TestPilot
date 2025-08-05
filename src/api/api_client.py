from http.client import responses
import requests
from typing import Optional, Dict, Any

"""
基础HTTP请求封装（通用层）
get(), post(), put(), delete()
"""

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.session()  # 复用TCP连接
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()  # 自动抛出HTTP错误
        return response

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, params=params).json()

    def post(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, json=json).json()

    #  可以扩展 put/delete/patch 等方法...
