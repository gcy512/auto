# -*- coding: utf-8 -*-
import os
import sys

# 设置环境变量解决Windows终端乱码问题（不修改sys.stdout/stderr，避免与pytest冲突）
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    # 尝试设置控制台代码页（如果可能）
    try:
        os.system('chcp 65001 >nul 2>&1')
    except:
        pass

import pytest

if __name__ == '__main__':
    # 运行pytest，使用pytest.ini中的配置
    exit_code = pytest.main()
    # 生成allure报告
    os.system("allure generate ./reporters/temp -o ./reporters/html --clean")
    sys.exit(exit_code)

print("hello world")
print('新增代码')
print("切换分支")