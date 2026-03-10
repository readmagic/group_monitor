#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DashScope 摘要器
作者: Frandy
"""

import requests
from typing import List, Dict, Optional
import logging
import json

from .base import BaseSummarizer
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


class DashScopeSummarizer(BaseSummarizer):
    """DashScope AI 摘要器"""

    def __init__(self, api_key: str, model: str = "qwen3-235b-a22b-instruct-2507"):
        self.api_key = api_key
        self.model = model
        self.session = requests.Session()

    TEMP_NICKNAME = "小黄1"

    def summarize(self, messages: List[Dict]) -> Optional[str]:
        """使用 DashScope 大模型流式总结对话"""
        if not messages:
            return None

        # 替换特殊昵称为临时昵称（去除前后空格后对比）
        processed_messages = []
        for msg in messages:
            nickname = msg['groupNickname'].strip()
            if "涉黄" in nickname:
                processed_messages.append({**msg, 'groupNickname': self.TEMP_NICKNAME})
            else:
                processed_messages.append(msg)

        conversation_text = "\n".join([
            f"{msg['groupNickname']}: {msg['content']}"
            for msg in processed_messages
        ])

        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-SSE": "enable"
        }

        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": USER_PROMPT_TEMPLATE.format(conversation=conversation_text)
                    }
                ]
            },
            "parameters": {
                "result_format": "message",
                "incremental_output": True
            }
        }

        try:
            logger.info("正在调用 DashScope 进行对话总结（流式）...")
            response = self.session.post(url, headers=headers, json=payload, stream=True, timeout=300)
            response.raise_for_status()

            full_content = []
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data:'):
                        data_str = line_str[5:].strip()
                        if data_str:
                            try:
                                data = json.loads(data_str)
                                if data.get("output") and data["output"].get("choices"):
                                    content = data["output"]["choices"][0].get("message", {}).get("content", "")
                                    if content:
                                        full_content.append(content)
                            except json.JSONDecodeError:
                                continue

            summary = "".join(full_content)
            if summary:
                logger.info("总结完成")
                # 将临时昵称替换回特殊昵称
                return summary.replace(self.TEMP_NICKNAME, "ⓘ 该群聊涉黄已被解散")
            else:
                logger.error("DashScope 返回内容为空")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"调用 DashScope 失败: {e}")
            return None


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(__file__).rsplit('/', 2)[0])
    from config import Config

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    config = Config('.env')
    if not config.dashscope_api_key:
        print("错误: 未配置 DASHSCOPE_API_KEY")
        sys.exit(1)

    summarizer = DashScopeSummarizer(config.dashscope_api_key)
    success = summarizer.test_connection()
    sys.exit(0 if success else 1)
