from http.client import responses
import requests
import logging
from typing import Optional, Dict, Any, Callable

"""
基础HTTP请求封装（通用层）
get(), post(), put(), delete()
"""

# 日志配置
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str,
                 default_headers: Optional[Dict[str, str]] = None,
                 responses_handler: Optional[Callable] = None):
        """
        初始化API客户端
        :param base_url: 基础URL
        :param default_headers: 默认请求头（可覆盖）
        :param responses_handler: 自定义响应处理函数（可选）
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.session()  # 复用TCP连接
        # 合并默认头和用户传入头
        self._set_default_headers(default_headers or {})
        self.response_handler = responses_handler or self._default_responses_handler
        # 添加 Reqres API key 头
        # self.session.headers.update({
        #     "x-api-key": "reqres-free-v1",
        #     "Content-Type": "application/json"
        # })
        # self.session.headers.update({"Content-Type": "application/json"})

    def _set_default_headers(self, headers: Dict[str, str]):
        """默认请求头"""
        default = {
            "Content-Type": "application/json",
            "User-Agent": "TestPilot"
        }
        if headers:
            default.update(headers)
        self.session.headers.update(default)

    def _default_responses_handler(self, response: requests.Response) -> Dict[str, Any]:
        """默认响应处理：统一返回格式"""
        result = {
            "status_code": response.status_code,
            "data": None,
            "headers": dict(response.headers),
            "error": None
        }
        try:
            result["data"] = response.json()
        except ValueError as e:
            logger.warning(f"Failed to parse JSON from{response.url}: {str(e)}")
            result["data"] = response.text  # 尝试返回原始文本

        # 处理错误
        if not response.ok:
            status_desc = responses.get(response.status_code, "Unknown error")
            error_msg = f"HTTP Error: {response.status_code}: {status_desc}"
            result["error"] = {
                "message": error_msg,
                "detail": result["data"]  # 附带原始错误信息
            }
        return result

    # 底层请求方法
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        endpoint = endpoint.lstrip('/')
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            return self.response_handler(response)
        except requests.RequestException as e:
            # 处理请求异常
            logger.error(f"Failed to {method} {url}: {str(e)}")
            return {
                "url": url,
                "status_code": None,
                "data": None,
                "headers": None,
                "error": {
                    "message": "Request failed",
                    "detail": str(e)
                }
            }
            # response.raise_for_status()  # 自动抛出HTTP错误
            # return {
            #     "status_code": response.status_code,
            #     "data": response.json(),
            #     "headers": dict(response.headers),  # 确保 headers 存在
            #     "error": None
            # }
        # except requests.HTTPError as e:
        #     return {
        #         "status_code": e.response.status_code,
        #         "data": None,
        #         "headers": dict(e.response.headers) if e.response else None,
        #         "error": e.response.text
        #     }

    # 暴露常用HTTP方法
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", endpoint, json=json)

    #  可以扩展 put/delete/patch 等方法...
    def put(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("PUT", endpoint, json=json)

    def delete(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("DELETE", endpoint, json=json)

    def patch(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("PATCH", endpoint, json=json)
