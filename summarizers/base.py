#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摘要器基类
作者: Frandy
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional


class BaseSummarizer(ABC):
    """摘要器基类"""

    @abstractmethod
    def summarize(self, messages: List[Dict]) -> Optional[str]:
        """
        对消息进行摘要

        Args:
            messages: 消息列表

        Returns:
            摘要文本
        """
        pass

    def test_connection(self) -> bool:
        """测试连通性"""
        test_messages = [
            {"groupNickname": "测试用户", "content": "这是一条测试消息"}
        ]
        return self.summarize(test_messages) is not None
