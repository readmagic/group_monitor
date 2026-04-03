#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信通知测试脚本
作者: Frandy
"""

from config import Config
from syncers import WeChatNotifier

if __name__ == "__main__":
    config = Config('.env')

    if not config.wechat_webhook_url or not config.wechat_webhook_secret:
        print("❌ 请在 .env 文件中配置 WECHAT_WEBHOOK_URL 和 WECHAT_WEBHOOK_SECRET")
        exit(1)

    notifier = WeChatNotifier(config.wechat_webhook_url, config.wechat_webhook_secret)

    # 测试发送简单消息
    print("正在发送测试消息...")
    success = notifier.send_message("这是一条测试消息")

    if success:
        print("✅ 测试消息发送成功")
    else:
        print("❌ 测试消息发送失败")