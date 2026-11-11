"""多轮对话小程序：带历史记录的 AI 聊天助手（贾维斯）。

核心点：把每一轮对话都追加进 messages 列表，并保存到 JSON 文件，
下次启动时恢复历史，从而实现"上下文记忆"。
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 创建客户端：api_key 是密钥，base_url 是 DeepSeek 服务地址
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"]
)

HISTORY_FILE1 = "chat_history.json"  # 保存对话历史的文件名

# 首次启动：若历史文件已存在则读入，否则用默认 system 消息开启对话
if os.path.exists(HISTORY_FILE1):
    with open(HISTORY_FILE1, "r", encoding="utf-8") as f:
        messages = json.load(f)  # 从 JSON 文件恢复历史对话
    print("已加载上次对话记录")
else:
    messages = [{"role": "system", "content": "你叫贾维斯,遇到不确定的事情就说不知道"}]

# 循环对话：直到用户输入"退出"
while True:
    questions = input("用户输入：")
    if questions == "退出":
        print("本次对话已结束")
        break
    else:
        # 把用户消息追加进历史，再一起发给模型
        messages.append({"role": "user", "content": questions})
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            temperature=0.7  # 温度参数：控制回答的随机性（0~1，越高越随机）
        )
        answer = response.choices[0].message.content
        # 把 AI 回答也追加进历史，并写回文件保存
        messages.append({"role": "assistant", "content": answer})
        with open(HISTORY_FILE1, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        print(f"回答：{answer}")