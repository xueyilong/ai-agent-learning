"""第四块（三档版）：列表与字典 —— 装数据的两种容器。

岗位对应：RAG 切分后的文本块、检索结果、模型返回的信息，全用列表/字典装。
过关标准：全部真实运行通过，能讲清每行作用。
"""

# ========== 基础档（必做，15 分钟） ==========

# 列表：一排有序盒子，用 [] 装，内容可增删，位置从 0 开始数
stations = ["南昌", "吉安", "赣州", "东莞"]
print(stations[0])        # 取第 1 个：南昌
print(stations[-1])       # 取最后一个：东莞

stations.append("深圳")   # 末尾加一个
print(stations)
print("一共几站：", len(stations))

# ========== 进阶档（必做，25 分钟） ==========

# 遍历 + 配合判断：从列表里挑出符合条件的
prices = [320, 150, 80, 460, 200]
cheap = []
for p in prices:
    if p <= 200:
        cheap.append(p)
print("200 元以内的票价：", cheap)

# 切片：取列表的一段，含头不含尾
print(prices[1:3])        # 第 2、3 个：[150, 80]

# 字典：带标签的盒子，用 {} 装，成对存“键: 值”
ticket = {
    "出发": "南昌",
    "到达": "东莞",
    "票价": 320,
}
print(ticket["出发"])     # 按键取值
ticket["折扣"] = 0.8      # 新增一对
print(ticket)

# ========== 贴近岗位档（选做，Agent 味） ==========

# 场景1：RAG 切分后，文本块就是一个“字符串列表”
chunks = ["第一条：列车开行规则", "第二条：票价计算办法", "第三条：退票规定"]
for i, chunk in enumerate(chunks):
    print(f"第{i + 1}块 → {chunk}")

# 场景2：模型一次调用返回的信息，用字典装最常见（真实结构长这样）
result = {
    "answer": "南昌到东莞票价约320元",
    "source": "票价计算办法",
    "confidence": 0.86,
    "used_tool": "票价查询",
}
print("回答：", result["answer"])
print("出处：", result["source"], " 置信度：", result["confidence"])

# 场景3：列表里装多个字典（多条检索结果，最贴近真实）
docs = [
    {"title": "开行规则", "score": 0.91},
    {"title": "票价办法", "score": 0.85},
    {"title": "退票规定", "score": 0.72},
]
for doc in docs:
    print(f"{doc['title']}（相关度 {doc['score']}）")

# ========== 过关标准 ==========
# 基础档：取数、append、len；进阶档：筛出 [150,80,200]、字典取值；岗位档：能看懂列表套字典