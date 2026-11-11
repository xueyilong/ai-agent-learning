"""函数练习：加法计算器、票价查询、调用费用统计、客流统计。

覆盖知识点：函数定义与调用、参数、try/except 异常处理、字典、循环。
"""


def add(a, b):
    """加法计算器：两个数都为正数时返回和，否则返回提示。"""
    if a > 0 and b > 0:
        return a + b
    else:
        return "计算失败"


print(add(3, 5))  # 正常：3 + 5 = 8
print(add(-2, 4))  # 含负数：返回"计算失败"


def ticket_tool(start, end):
    """车票查询工具：从固定字典查询起终点票价，查不到则返回提示。"""
    table = {("南昌", "东莞"): 320, ("南昌", "深圳"): 360}
    return table.get((start, end), "未查到该程车")


def price(input_tokens, output_tokens):
    """计算一次模型调用费用：输入/输出 token 按不同单价计费。"""
    total_prise = input_tokens / 1000 * 0.001 + output_tokens / 1000 * 0.002
    return total_prise


count = 1
total_cost = 0
cost_dict = {}
while True:
    if count <= 3:
        # 先拿输入 token 量
        input_tokens1 = input("输入量为：")
        try:
            input_tokens1 = float(input_tokens1)  # 尝试转数字
        except ValueError:
            print("请输入数字！程序结束。")
            break

        # 再拿输出 token 量
        output_tokens1 = input("输出量为：")
        try:
            output_tokens1 = float(output_tokens1)  # 尝试转数字
        except ValueError:
            print("请输入数字！程序结束。")
            break

        # 两个都合法，才计算本次费用
        cost = price(input_tokens=input_tokens1, output_tokens=output_tokens1)
        total_cost = total_cost + cost
        print(f"当前输入次数为{count}次")
        key = f"第{count}次"
        cost_dict[key] = cost
        print(f"本次计算费用为{cost}")
        count = count + 1

    elif count > 3:
        print("计算次数已用尽，请稍后再试！")
        break

print(f"一共算了{count - 1}次，本次计算总费用为{total_cost}")
print(f"计算结果如下："
      f"{cost_dict}")
count = int(input("您想查第几次？："))
print(f"第{count}次的计算费用为{cost_dict[f"第{count}次"]}")


def total_passengers(dates):
    """汇总各站点客流量：把字典里所有值加起来。"""
    return sum(dates.values())


print(f"总客流为{total_passengers({"南昌": 120, "东莞": 80, "南京": 320, "八一广场": 160})}")


def lookup_passengers(data, station):
    """查某站点客流量，查不到则返回"未收录"。"""
    return data.get(station, "未收录")


print(lookup_passengers({"南昌": 120, "东莞": 80, "南京": 320, "八一广场": 160}, "南昌"))