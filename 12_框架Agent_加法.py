"""Agentic RAG：用 create_agent 一键封装一个带检索工具的 Agent。

对比 13_画stategraph图.py 的手写状态图，这里用 LangChain 高层的 create_agent
自动完成"模型 -> 工具 -> 模型"的循环，只需传入模型、工具和系统提示即可。
"""
import os
from dotenv import load_dotenv  # 加载 .env 中的环境变量（API 密钥等）
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 递归字符切块器
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # 文本向量化模型 + 聊天模型
from langchain_core.vectorstores import InMemoryVectorStore  # 内存向量库
from langchain_core.tools import tool  # @tool 装饰器：把普通函数声明为工具
from langchain.agents import create_agent  # 高层封装：一键创建 Agent
from langgraph.checkpoint.sqlite import SqliteSaver  # 把对话状态存档到 SQLite 数据库
import dashscope
from http import HTTPStatus

load_dotenv()
with open("07_读写文件_学习笔记.md", "r", encoding="utf-8-sig") as f:
    text = f.read()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20,
    separators=["\n\n", "\n", "。", "，", " ", ""]
)
chunks = splitter.split_text(text)
embeddings = OpenAIEmbeddings(
    model="text-embedding-v4",
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["base_url1"],
    chunk_size=10,
    check_embedding_ctx_length=False
)
vectorstore = InMemoryVectorStore.from_texts(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


@tool
def add(a, b) -> int:
    """这是一个加法计算器，让用户需要加法计算的时候使用"""
    return a + b


@tool
def knowledge_search(query: str) -> str:
    """检索学习笔记资料，当问题需要依据文档回答时调用。"""
    documents = [doc.page_content for doc in retriever.invoke(query)]
    resp = dashscope.TextReRank.call(
        model="qwen3-rerank",
        documents=documents,
        top_n=3,
        query=query,
        return_documents=True
    )
    if resp.status_code != HTTPStatus.OK:
        return "检索失败，请稍后再试"
    else:
        ranked_texts = [doc["document"]["text"] for doc in resp.output.results]
        return "\n".join(ranked_texts)


tools = [add, knowledge_search]
model = ChatOpenAI(
    model="deepseek-flash",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"]
)
with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="需要查资料的时候就去查资料，资料里没有的就说不知道",
        checkpointer=checkpointer
    )
    config = {"configurable": {"thread_id": "user-2"}}

    while True:
        question = input("请输入：")
        if question == "退出":
            print("已退出")
            break
        else:
            answer = agent.invoke(
                {"messages": [{"role": "user", "content": question}]},
                config
            )
            print(answer["messages"][-1].content)
print()