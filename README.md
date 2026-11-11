# 从零自学 AI Agent 开发

零基础系统学习大模型应用开发的完整过程：从 Python 基础、模型 API 调用，到 Function Calling、RAG 全流程，再到 LangChain / LangGraph 框架底层与可观测性。每个阶段都包含可运行代码、手写实现和学习笔记。

## 学习背景

- 起点：零编程基础，自学 AI Agent 开发，目标求职 AI 应用开发实习；
- 方式：按阶段推进，每个模块真实运行、手写实现，并能讲清每一行原理；
- 模型：对话使用 DeepSeek，向量化与重排使用阿里云 DashScope。

## 学习路线

0. 工具就位
1. Python 基础
2. 模型基础与 API
3. Agent 工具调用（Function Calling）
4. RAG 全流程
5. 主流框架 LangChain / LangGraph（当前阶段）
6. FastAPI 与 Docker 部署
7. 评估、测试、文档、SQL
8. 交通问答 Agent 项目与投递

## 技术栈

| 类别 | 技术 |
|---|---|
| 语言 | Python |
| 对话模型 | DeepSeek（deepseek-flash） |
| 向量化 | DashScope text-embedding-v4 |
| 重排模型 | qwen3-rerank |
| 应用框架 | LangChain v1（LCEL、create_agent） |
| 底层编排 | LangGraph（StateGraph、节点、条件边） |
| 向量库 | InMemoryVectorStore |
| 持久化记忆 | SqliteSaver |
| 可观测性 | LangSmith |

## 目录结构与阶段说明

| 文件 | 内容 |
|---|---|
| 01–07 | Python 基础与第一个 AI 程序：变量、条件、循环、列表字典、函数、读写文件 |
| 08 | 多轮对话与流式输出 |
| 09 | 工具调用（Function Calling） |
| 10 | 手写 Function Calling + RAG 整合（架构 A） |
| 11 | LCEL 固定 RAG、文档切分与向量化 |
| 12 | create_agent 应用层：加法工具 + Agentic RAG |
| 13 | LangGraph StateGraph 手写图：节点、条件路由、持久化记忆、重排 |
| *_学习笔记.md | 每个阶段的详细学习笔记 |
| AI学习总纲.md | 整体知识框架 |

## 核心知识点

### RAG 全流程
文档加载 → 递归切分（RecursiveCharacterTextSplitter）→ Embedding 向量化 → 向量检索 → 重排精排 → 拼提示词 → 生成答案，并通过系统消息约束防幻觉。

### 两阶段检索
- 召回：向量检索快速扩大候选（粗筛，快但粗）；
- 精排：qwen3-rerank 交叉编码器对候选重新打分（准但慢），取 Top N。

### LangGraph 底层
状态（State）在节点间传递，节点处理数据，固定边与条件边决定流向，条件边由路由函数返回值决定，从而形成"模型 → 工具 → 模型"的循环。

## 如何运行

1. 安装依赖：
   `pip install -r requirements.txt`

2. 在根目录创建 `.env` 文件，配置以下环境变量（填入你自己的密钥）：

```

DASHSCOPE_API_KEY = 你的 DashScope 密钥
DEEPSEEK_API_KEY = 你的 DeepSeek 密钥
base_url=DeepSeek 接口地址
base_url1=DashScope 接口地址
LANGSMITH_TRACING=true
LANGSMITH_API_KEY = 你的 LangSmith 密钥
LANGSMITH_PROJECT = 你的项目名

```

3. 直接运行对应脚本，例如：
   `python 13_画stategraph图.py`

## 说明

- `.env` 已通过 .gitignore 排除，不会提交任何真实密钥；
- 数据库文件、虚拟环境、运行产物均已忽略；
- 本仓库为学习过程记录，后续会在此基础上构建完整的交通问答 Agent 项目。