import os
import sys
from typing import Optional, Any, Dict, List

# 获取当前文件的绝对路径
_CURRENT_FILE_PATH = os.path.abspath(__file__)

# 项目根目录
PROJECT_ROOT = os.path.dirname(_CURRENT_FILE_PATH)

# 确保项目根目录被添加到Python 搜索路径
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0,PROJECT_ROOT)

# 定义常用子目录路径
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
API_DIR = os.path.join(SRC_DIR, "api")
CLIENTS_DIR = os.path.join(API_DIR, "clients")

def get_relative_path(relative_path: str) -> str:
    """
    将相对路径转换为基于项目根目录的绝对路径
    Args:
        relative_path: 相对于项目根目录的路径（如 "data/config.json"）
    Returns:
        绝对路径字符串
    """
    return os.path.abspath(os.path.join(PROJECT_ROOT, relative_path))

def verify_path_exists() -> None:
    """
    验证路径是否存在，如果不存在则抛出异常
    Args:
        path: 路径字符串
    """
    requried_path = [PROJECT_ROOT, SRC_DIR, TESTS_DIR, API_DIR, CLIENTS_DIR]
    for dir_path in requried_path:
        if not os.path.isdir(dir_path):
            raise FileNotFoundError(f"关键路径 {dir_path} 不存在")

# 验证路径是否存在
try:
    verify_path_exists()
except FileNotFoundError as e:
    print(f"关键路径验配置错误: {str(e)}", file=sys.stderr)
    sys.exit(1)