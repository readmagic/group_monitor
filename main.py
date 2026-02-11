#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信群聊监控主程序
作者: Frandy
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path

from config import Config
from chat_fetcher import ChatFetcher
from summarizers import DashScopeSummarizer
from syncers import GitHubSyncer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_report(messages: list, summary: str, output_path: str) -> bool:
    """生成 Markdown 报告"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        markdown_content = f"""# 微信群聊监控报告

**生成时间**: {timestamp}
**消息数量**: {len(messages)} 条

---

## 对话总结

{summary}
"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown_content, encoding='utf-8')
        logger.info(f"报告已生成: {output_path}")
        return True
    except Exception as e:
        logger.error(f"生成报告失败: {e}")
        return False


def main():
    """主函数"""
    config = Config('.env')

    if not config.dashscope_api_key:
        logger.error("请在 .env 文件中配置 DASHSCOPE_API_KEY")
        return

    # 1. 获取群聊消息
    fetcher = ChatFetcher(config.api_base_url, config.account)
    yesterday_messages = fetcher.fetch_yesterday_messages(config.talker_id)
    if not yesterday_messages:
        logger.warning("没有找到昨天的消息")
        return

    filtered_messages = fetcher.filter_user_messages(yesterday_messages)
    if not filtered_messages:
        logger.warning("没有找到用户消息")
        return

    # 2. AI 总结
    summarizer = DashScopeSummarizer(config.dashscope_api_key)
    summary = summarizer.summarize(filtered_messages)
    if not summary:
        logger.warning("总结失败，将使用默认提示")
        summary = "总结生成失败，请检查 DashScope API 配置。"

    # 3. 确定报告输出路径
    yesterday = (datetime.now().date() - timedelta(days=1)).strftime("%Y%m%d")
    report_filename = f"群聊报告_{yesterday}.md"

    # 4. 同步到 GitHub（先确保仓库存在，报告直接生成到仓库目录）
    if config.github_repo:
        syncer = GitHubSyncer(config.github_repo, config.github_repo_dir)
        repo_dir = syncer.ensure_repo_dir()
        if repo_dir:
            output_path = f"{repo_dir}/{report_filename}"
        else:
            output_path = f"reports/{report_filename}"
    else:
        output_path = f"reports/{report_filename}"

    if not generate_report(filtered_messages, summary, output_path):
        return

    # 5. 提交并推送到 GitHub
    if config.github_repo and syncer:
        syncer.commit_and_push(report_filename)

    logger.info("监控任务完成")


if __name__ == "__main__":
    main()
