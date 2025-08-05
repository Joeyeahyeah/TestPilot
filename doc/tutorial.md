# TestPilot 自动化测试教程

## 📅 **整体时间规划（建议4-6周）**

| 阶段       | 时间   | 核心目标          | 关键交付物                      |
|----------|------|---------------|----------------------------|
| **环境搭建** | 0.5天 | 开发环境就绪        | 本地可运行的Python+Pytest        |
| **阶段一**  | 1~2周 | 完成API+UI自动化框架 | 可执行的测试用例+Allure报告          |
| **阶段二**  | 1周   | 集成CI/CD流水线    | GitHub Actions流水线+Docker镜像 |
| **阶段三**  | 1周   | 扩展1-2项进阶能力    | 测试数据工厂/Grafana仪表盘          |
| **文档总结** | 0.5天 | 项目复盘与简历包装     | 技术文档+简历话术                  |

---

## 🛠️ **阶段一：自动化测试框架搭建（核心重点）**

### 📌 步骤1：技术栈安装（Day 1）

```bash
# 必装工具清单
Python 3.8+  
pip install pytest requests selenium allure-pytest pytest-html  
Chrome浏览器 + 对应版本ChromeDriver  
IDE：VSCode或PyCharm
```

### 📌 步骤2：API自动化实现（Day 2-3）

**任务清单**：

1. 创建项目结构：
   ```bash
   /project
     ├── api
     │   ├── test_login.py    # 测试用例
     │   └── api_client.py    # 封装请求工具
     ├── utils
     │   └── data_loader.py   # 数据读取工具
     └── conftest.py          # 全局配置
   ```
2. 封装API客户端 (`api_client.py`)：
   ```python
   import requests
   class APIClient:
       def __init__(self, base_url):
           self.base_url = base_url
           
       def post(self, endpoint, json=None):
           url = f"{self.base_url}{endpoint}"
           return requests.post(url, json=json)
   ```
3. 编写数据驱动测试用例 (`test_login.py`)：
   ```python
   import pytest
   from apiclient import APIClient
   # from .api_client import APIClient
   
   @pytest.fixture(scope="module")
   def api():
       return APIClient("https://api.demo.com")
   
   @pytest.mark.parametrize("username, password, expected_code", 
       [("admin", "123456", 200), 
        ("test", "wrong_pwd", 401)])
   def test_login(api, username, password, expected_code):
       resp = api.post("/login", json={"user":username, "pwd":password})
       assert resp.status_code == expected_code
   ```

### 📌 步骤3：UI自动化实现（Day 4-6）

**任务清单**：

1. 实现POM模式：
   ```bash
   /project
     └── ui
         ├── pages
         │   ├── login_page.py  # 登录页面
         │   └── cart_page.py   # 购物车页面
         └── tests
             └── test_cart.py   # 测试用例
   ```
2. 登录页面封装 (`login_page.py`)：
   ```python
   from selenium.webdriver.common.by import By
   
   class LoginPage:
       def __init__(self, driver):
           self.driver = driver
           self.username_loc = (By.ID, "username")
           self.password_loc = (By.ID, "password")
           
       def login(self, username, password):
           self.driver.find_element(*self.username_loc).send_keys(username)
           self.driver.find_element(*self.password_loc).send_keys(password)
           self.driver.find_element(By.ID, "login-btn").click()
   ```
3. 编写购物车测试 (`test_cart.py`)：
   ```python
   def LoginPage():
       pass
   def ProductPage():
       pass
   def CartPage():
       pass
   
   def test_add_cart(browser):  # browser是pytest-selenium提供的fixture
       login_page = LoginPage(browser)
       login_page.login("test_user", "pass123")
       
       product_page = ProductPage(browser)
       product_page.add_to_cart("iPhone 15")
       
       cart_page = CartPage(browser)
       assert "iPhone 15" in cart_page.get_items()
   ```

### 📌 步骤4：测试报告与执行（Day 7）

1. 添加Allure支持：
   ```bash
   # 运行测试并生成报告
   pytest --alluredir=./allure-results
   allure serve ./allure-results  # 本地查看报告
   ```
2. **成果验证**：
    - [x] 执行命令后浏览器自动完成登录+加购操作
    - [x] Allure报告显示API/UI测试通过率
    - [x] 报告包含失败用例的截图和日志

---

## ⚙️ **阶段二：CI/CD流水线集成（工程化落地）**

### 📌 步骤1：代码托管（Day 1）

1. 创建GitHub仓库
2. 提交代码并遵守规范：
   ```bash
   git checkout -b feature/api-automation
   git add .
   git commit -m "feat: add API login tests"
   git push origin feature/api-automation
   ```

### 📌 步骤2：流水线配置（Day 2-3）

1. 创建GitHub Actions文件 (`.github/workflows/api_test.yml`)：
   ```yaml
   name: API Automation
   on: [push]
   jobs:
     test:
       runs-on: ubuntu-latest
       container: python:3.10-slim  # 使用官方镜像
       steps:
       - uses: actions/checkout@v4
       - name: Install dependencies
         run: pip install pytest requests allure-pytest
       - name: Run tests
         run: pytest api/ --alluredir=allure-results
       - name: Upload Allure Report
         uses: actions/upload-artifact@v3
         with:
           name: allure-report
           path: allure-results
   ```

### 📌 步骤3：容器化执行（Day 4）

1. 创建Dockerfile：
   ```dockerfile
   FROM python:3.10-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["pytest", "ui/", "--alluredir=allure-results"] 
   ```
2. 本地验证：
   ```bash
   docker build -t ui-automation . 
   docker run -v $(pwd)/allure-results:/app/allure-results ui-automation
   ```

### ✅ 阶段验证：

1. 推送代码后GitHub Actions自动执行
2. 流水线详情页显示测试通过率
3. 可下载Allure结果文件本地生成报告

---

## 🚀 **阶段三：扩展能力（选择1-2项）**

### 选项1：测试数据工厂（推荐）

```python
# utils/data_factory.py
from faker import Faker


def generate_user():
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address()
    }


# 测试用例中使用
def test_register(api):
    user_data = generate_user()
    resp = api.post("/register", json=user_data)
    assert resp.status_code == 201
```

### 选项2：自动化异常处理

```python
# conftest.py 添加智能等待
import pytest
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
```

### 选项3：可视化监控（需额外1天）

1. 安装Prometheus + Grafana
2. 使用pytest插件收集指标：
   ```python
   # conftest.py
   import time
   def pytest_terminal_summary(terminalreporter):
       duration = time.time() - terminalreporter._sessionstarttime
       with open("metrics.txt", "a") as f:
           f.write(f"test_duration {duration}\n")
           f.write(f"test_pass {terminalreporter.stats.get('passed', 0)}\n")
   ```
3. 配置Grafana面板展示：
   ```mermaid
   graph LR
   A[测试执行] -->|写入指标| B[Prometheus]
   B --> C[Grafana]
   C --> D[展示通过率/时长]
   ```

---

## 📝 **文档与简历包装（核心竞争力转化）**

### 交付物清单：

1. **技术文档**（必须）：
   ```markdown
   ## 项目架构
   ![](./docs/architecture.png)
   
   ## 快速开始
   ```bash
   pip install -r requirements.txt
   pytest api/ --alluredir=./report
   ```

   ## 典型问题解决
   Q: Chrome版本不兼容  
   A: 使用`webdriver_manager`自动匹配驱动：
   ```python
   from selenium import webdriver
   from webdriver_manager.chrome import ChromeDriverManager
   driver = webdriver.Chrome(ChromeDriverManager().install())
   ```

2. **简历话术示例**：
   > **测试自动化平台开发**
   > - 基于Pytest+Allure搭建API/UI自动化框架，采用Page Object模式降低维护成本
   > - 实现GitHub Actions持续集成流水线，测试执行效率提升40%
   > - 开发测试数据工厂自动生成100+边界值用例，发现3个隐蔽逻辑缺陷
   > - 关键创新：通过智能等待机制解决UI测试Flaky问题，稳定性达98%

---

## ⚠️ **关键避坑指南**

1. **环境问题**：
    - 使用`webdriver_manager`自动管理浏览器驱动版本
    - 用`python-dotenv`管理环境变量（不同环境的URL/账号）

2. **UI自动化不稳定**：
    - 禁用浏览器扩展：`chrome_options.add_argument("--disable-extensions")`
    - 添加重试机制：`@pytest.mark.flaky(reruns=2)`

3. **API依赖问题**：
    - 测试前自动初始化数据：`pytest.fixture(scope="module")`
    - 使用Mock服务隔离依赖：`pip install pytest-mock`

4. **CI/CD执行失败**：
    - 本地先执行`pytest --strict-markers`验证标记合法性
    - 在Actions中增加超时设置：`timeout-minutes: 30`

---

## 💡 **执行要点总结**

1. **每天明确目标**：完成1个测试类/1个CI配置/1个工具函数
2. **先跑通再优化**：第一天先实现1个API+1个UI用例全流程
3. **善用GPT调试**：遇到报错直接贴错误日志+代码片段询问
4. **每日代码提交**：Git提交记录就是你的进度证明

**真正的核心竞争力不是写多少代码，而是你如何用自动化解决真实的测试痛点**。按照此计划推进，4周后你将拥有远超同龄人的工程化能力矩阵。