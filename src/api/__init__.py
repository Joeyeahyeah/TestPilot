"""
API 核心模块
    包含所有与服务端交互的客户端封装
"""

from .api_client import APIClient   # 暴露基础类
from .clients import AuthClient     # 暴露常用客户端
import requests

__all__ = ["APIClient", "AuthClient"]   #限制from api import *时的导出
requests.Session().headers.update({"User-Agent": "TestPilot"})
