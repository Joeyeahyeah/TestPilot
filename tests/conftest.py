import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@pytest.fixture
def smart_wait(browser):
    def _wait(locator, timeout=10):
        return WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(locator))

    return _wait
# 页面中使用
class ProductPage:
    def add_to_cart(self, smart_wait):
        smart_wait((By.ID, "add-btn")).click()  # 自动等待元素



def pytest_terminal_summary(terminalreporter):
   duration = time.time() - terminalreporter._sessionstarttime
   with open("metrics.txt", "a") as f:
       f.write(f"test_duration {duration}\n")
       f.write(f"test_pass {terminalreporter.stats.get('passed', 0)}\n")
