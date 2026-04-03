#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信通知器
作者: Frandy
"""

import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)


class WeChatNotifier:
    """微信通知器"""

    def __init__(self, webhook_url: str, webhook_secret: str):
        """
        初始化微信通知器

        Args:
            webhook_url: Webhook URL
            webhook_secret: Webhook Secret
        """
        self.webhook_url = webhook_url
        self.webhook_secret = webhook_secret

    def send_message(self, text: str) -> bool:
        """
        发送微信消息

        Args:
            text: 消息内容

        Returns:
            是否成功
        """
        if not self.webhook_url or not self.webhook_secret:
            logger.warning("微信 Webhook 配置不完整，跳过通知")
            return False

        try:
            headers = {
                "Content-Type": "application/json",
                "X-Webhook-Secret": self.webhook_secret
            }
            payload = {"text": text}

            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                logger.info("微信通知发送成功")
                return True
            else:
                logger.error(f"微信通知发送失败: HTTP {response.status_code} - {response.text}")
                return False

        except requests.exceptions.Timeout:
            logger.error("微信通知发送超时")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"微信通知发送失败: {e}")
            return False
        except Exception as e:
            logger.error(f"发送微信通知时发生错误: {e}")
            return False

    def notify_report_uploaded(self, report_date: str, github_url: Optional[str] = None) -> bool:
        """
        通知报告已上传

        Args:
            report_date: 报告日期
            github_url: GitHub 链接（可选）

        Returns:
            是否成功
        """
        message = f"✅ 群聊报告已上传\n日期: {report_date}"
        if github_url:
            message += f"\n链接: {github_url}"

        return self.send_message(message)