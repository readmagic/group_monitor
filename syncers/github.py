#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 同步器
作者: Frandy
"""

import shutil
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Optional
from git import Repo, GitCommandError

from .base import BaseSyncer

logger = logging.getLogger(__name__)


class GitHubSyncer(BaseSyncer):
    """GitHub 同步器"""

    def __init__(self, repo_url: str, repo_dir: str = None):
        self.repo_url = repo_url
        self.repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        if repo_dir:
            self.repo_dir = Path(repo_dir)
        else:
            self.script_dir = Path(__file__).parent.parent.resolve()
            self.repo_dir = self.script_dir / self.repo_name
        self.repo = None

    def _ensure_repo(self) -> bool:
        """确保仓库存在"""
        try:
            if not self.repo_dir.exists():
                logger.info(f"首次运行，正在克隆仓库: {self.repo_url}")
                self.repo = Repo.clone_from(self.repo_url, self.repo_dir)
                logger.info(f"仓库已克隆到: {self.repo_dir}")
            else:
                # 检查是否是有效的 Git 仓库
                git_dir = self.repo_dir / ".git"
                if not git_dir.exists():
                    logger.warning(f"目录存在但不是 Git 仓库，正在克隆: {self.repo_dir}")
                    shutil.rmtree(self.repo_dir)
                    self.repo = Repo.clone_from(self.repo_url, self.repo_dir)
                    logger.info(f"仓库已克隆到: {self.repo_dir}")
                else:
                    self.repo = Repo(self.repo_dir)
                    logger.info("正在拉取最新代码...")
                    self.repo.remotes.origin.pull()
            return True
        except GitCommandError as e:
            logger.error(f"Git 操作失败: {e}")
            return False

    def ensure_repo_dir(self) -> Optional[str]:
        """确保仓库目录存在并返回路径"""
        if self._ensure_repo():
            return str(self.repo_dir)
        return None

    def commit_and_push(self, filename: str) -> bool:
        """提交并推送文件到 GitHub"""
        try:
            if not self.repo:
                self.repo = Repo(self.repo_dir)

            self.repo.index.add([filename])

            if not self.repo.index.diff("HEAD"):
                logger.info("没有新内容需要提交")
                return True

            yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
            commit_msg = f"添加 {yesterday} 群聊报告"
            self.repo.index.commit(commit_msg)
            logger.info(f"已提交: {commit_msg}")

            logger.info("正在推送到 GitHub...")
            self.repo.remotes.origin.push()
            logger.info("报告已成功同步到 GitHub")
            return True

        except GitCommandError as e:
            logger.error(f"Git 操作失败: {e}")
            return False
        except Exception as e:
            logger.error(f"同步到 GitHub 失败: {e}")
            return False

    def sync(self, report_path: str) -> bool:
        """将报告同步到 GitHub 仓库"""
        report_file = Path(report_path)
        if not report_file.exists():
            logger.error(f"报告文件不存在: {report_path}")
            return False

        try:
            if not self._ensure_repo():
                return False

            dest_path = self.repo_dir / report_file.name
            shutil.copy2(report_file, dest_path)
            logger.info(f"已复制报告到: {dest_path}")

            self.repo.index.add([report_file.name])

            if not self.repo.index.diff("HEAD"):
                logger.info("没有新内容需要提交")
                return True

            yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%Y-%m-%d")
            commit_msg = f"添加 {yesterday} 群聊报告"
            self.repo.index.commit(commit_msg)
            logger.info(f"已提交: {commit_msg}")

            logger.info("正在推送到 GitHub...")
            self.repo.remotes.origin.push()
            logger.info("报告已成功同步到 GitHub")
            return True

        except GitCommandError as e:
            logger.error(f"Git 操作失败: {e}")
            return False
        except Exception as e:
            logger.error(f"同步到 GitHub 失败: {e}")
            return False
