import os  # 操作系统接口：用于读取环境变量
from langchain_openai import ChatOpenAI  # OpenAI 兼容的聊天模型客户端
from langchain_openai import OpenAIEmbeddings  # OpenAI 兼容的文本向量化（Embedding）客户端
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 递归字符切分器：将长文本切分为小块
from langchain_core.vectorstores import InMemoryVectorStore  # 内存向量数据库：存储与检索文本向量
from langchain_core.prompts import ChatPromptTemplate  # 聊天提示词模板
from langchain_core.output_parsers import StrOutputParser  # 字符串输出解析器：将模型输出转为纯文本
from langchain_core.runnables import RunnableLambda, RunnablePassthrough  # LCEL 运行组件：包装普通函数 / 透传输入
from dotenv import load_dotenv  # 从 .env 文件加载环境变量
import datetime  # 日期时间处理
import dashscope  # 阿里云百炼 SDK：提供文本重排序（Rerank）服务
from http import HTTPStatus  # HTTP 状态码枚举：用于判断 API 请求是否成功

load_dotenv()  # 加载 .env 文件中的环境变量（API 密钥等）
dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]  # 手动注入百炼密钥（import 时环境变量尚未加载）


def calculator(a, b, op):
    """四则运算计算器，支持 +、-、*、/ 四种运算。"""
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return "错误"
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "分母不能等于0"
        else:
            return a/b
    else:
        return "运算符错误"


def get_current_time():
    """返回当前日期时间，格式为 %Y-%m-%d, %H-%M-%S。"""
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d, %H-%M-%S")


def convert_temperature(c, unit):
    """温度单位转换：c 为摄氏度，unit 为 "F"（华氏度）或 "K"（开尔文）。"""
    if unit == "F":
        return c * 9 / 5 + 32
    elif unit == "K":
        return c + 273.15
    else:
        return f"不支持的单位：{unit}"


def get_station_flow(station):
    """查询地铁站客流，数据来源为内置字典 {"八一广场": 150, "南昌西站": 80}。"""
    resource = {"八一广场": 150, "南昌西站": 80}
    traffic = resource[station]
    return traffic


def judge_crowding(flow):
    """根据客流判断拥挤程度：达到 120 视为拥挤，否则视为正常。"""
    if flow >= 120:
        return "拥挤"
    else:
        return "正常"


embeddings = OpenAIEmbeddings(  # 初始化文本向量化客户端
    model="text-embedding-v4",
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["base_url1"],
    check_embedding_ctx_length=False,  # 关闭输入长度检查
    chunk_size=10  # 每批处理的文本块数量
)

with open("05_列表与字典_学习笔记.md", "r", encoding="utf-8-sig") as f:  # 读取学习笔记文件
    content = f.read()
splitter = RecursiveCharacterTextSplitter(  # 初始化文本切分器
    chunk_size=100,  # 每块最大 100 字符
    chunk_overlap=20,  # 相邻块重叠 20 字符，防止语义被切断
    separators=["\n\n", "\n", "。", "，", " ", ""]  # 切分分隔符（按优先级从高到低）
)
chunks = splitter.split_text(content)  # 将全文切分为文本块列表
vectorstore = InMemoryVectorStore.from_texts(chunks, embeddings)  # 将文本块向量化并存入内存向量库
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})  # 创建检索器，每次返回最相关的 10 个块


def knowledge_search(query: str) -> str:
    """检索学习笔记资料：先向量召回候选文档，再调用重排序模型精排，返回最相关的文本。"""
    documents = [doc.page_content for doc in retriever.invoke(query)]  # 第一步：向量召回候选文档
    resp = dashscope.TextReRank.call(  # 第二步：调用重排序模型进行精排
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


question = input("请输入：")  # 读取用户输入的问题
prompt = ChatPromptTemplate.from_messages([  # 构建聊天提示词模板
    ("system", "当需要查资料时，按照资料内容回答问题，资料里没有就说不知道、不允许编造。"),
    ("human", "资料：{context}\n\n问题：{question}")
])

response = ChatOpenAI(  # 初始化聊天模型客户端
    model="deepseek-flash",
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"]
)

parser = StrOutputParser()  # 初始化字符串输出解析器

rag_chain = (  # 构建 RAG 链：检索 -> 拼接提示词 -> 模型生成 -> 解析输出
    {"context": RunnableLambda(knowledge_search), "question": RunnablePassthrough()}
    | prompt
    | response
     | StrOutputParser())

answer = rag_chain.invoke(question)  # 执行 RAG 链，生成答案
print(answer)  # 输出答案