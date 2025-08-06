import os
import sys
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#导入API客户端相关类
from src.api import APIClient
from src.api.clients import AuthClient, UserClient

#首先添加获取测试报告的钩子函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取每个测试用例的执行结果并存储"""
    outcome = yield
    rep = outcome.get_result()
    # 将结果存储在item的属性中，后续可以通过item.rep_call访问
    setattr(item, "rep_" + rep.when, rep)

#修改自动重试fixture
@pytest.fixture(autouse=True)
def auto_retry(request):
    """自动重试失败用例，最多重试2次"""
    yield
    # 检查测试是否失败
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        max_retries = 2
        current_retry = request.node.execution_count - 1
        if current_retry < max_retries:
            request.node.add_marker(pytest.mark.flaky(reruns=max_retries - current_retry))
            time.sleep(1)
    # if request.node.rep_call.failed:
    #     time.sleep(1)
    #     return request.node.rerun()
@pytest.fixture
def smart_wait(browser):
    """提供智能等待功能，用于页面元素"""
    def _wait(locator, timeout=10):
        return WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(locator))
    return _wait

# 页面中使用
class ProductPage:
    def add_to_cart(self, smart_wait):
        smart_wait((By.ID, "add-btn")).click()  # 自动等待元素
# 测试指标收集
def pytest_terminal_summary(terminalreporter):
   # duration = time.time() - terminalreporter._sessionstarttime
   # 新代码：通过session获取开始时间
   # duration = time.time() - terminalreporter.config.session._sessionstarttime
   # 正确获取测试开始时间的方式（兼容新版本pytest）
   # session = terminalreporter._session
   # duration = time.time() - session._starttime  # 使用session的_starttime属性
   # 兼容不同 pytest 版本获取测试时长
   try:
       # 1. 确保 reports 目录存在
       reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
       os.makedirs(reports_dir, exist_ok=True)

       # 2. 构建完整文件路径
       report_path = os.path.join(reports_dir, "metrics.txt")

       # 3. 获取测试数据（兼容不同pytest版本）
       session = getattr(terminalreporter, "_session", None)
       duration = (time.time() - session._starttime) if hasattr(session, "_starttime") else 0

       # 统计各种状态的用例数量
       stats = terminalreporter.stats
       passed = len(terminalreporter.stats.get('passed', []))
       failed = len(terminalreporter.stats.get('failed', []))
       skipped = len(terminalreporter.stats.get('skipped', []))
       total = passed + failed + skipped

       # 4. 写入报告文件（使用绝对路径）
       try:
           with open(report_path, "a", encoding="utf-8") as f:
               f.write(f"test_duration {duration:.2f}s\n")
               f.write(f"test_total {total}\n")
               f.write(f"test_pass {passed}\n")
               f.write(f"test_fail {failed}\n")
               f.write(f"test_skip {skipped}\n")
               if total > 0:
                   f.write(f"test_pass_rate {passed / total * 100:.2f}%\n")
               else:
                   f.write("test_pass_rate 0%\n")
               f.write("-" * 50 + "\n")
       except IOError as e:
           print(f"\n 写入报告出错：{str(e)}")
   except Exception as e:
        print(f"\n⚠️ 生成测试报告时出错: {str(e)}", file=sys.stderr)
        f.write("------------------------------------------------------------------------------\n")

# API测试相关Fixture
@pytest.fixture(scope="session")
def api_base_url():
    """API服务基础URL 可根据环境变量切换"""
    # return "http://localhost:8000"
    return "https://reqres.in/api"
@pytest.fixture
def auth_client(api_base_url):
    """认证客户端Fixture，负责处理登录状态"""
    client = AuthClient(api_base_url)
    # login_response = client.login(username="username", password="password")
    # ReqRes
    assert client.check_health(), "API服务不可用"
    # Reqres old
    # login_response = client.login(
    #     username="eve.holt@reqres.in",
    #     password="cityslicka"
    # )
    # assert  login_response["status_code"] == 200, "登录失败"
    # assert "token" in login_response, "登录响应中未包含token"
    yield client # 提供给测试用例使用
    # 登出可能不需要，因为 Reqres 没有真正的会话
    # client.logout()

@pytest.fixture
def test_user_data():
    timestamp = int(time.time())
    return {
        "name": f"Test User {timestamp}",
        "job": f"Developer {timestamp}"
    }

@pytest.fixture
def user_client(api_base_url, auth_client):
    """用户管理客户端Fixture， 依赖已认证的auth_client"""
    return UserClient(api_base_url, auth_client)