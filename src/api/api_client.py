from http.client import responses
import requests
from typing import Optional, Dict, Any

"""
基础HTTP请求封装（通用层）
get(), post(), put(), delete()
"""

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.session()  # 复用TCP连接
        # 添加 Reqres API key 头
        self.session.headers.update({
            "x-api-key": "reqres-free-v1",
            "Content-Type": "application/json"
        })
        # self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str,Any]:
        endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # 自动抛出HTTP错误
            return {
                "status_code": response.status_code,
                "data": response.json(),
                "headers": response.headers
            }
        except requests.HTTPError as e:
            return {
                "status_code": e.response.status_code,
                # "data": e.response.json(),
                # "headers": e.response.headers
                "error": e.response.text
            }

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, params=params)
        # response = self._request("GET", endpoint, params=params)
        # return {
        #     "status_code": response.status_code,
        #     "data": response.json(),
        #     "headers": response.headers
        # }
    
    def post(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, json=json)
        # response = self._request("POST", endpoint, json=json)
        # return {
        #     "status_code": response.status_code,
        #     "data": response.json(),
        #     "headers": response.headers
        # }
    #  可以扩展 put/delete/patch 等方法...
    def put(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("PUT", endpoint, json=json)