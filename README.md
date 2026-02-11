# 微信群信息监控程序

一个用于监控微信群聊消息并生成智能总结报告的 Python 程序。

## 项目背景

快要到春节了，生活中事情太多太忙，没有时间看群里的精华消息。一层层爬楼又太慢，错过了很多有价值的讨论。

另外，最近想体验一下 Vibe Coding（氛围编程），所以这个项目全程不手写代码，完全通过 AI 对话式生成。从需求分析、架构设计到代码实现，全部由 AI 完成，我只负责提需求和验收。

看来效果还不错，AI 不仅能理解需求，还能主动优化代码结构、添加测试用例、处理边界情况。这种人机协作的编程方式，确实能大幅提升开发效率。

## 平台要求

**仅支持 Windows 系统**

## 功能特性

- 自动获取昨天一整天的微信群聊消息
- 使用阿里云 DashScope 大模型进行对话总结
- 生成结构化的 Markdown 报告
- 自动同步报告到 GitHub 仓库

## 前置条件

### 1. 安装 WeChatDataAnalysis

需要先安装 [WeChatDataAnalysis](https://github.com/LifeArchiveProject/WeChatDataAnalysis) 软件：

1. 访问 https://github.com/LifeArchiveProject/WeChatDataAnalysis
2. 下载并安装软件
3. 使用微信号登录
4. 软件会自动收集聊天消息并启动本地服务（默认端口 8000）

### 2. 获取配置信息

#### ACCOUNT（微信账号 ID）

在以下目录查找：
```
C:\Users\<用户名>\Documents\xwechat_files
```

目录名格式为 `wxid_xxxxxx_yyyy`，其中 `wxid_xxxxxx` 就是你的 ACCOUNT。

例如：目录名为 `wxid_629q9owg921w22_files`，则 ACCOUNT 为 `wxid_629q9owg921w22`

#### TALKER_ID（聊天 ID）

通过 WeChatDataAnalysis 软件界面获取：
- 个人聊天：对方的微信 ID
- 群聊：群 ID，格式为 `数字@chatroom`，例如 `53725032966@chatroom`

## 环境要求

- Windows 10/11
- Python 3.8+
- Git（用于同步到 GitHub）

## 安装步骤

1. 克隆项目：
```bash
git clone https://github.com/readmagic/group_monitor.git
cd group_monitor
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

主要依赖：
- `requests` - HTTP 请求
- `GitPython` - Git 操作

3. 创建配置文件：
```bash
copy .env.example .env
```

4. 编辑 `.env` 文件，填入实际配置

## 配置说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| API_BASE_URL | WeChatDataAnalysis 服务地址 | http://localhost:8000 |
| ACCOUNT | 微信账号 ID | wxid_669q9owg921w22 |
| TALKER_ID | 监控的聊天 ID | 53725032966@chatroom |
| DASHSCOPE_API_KEY | 阿里云 DashScope API 密钥 | sk-xxxxxxxx |
| OUTPUT_DIR | 报告输出目录 | reports |
| GITHUB_REPO | GitHub 仓库地址（可选） | https://github.com/user/repo |
| GITHUB_REPO_DIR | 本地仓库目录（可选） | D:\reports |

### 配置示例

```ini
# 消息 API 配置
API_BASE_URL=http://localhost:8000
ACCOUNT=wxid_629q9owg921w22
TALKER_ID=53725032966@chatroom

# DashScope API 配置
DASHSCOPE_API_KEY=sk-your-api-key

# 输出配置
OUTPUT_DIR=reports

# GitHub 仓库配置（可选）
GITHUB_REPO=https://github.com/readmagic/shengsheng_group_disscus
GITHUB_REPO_DIR=D:\shengsheng_group_disscus
```

## 使用方法

确保 WeChatDataAnalysis 软件正在运行，然后执行：

```bash
python main.py
```

程序会：
1. 获取昨天的群聊消息
2. 调用 AI 生成总结
3. 生成 Markdown 报告
4. 同步到 GitHub（如果配置了）

### 定时任务（可选）

如果需要每天自动执行，可以使用以下方式：

#### 方式一：Python 调度器

```bash
python scheduler.py
```

程序会每天凌晨 1 点自动执行监控任务。保持命令行窗口运行即可。

#### 方式二：Windows 任务计划程序

1. 打开"任务计划程序"（按 `Win + R`，输入 `taskschd.msc`）
2. 点击右侧"创建基本任务"
3. 名称：`微信群监控`，点击"下一步"
4. 触发器：选择"每天"，开始时间设为 `01:00:00`
5. 操作：选择"启动程序"
   - 程序或脚本：`python`
   - 添加参数：`main.py` 的完整路径，如 `C:\group_monitor\main.py`
   - 起始于：项目目录，如 `C:\group_monitor`
6. 完成创建

## 项目结构

```
groupMonitor_client/
├── main.py              # 主程序入口
├── scheduler.py         # 定时任务调度器（可选）
├── config.py            # 配置加载模块
├── chat_fetcher.py      # 消息获取模块
├── summarizers/         # AI 摘要器包
│   ├── base.py          # 基类
│   ├── dashscope.py     # DashScope 实现
│   └── prompts.py       # 提示词常量
├── syncers/             # 同步器包
│   ├── base.py          # 基类
│   └── github.py        # GitHub 同步实现
├── tests/               # 测试用例
├── requirements.txt     # 依赖列表
├── .env.example         # 配置示例
└── .env                 # 实际配置（需自行创建）
```

## API 参考

### WeChatDataAnalysis API

- 端点：`/api/chat/messages`
- 参数：
  - `account`: 微信账号 ID
  - `username`: 聊天 ID
  - `limit`: 每页数量
  - `offset`: 偏移量
  - `order`: 排序方式（asc/desc）
  - `render_types`: 消息类型（text）

### DashScope API

- 官方文档：https://help.aliyun.com/zh/dashscope/
- 模型：qwen3-235b-a22b-instruct-2507
- 功能：流式文本生成和对话总结

## 注意事项

1. 确保 WeChatDataAnalysis 软件正在运行且已登录微信
2. DashScope API Key 需要有足够的调用额度
3. 首次运行会自动克隆 GitHub 仓库（如果配置了）
4. 报告文件名格式：`群聊报告_YYYYMMDD.md`

## 作者

Frandy

## 许可证

MIT
