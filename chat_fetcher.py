#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
群聊消息获取模块
作者: Frandy
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ChatFetcher:
    """群聊消息获取器"""

    def __init__(self, api_base_url: str, account: str):
        self.api_base_url = api_base_url
        self.account = account
        self.session = requests.Session()

    def fetch_messages_page(self, username: str, limit: int = 100, offset: int = 0) -> Optional[Dict]:
        """分页获取群消息"""
        url = f"{self.api_base_url}/api/chat/messages"
        params = {
            "account": self.account,
            "username": username,
            "limit": limit,
            "offset": offset,
            "order": "desc",
            "render_types": "text"
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"获取消息失败: {e}")
            return None

    def fetch_yesterday_messages(self, username: str, page_size: int = 500) -> List[Dict]:
        """获取昨天一整天的文本消息"""
        yesterday = datetime.now().date() - timedelta(days=1)
        logger.info(f"正在获取昨天({yesterday})的消息")

        all_messages = []
        offset = 0

        while True:
            logger.info(f"正在获取第 {offset // page_size + 1} 页消息 (offset={offset})")
            data = self.fetch_messages_page(username, limit=page_size, offset=offset)

            if not data or data.get("status") != "success":
                logger.error("获取消息失败")
                break

            messages = data.get("messages", [])
            if not messages:
                logger.info("没有更多消息")
                break

            for msg in messages:
                create_time = msg.get("createTime", 0)
                msg_date = datetime.fromtimestamp(create_time).date()

                if msg_date == yesterday:
                    all_messages.append(msg)
                elif msg_date < yesterday:
                    logger.info("已到达前天，停止获取")
                    logger.info(f"共获取昨天 {len(all_messages)} 条消息")
                    return all_messages

            has_more = data.get("hasMore", False)
            if not has_more:
                logger.info("没有更多数据")
                break

            last_msg_time = messages[-1].get("createTime", 0) if messages else 0
            last_msg_date = datetime.fromtimestamp(last_msg_time).date()
            if last_msg_date < yesterday:
                logger.info("最后一条消息已早于昨天，停止获取")
                break

            offset += page_size

        logger.info(f"共获取昨天 {len(all_messages)} 条消息")
        return all_messages

    def filter_user_messages(self, messages: List[Dict]) -> List[Dict]:
        """过滤出群用户的对话消息"""
        if not messages:
            return []

        filtered_messages = []
        for msg in messages:
            if msg.get("renderType") == "text" and msg.get("content"):
                filtered_messages.append({
                    "sender": msg.get("senderUsername", "未知"),
                    "groupNickname": msg.get("senderDisplayName", "未知"),
                    "content": msg.get("content", ""),
                    "timestamp": msg.get("createTime", 0),
                })

        logger.info(f"过滤后保留 {len(filtered_messages)} 条用户消息")
        return filtered_messages
