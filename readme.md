# TestPilot

TestPilot 是一款智能测试自动化平台，旨在通过 API + UI 自动化测试 和 CI/CD 集成，帮助研发团队提升测试效率与质量保障能力。


## 环境准备

**开发/测试**

```bash
# 安装完整依赖
pip install -r requirements.txt -r requirements-test.txt

# 安装核心依赖
pip install -r requirements.txt

# 安装测试依赖
pip install -r requirements-test.txt

# 运行测试
pytest tests/
```