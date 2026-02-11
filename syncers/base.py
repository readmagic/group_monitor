#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步器基类
作者: Frandy
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseSyncer(ABC):
    """同步器基类"""

    @abstractmethod
    def ensure_repo_dir(self) -> Optional[str]:
        """
        确保仓库目录存在

        Returns:
            仓库目录路径，失败返回 None
        """
        pass

    @abstractmethod
    def commit_and_push(self, filename: str) -> bool:
        """
        提交并推送文件

        Args:
            filename: 文件名

        Returns:
            是否成功
        """
        pass

    @abstractmethod
    def sync(self, report_path: str) -> bool:
        """
        同步报告文件

        Args:
            report_path: 报告文件路径

        Returns:
            是否成功
        """
        pass
