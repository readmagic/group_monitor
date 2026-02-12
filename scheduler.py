#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器
作者: Frandy
"""

import schedule
import time
import logging
import subprocess
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_monitor():
    """执行监控任务"""
    try:
        script_dir = Path(__file__).parent
        main_script = script_dir / "main.py"

        logger.info("开始执行群聊监控任务...")
        result = subprocess.run(
            ["python", str(main_script)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'  # 遇到无法解码的字符时用替换字符代替
        )

        if result.returncode == 0:
            logger.info("监控任务执行成功")
            if result.stdout:
                logger.info(f"输出: {result.stdout}")
        else:
            logger.error(f"监控任务执行失败: {result.stderr}")
            if result.stdout:
                logger.info(f"输出: {result.stdout}")

    except Exception as e:
        logger.error(f"执行监控任务时发生错误: {e}")


def main():
    """主函数"""
    # 每天凌晨 1 点执行
    schedule.every().day.at("01:00").do(run_monitor)

    logger.info("定时任务调度器已启动，等待每天 01:00 执行...")
    logger.info("按 Ctrl+C 退出")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    except KeyboardInterrupt:
        logger.info("定时任务调度器已停止")


if __name__ == "__main__":
    main()
