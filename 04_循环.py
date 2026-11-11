"""第三块（三档版）：循环 —— 让程序重复干活。

岗位对应：批量处理文档、逐条切分、重试 N 次、遍历检索结果，全靠循环。
过关标准：全部真实运行通过，并能讲清每行作用。
"""

# ========== 基础档（必做，15 分钟） ==========

# for：把一个序列里的东西逐个取出来，range(5) 生成 0,1,2,3,4
for i in range(5):
    print("第", i, "次")

# 遍历列表：列表是一排有序盒子
fruits = ["苹果", "香蕉", "橘子"]
for fruit in fruits:
    print("水果：", fruit)

# ========== 进阶档（必做，25 分钟） ==========

# 累加：循环里把数字一个个加起来（统计、求和的通用套路）
total = 0
for n in range(1, 11):   # 1 到 10
    total = total + n
print("1 到 10 的和：", total)

# while：满足条件就一直做，条件不满足就停
count = 3
while count > 0:
    print("倒计时：", count)
    count = count - 1
print("开始！")

# break：提前跳出整个循环；continue：只跳过本次，进入下一次
# 演示 break：找到目标就立刻停止，不再往后找
for n in range(1, 6):
    if n == 3:
        print("找到 3，提前结束")
        break
    print("数字：", n)

# 演示 continue：跳过 3，但继续往后
for n in range(1, 6):
    if n == 3:
        continue
    print("数字：", n)

# ========== 贴近岗位档（选做，Agent 味） ==========

# 场景1：模型回答失败时自动重试，最多 5 次
#   用 while 模拟“只要没成功且次数没到 5 就继续”
max_retry = 3
attempt = 1
success = False
while attempt <= max_retry and not success:
    print(f"第 {attempt} 次尝试生成回答...")
    # 真实场景里这里调用模型，成功就把 success 设为 True
    attempt = attempt + 1
if not success:
    print("超过重试次数，告知用户稍后再试")

# 场景2：批量处理检索到的资料，逐条打印序号和内容
retrieved_docs = ["资料A：列车开行规则", "资料B：票价计算办法", "资料C：退票规定"]
for index, doc in enumerate(retrieved_docs):
    # enumerate 同时给出“序号”和“内容”，从 0 开始
    print(f"第 {index + 1} 条：{doc}")

# ========== 过关标准 ==========
# 基础档：打印 5 次、3 个水果；进阶档：和为 55、倒计时 3-2-1；岗位档：重试 3 次、资料 3 条