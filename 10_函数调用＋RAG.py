"""函数调用 + RAG：手写 OpenAI 的 function calling（函数调用）完整流程。

本文件手动实现"模型决定调用哪个工具 -> 本地执行工具 -> 把结果回填 -> 再让模型生成最终回答"
的完整闭环，并接入一个基于余弦相似度的简易 RAG 检索。
对比 12/13 用 LangChain 的高层封装，这里展示的是底层原理。
"""
import os
import json
from openai import OpenAI
import dotenv
import datetime
import math
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 递归字符切块器

dotenv.load_dotenv()

# 向量化客户端（走阿里云百炼，用于把文本转成向量）
embedding_client = OpenAI(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    base_url=os.environ["base_url1"]
)
# 聊天客户端（走 DeepSeek，用于对话）
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"]
)


def calculator(a, b, op):
    """四则运算计算器：op 为 "+"/"-"/"*"/"/"，除数为 0 时返回提示而非报错。"""
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
            return a / b
    else:
        return "运算符错误"


def get_current_time():
    """返回当前时间，格式为 %Y-%m-%d, %H-%M-%S。"""
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d, %H-%M-%S")


def convert_temperature(c, unit):
    """温度转换：c 为摄氏度；unit 为 "F" 转华氏度，为 "K" 转开尔文。"""
    if unit == "F":
        return c * 9 / 5 + 32
    elif unit == "K":
        return c + 273.15
    else:
        return f"不支持的单位：{unit}"


def get_station_flow(station):
    """从固定字典查询某站点客流。"""
    resource = {"八一广场": 150, "南昌西站": 80}
    traffic = resource[station]
    return traffic


def judge_crowding(flow):
    """判断拥挤程度：客流 >= 120 返回"拥挤"，否则返回"正常"。"""
    if flow >= 120:
        return "拥挤"
    else:
        return "正常"


with open("学习小结.txt", "r", encoding="utf-8-sig") as f:
    content = f.read()


def chunk_by_length_embedding(text, chunk_size):
    """把文本按 chunk_size 切块，再分批调用 embedding 接口转成向量。"""
    batch_size = 10
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=20,
        separators=["\n\n", "\n", "。", "，", " ", ""]
    )
    ch = splitter.split_text(text)
    chunks_vectors = []
    for i in range(0, len(ch), batch_size):
        batch = ch[i:i + batch_size]  # 每次取一个批次的文本块
        res = embedding_client.embeddings.create(
            model="text-embedding-v4",
            input=batch
        )
        for item in res.data:
            chunks_vectors.append(item.embedding)
    return chunks_vectors, ch


chunk_vectors, chunks = chunk_by_length_embedding(content, 100)


def questions_embedding(question):
    """把用户问题转成向量，返回向量列表。"""
    res = embedding_client.embeddings.create(
        model="text-embedding-v4",
        input=question
    )

    question_vectors = []
    for item in res.data:
        question_vectors.append(item.embedding)
    return question_vectors


def cosine_search(question_vector, chunks_vectors, c, k=3):
    """余弦相似度检索：计算问题向量与每个块向量的相似度，返回最相似的前 k 个。"""
    results = []
    total1 = 0
    for x in question_vector[0]:
        total1 += x * x  # 问题向量的模平方（用于计算余弦相似度的分母）
    for i in range(len(c)):
        total2 = 0
        total3 = 0
        for x, y in zip(question_vector[0], chunks_vectors[i]):
            total2 += y * y  # 块向量的模平方
            total3 += x * y  # 两个向量的点积
        if total1 == 0 or total2 == 0:
            sim = 0
        else:
            sim = total3 / (math.sqrt(total2) * math.sqrt(total1))  # 余弦相似度公式
        results.append((sim, c[i]))
    results.sort(reverse=True)  # 按相似度从高到低排序
    return results[:k]  # 只返回最相似的前 k 个


def knowledge_search(question):
    """RAG 检索：问题向量化 -> 余弦相似度检索 -> 拼接检索到的文本块返回。"""
    # 1. 问题向量化
    question_vectors = questions_embedding(question)
    # 2. 用余弦相似度检索最相关的文本块
    top_k = cosine_search(question_vectors, chunk_vectors, chunks)
    # 3. 把检索到的块拼成一段资料文本返回
    context_text = ""
    for sim, chunk_text in top_k:
        context_text = context_text + chunk_text + "\n"
    return context_text


# 工具清单：告诉模型有哪些工具可用，以及每个工具的参数格式（JSON Schema）
tools = [{
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "这是一个计算器，进行加减乘除四则运算，当用户需要数学运算时候使用",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "第一个数字"},
                "b": {"type": "number", "description": "第二个数字"},
                "op": {
                    "type": "string",
                    "description": "运算符",
                    "enum": ["+", "-", "*", "/"]
                }
            },
            "required": ["a", "b", "op"]
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "这是一个用来查询实施时间的工具",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "convert_temperature",
        "description": "这是一个温度转换器，可以将摄氏度转换为华氏度或者开尔文",
        "parameters": {
            "type": "object",
            "properties": {
                "c": {"type": "number", "description": "摄氏度的数值"},
                "unit": {
                    "type": "string",
                    "description": "华氏度和开尔文的单位",
                    "enum": ["F", "K"]
                }
            },
            "required": ["c", "unit"]
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "knowledge_search",
        "description": "当用户的问题需要查阅学习资料/知识库才能回答时调用",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "用户的问题"},
            },
            "required": ["question"]
        }
    }
}]


HISTORY_FILES = "chat_history_stream2.json"  # 保存对话历史的文件名

# 首次启动：有历史文件且非空就恢复，否则用默认 system 消息开启对话
if os.path.exists(HISTORY_FILES):
    with open(HISTORY_FILES, "r", encoding="utf-8") as f:
        content = f.read()
        if content.strip():
            messages = json.loads(content)
        else:
            messages = [{"role": "system", "content": "你是问答助手。当工具返回资料时，只能依据资料回答；资料里没有的内容就就自己说。"}]
else:
    messages = [{"role": "system", "content": "你是问答助手。当工具返回资料时，只能依据资料回答；资料里没有的内容就自己说。"}]

while True:
    questions = input("请输入：")
    if questions == "退出":
        print("已退出")
        break
    else:
        messages.append({"role": "user", "content": questions})
        # 带着工具清单请求模型，模型会决定是否需要调用工具
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=tools
        )
        answer = response.choices[0].message
        print(answer)
        if not answer.tool_calls:
            # 模型没调用工具：直接输出回答
            print(answer.content)
            print("（本次未调用工具）")
            messages.append(answer.model_dump(include={"role", "content"}))
        else:
            # 模型要调用工具：先保存这条带工具调用的消息，再本地执行工具
            messages.append(answer.model_dump(exclude_none=True))
            if answer.tool_calls:
                toll_call = answer.tool_calls[0]  # 取第一个工具调用
                args = json.loads(toll_call.function.arguments)  # 解析模型给出的参数 JSON
                if toll_call.function.name == "calculator":
                    result = calculator(args["a"], args["b"], args["op"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": toll_call.id,
                        "content": str(result)
                    }
                    )
                elif toll_call.function.name == "get_current_time":
                    result = get_current_time()
                    messages.append({
                        "role": "tool",
                        "tool_call_id": toll_call.id,
                        "content": str(result)
                    }
                    )
                elif toll_call.function.name == "convert_temperature":
                    result = convert_temperature(args["c"], args["unit"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": toll_call.id,
                        "content": str(result)
                    })
                elif toll_call.function.name == "knowledge_search":
                    result = knowledge_search(args["question"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": toll_call.id,
                        "content": str(result)
                    }
                    )
            # 工具结果回填后，再次请求模型生成最终回答（流式输出）
            final = client.chat.completions.create(
                model="deepseek-flash",
                messages=messages,
                stream=True,
            )
            final_answer = ""
            for chunk in final:
                delta = chunk.choices[0].delta
                if delta.content:
                    final_answer += delta.content
            print(final_answer, end="", flush=True)
            messages.append({"role": "assistant", "content": final_answer})
        with open(HISTORY_FILES, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print()