#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摘要提示词常量
作者: Frandy
"""

SYSTEM_PROMPT = """你是一个专业的对话总结助手，请对以下微信群聊对话进行总结，提取关键信息、活跃群成员、主要话题和重要结论。如果话题涉及到技术类型，给予AI的见解。"""

USER_PROMPT_TEMPLATE = """请总结以下群聊对话：

{conversation}"""
