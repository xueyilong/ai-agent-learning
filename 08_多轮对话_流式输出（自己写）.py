"""多轮对话 + 流式输出：让 AI 像打字一样逐字输出回答。

关键点：
1. stream=True 开启流式返回，响应是一段一段来的；
2. 每收到一段就立刻打印，实现"边生成边显示"；
3. 对话历史同样保存到 JSON 文件，实现上下文记忆。
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"],
)

HISTORY_FILE2 = "chat_history_stream.json"  # 保存对话历史的文件名

# 首次启动：有历史文件就恢复，否则用默认 system 消息开启对话
if os.path.exists(HISTORY_FILE2):
    with open(HISTORY_FILE2, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = [{"role": "system", "content": "你是一名英雄联盟解说"}]

while True:
    questions = input("请输入：")
    if questions == "退出":
        print("对话已结束")
        break
    else:
        messages.append({"role": "user", "content": questions})
        # stream=True：开启流式返回
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            stream=True
        )
        answer = ""
        print("回答：", end="", flush=True)  # end="" 不换行；flush=True 立即刷新到屏幕
        # 逐段接收增量内容，边收边打印
        for chunk in response:
            delta = chunk.choices[0].delta
            if delta.content:
                answer += delta.content
                print(delta.content, end="", flush=True)
        messages.append({"role": "assistant", "content": answer})
        with open(HISTORY_FILE2, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print()