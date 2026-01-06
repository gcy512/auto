# -*- coding: utf-8 -*-
"""
pytest配置文件，用于设置编码和全局配置
注意：不修改sys.stdout/stderr，避免与pytest的捕获机制冲突
"""
import sys
import os

# 只设置环境变量，不修改标准输出流（避免与pytest冲突）
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

