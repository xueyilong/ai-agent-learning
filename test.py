import os
import sqlite3
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.tools import tool
from typing_extensions import TypedDict
from typing import Annotated, Literal
import operator
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from http import HTTPStatus
import dashscope
from langgraph.checkpoint.sqlite import SqliteSaver
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.sse import EventSourceResponse, ServerSentEvent
load_dotenv()
app = FastAPI(title="第一个agent接口")

with open("01_第一个AI程序_学习笔记.md", "r", encoding="utf-8-sig") as f:
    content = f.read()
splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", "，", " ", ""]
    )
chunks = splitter.split_text(content)
embeddings = OpenAIEmbeddings(
    model="text-embedding-v4",
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["base_url1"],
    check_embedding_ctx_length=False,
    chunk_size=10
)
vectorstore = InMemoryVectorStore.from_texts(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})


@tool
def add(a: int, b: int) -> int:
    """这是一个加法计算式，让用户问加法相关问题时调用"""
    return a + b


@tool
def search_knowledge(query: str) -> str:
    """这是检索器，当用户需要查资料的时候调用"""
    documents = [doc.page_content for doc in retriever.invoke(query)]
    rep = dashscope.TextReRank.call(
        model="qwen3-rerank",
        query=query,
        documents=documents,
        top_n=3,
        return_documents=True
    )
    if rep.status_code != HTTPStatus.OK:
        return "网络错误，请重试！"
    else:
        rerank_text = [doc["message"]["text"] for doc in rep.output.results]
        return "\n".join(rerank_text)


tools = [add, search_knowledge]
tools_by_name = {t.name: t for t in tools}
model = ChatOpenAI(
    model="deepseek-flash",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"]
)
model_with_tool = model.bind_tools(tools)


class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


def model_call(state: MessagesState) -> MessagesState:
    answer = model_with_tool.invoke(
        [SystemMessage(content="你是一名科研助手，用户的问题需要查资料的时候去调用相关工具，资料里没有的就说不知道，不要瞎编")]
        + state["messages"]
    )
    return {"messages": [answer]}


def tool_node(state: MessagesState) -> MessagesState:
    results = []
    for tool_call in state["messages"][-1].tool_calls:
        t = tools_by_name[tool_call["name"]]
        results.append(ToolMessage(content=str(t.invoke(tool_call["args"])), tool_call_id=tool_call["id"]))
    return {"messages": results}


def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    last_message = state["messages"][-1].tool_calls
    if last_message:
        return "tool_node"
    else:
        return END


builder = StateGraph(MessagesState)
builder.add_node("model_call", model_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "model_call")
builder.add_conditional_edges("model_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "model_call")
connect = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
checkpointer = SqliteSaver(connect)
graph = builder.compile(checkpointer=checkpointer)


class QuestionQuest(BaseModel):
    question: str
    thread_id: str = "user-1"


@app.post("/agent")
def chat(message: QuestionQuest):
    if not message.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")
    config = {"configurable": {"thread_id": message.thread_id}}
    try:
        results = graph.invoke(
            {"messages": [HumanMessage(content=message.question)]},
            config
        )
    except Exception:
        raise HTTPException(status_code=500, detail="服务处理失败，请稍后再试")
    return results["messages"][-1].content


@app.post("/agent/stream", response_class=EventSourceResponse)
def stream_chat(message: QuestionQuest):
    if not message.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")
    config = {"configurable": {"thread_id": message.thread_id}}
    inputs = {"messages": [HumanMessage(content=message.question)]}
    try:
        for msg_chunk, metadata in graph.stream(
            inputs, config=config, stream_mode="messages"
        ):
            if msg_chunk.content:
                yield ServerSentEvent(data=msg_chunk.content)
        yield ServerSentEvent(raw_data="[DONE]", event="done")
    except Exception:
        yield ServerSentEvent(raw_data="服务处理失败，请稍后再试", event="error")



