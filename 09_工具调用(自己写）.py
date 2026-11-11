"""工具函数练习：定义一组可被模型调用的工具函数。

包含：四则运算、获取当前时间、温度转换、客流查询、拥挤判断。
这些函数将来会通过 function calling（函数调用）交给大模型按需调用。
"""
from datetime import datetime


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
            return "分母不能为零"
        else:
            return a / b
    else:
        return "运算符错误！"


print(calculator(a=2, b=4, op="+"))


def get_current_time():
    """返回当前时间，格式为 %Y-%m-%d %H:%M:%S。"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


print(get_current_time())


def convert_temperature(c, unit):
    """温度转换：c 为摄氏度；unit 为 "F" 转华氏度，为 "K" 转开尔文。"""
    if unit == "F":
        return c * 9 / 5 + 32       # 摄氏转华氏公式
    elif unit == "K":
        return c + 273.15           # 摄氏转开尔文公式
    else:
        return "不支持的单位！"


print(convert_temperature(46, "F"))


# 站点客流数据源：站名 -> 客流量
resource = {"八一广场": 150, "南昌西站": 80}


def get_station_flow(station):
    """从客流字典查询某站点客流量，查不到则返回提示。"""
    if station in resource:
        return resource[station]
    else:
        return f"未找到{station}"


print(get_station_flow("八一广场"))


def judge_crowding(flow):
    """判断拥挤程度：客流 >= 120 返回"拥挤"，否则返回"正常"。"""
    flow = float(flow)
    if flow >= 120:
        return "拥挤"
    else:
        return "正常"


print(judge_crowding(1234))