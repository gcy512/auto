# logger.py
# -*- coding: utf-8 -*-
import logging
import os
import sys
from datetime import datetime

from config import logs_path

# 只设置环境变量，不修改标准输出流（避免与pytest冲突）
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'


class APITestLogger:
    @staticmethod
    def setup_logger():
        # 获取当前项目名称（假设为当前工作目录的名称）
        project_name = os.path.basename(os.getcwd())

        # 获取当前时间，格式为YYYYMMDD
        current_time = datetime.now().strftime('%Y%m%d')

        # 创建日志文件名
        log_filename = f"{project_name}_{current_time}.log"

        # 确保日志存放路径存在
        os.makedirs(logs_path, exist_ok=True)

        # 构建完整的日志文件路径
        log_file_path = os.path.join(logs_path, log_filename)

        # 创建日志器
        logger = logging.getLogger(project_name)
        logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if not logger.handlers:
            # 创建文件处理器
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)

            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            # 创建格式器
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # 将格式器添加到处理器
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            # 将处理器添加到日志器
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger


# 使用示例
if __name__ == "__main__":
    logger = APITestLogger.setup_logger()
    logger.info("这是一个测试日志信息。")
