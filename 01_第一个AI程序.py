"""第一个 AI 程序：调用 DeepSeek 大模型回答一句话。"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# 从 .env 文件中加载环境变量（密钥存在 .env 里，安全不暴露）
load_dotenv()

# 1. 创建客户端：api_key 是密码，base_url 是 DeepSeek 的服务地址
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url=os.environ["base_url"],
)

# 2. 发起一次对话：model 选模型，messages 是对话内容
#    role="user" 表示这是“用户”说的话；system 可用来设定 AI 的身份
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": ""},
        {"role": "user", "content": "你是一位地理老师，你要给我讲两地的距离。回答的格式为：大概多少km。请说明采用哪种距离；如果无法核实准确数值，请标明是估算，不要把估算写成精确值。请你回答：从北京到上海大概多少km？"},
    ],
)
# 3. 取出并打印 AI 的回答
answer = response.choices[0].message.content
print("AI 的回答：")
print(answer)