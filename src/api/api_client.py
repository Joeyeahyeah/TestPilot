from http.client import responses

import requests
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
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
        # url = f"{self.base_url}{endpoint}"
        # return requests.get(url, params=params)

    def post(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, json=json).json()
        # url = f"{self.base_url}{endpoint}"
        # return requests.post(url, json=json)
    #  可以扩展 put/delete/patch 等方法...
