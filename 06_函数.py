"""第五块（三档版）：函数 def —— 把一段操作打包成工具。

岗位对应：Agent 里每个"工具"就是一个函数；写函数是开发的基本动作。
过关标准：全部真实运行通过，能讲清每行作用。
"""

# ========== 基础档（必做，15 分钟） ==========

# def 定义函数：给一段操作起名字，括号里是“输入”，return 是“输出”
def greet(name):
    return f"你好，{name}"


# 调用：写名字加括号，把数据传进去
print(greet("薛同学"))


print(greet("老师"))


# 没有参数的函数
def say_hi():
    print("hi")


say_hi()


# ========== 进阶档（必做，25 分钟） ==========


# 多个参数：算折后票价
def discounted_price(price, discount):
    return price * discount


print("折后票价：", discounted_price(320, 0.8))   # 256.0


# 函数里可以用条件判断：返回不同结果
def price_level(price):
    if price >= 300:
        return "高"
    elif price >= 150:
        return "中"
    else:
        return "低"


print(price_level(320), price_level(180), price_level(90))


# 把结果存进变量再用
final = discounted_price(460, 0.8)
print("最终：", final)

# ========== 贴近岗位档（选做，Agent 味） ==========


# 场景1：Agent 的“工具”就是一个函数 —— 票价查询工具
def ticket_tool(start, end):
    # 真实场景里这里查数据库，先用字典模拟
    table = {("南昌", "东莞"): 320, ("南昌", "深圳"): 360}
    return table.get((start, end), "暂无该线路")


print("票价查询：", ticket_tool("南昌", "东莞"))
print("票价查询：", ticket_tool("南昌", "北京"))


# 场景2：一个“计算总费用”的函数，输入输出清晰（可反复调用）
def calc_cost(input_tokens, output_tokens):
    cost = input_tokens / 1000 * 0.001 + output_tokens / 1000 * 0.002
    return round(cost, 4)


print("调用费用：", calc_cost(1200, 300))   # 0.0018

# ========== 过关标准 ==========
# 基础档：定义并调用；进阶档：多参数、带判断返回；岗位档：看懂“工具=函数”，算出 256 与 0.0018