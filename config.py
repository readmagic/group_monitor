#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载模块
作者: Frandy
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """配置类"""

    def __init__(self, env_file: Optional[str] = None):
        """
        初始化配置

        Args:
            env_file: .env 文件路径
        """
        if env_file:
            self.load_env_file(env_file)

    @staticmethod
    def load_env_file(env_file: str):
        """加载 .env 文件"""
        env_path = Path(env_file)
        if not env_path.exists():
            return

        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

    @property
    def api_base_url(self) -> str:
        """获取 API 基础地址"""
        return os.getenv('API_BASE_URL')

    @property
    def account(self) -> str:
        """获取微信账号ID"""
        return os.getenv('ACCOUNT')

    @property
    def talker_id(self) -> str:
        """获取群聊 ID"""
        return os.getenv('TALKER_ID')

    @property
    def dashscope_api_key(self) -> str:
        """获取 DashScope API Key"""
        return os.getenv('DASHSCOPE_API_KEY')

    @property
    def output_dir(self) -> str:
        """获取输出目录"""
        return os.getenv('OUTPUT_DIR', 'reports')

    @property
    def github_repo(self) -> str:
        """获取 GitHub 仓库地址"""
        return os.getenv('GITHUB_REPO')

    @property
    def github_repo_dir(self) -> str:
        """获取 GitHub 仓库本地目录"""
        return os.getenv('GITHUB_REPO_DIR')
