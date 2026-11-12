"""LangGraph 底层状态图：手写一个带工具调用的 Agent 图。

与 create_agent 的一键封装不同，这里手动搭建 StateGraph（状态图）的每个部件：
定义状态 -> 定义节点（模型节点 / 工具节点）-> 定义路由函数 -> 连接边 -> 编译运行。
执行流程：START -> model_call ->（模型要调工具就走 tool_node，否则结束）-> 回到 model_call。
"""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # 文本向量化模型 + 聊天模型
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 递归字符切块器
from langchain_core.vectorstores import InMemoryVectorStore  # 内存向量库
from langchain_core.tools import tool  # @tool 装饰器：把普通函数声明为可被模型调用的工具
from typing_extensions import TypedDict  # 定义带类型字段的字典
import operator  # 提供 operator.add，用于消息列表的合并（累加）
from typing import Literal, Annotated  # Literal 限定返回取值；Annotated 给字段附加合并规则
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, SystemMessage  # 四种消息类型
from langgraph.graph import StateGraph, START, END  # 状态图 + 起点/终点两个特殊标记
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
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


@tool
def add(a: int, b: int) -> int:
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
tools_by_name = {t.name: t for t in tools}  # 工具名 -> 工具对象 的字典，方便按名字查找工具
model = ChatOpenAI(
    model="deepseek-flash",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"]
)
model_with_tools = model.bind_tools(tools)  # 绑定工具：让模型知道它可以调用哪些工具


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]  # 消息列表，用 operator.add 累加合并


def model_call(state: MessagesState) -> MessagesState:
    """模型节点：把系统提示 + 历史消息发给模型，返回模型产生的下一条消息。"""
    answer = model_with_tools.invoke(
        [SystemMessage(content="你是一名科研助手，用户的问题需要查资料的时候去调用相关工具，资料里没有的就说不知道，不要瞎编")]
        + state["messages"]
    )
    return {"messages": [answer]}


def tool_node(state: MessagesState) -> MessagesState:
    """工具节点：执行模型请求的每一个工具调用，并把结果包装成 ToolMessage 返回。"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        f = tools_by_name[tool_call["name"]]
        result.append(ToolMessage(content=str(f.invoke(tool_call["args"])), tool_call_id=tool_call["id"]))
    return {"messages": result}


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """路由函数：如果模型最后一条消息里有工具调用，就转去工具节点，否则结束。"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    else:
        return END


builder = StateGraph(MessagesState)
builder.add_node("model_call", model_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "model_call")
builder.add_conditional_edges("model_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "model_call")
with SqliteSaver.from_conn_string("checkpoints.sqlite") as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "user-1"}}

    while True:
        question = input("请输入（输入 quit 退出）：")
        if question == "quit":
            break
        result = graph.invoke(
            {"messages": [HumanMessage(content=question)]},
            config
        )
        print(result["messages"][-1].content)
print()