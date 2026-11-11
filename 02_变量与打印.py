"""第一块（三档版）：变量、输入、计算与格式化输出。

目标：几个月后找 AI Agent 开发实习，本块是所有岗位 JD 第一条。
过关标准：全部真实运行通过，并能讲清每一行作用。
"""

# ========== 基础档（必做，5 分钟） ==========

my_city = "南昌"
my_hobby = "唱歌"
favorite_movie = "复仇者联盟"

print(f"我在{my_city}，喜欢{my_hobby}, 我最喜欢的电影是{favorite_movie}")

# ========== 进阶档（必做，20 分钟） ==========

# input()：程序暂停，等你从键盘输入，得到的是文字
# float()：把输入的文字转成数字，才能计算
a = float(input("请输入第一个数："))
b = float(input("请输入第二个数："))
c = float(input("请输入第三个数："))
is_student = True
print(f"三个数的和为{a+b+c}，"
      f"平均数为{(a+b+c)/3}， {a}是否等于 10：{a==10}， {is_student == True}")
# ========== 贴近岗位档（选做，交通味） ==========

start_station = input("请输入出发站：")
end_station = input("请输入到达站：")
ticket_price = float(input("请输入票价："))
discount = 0.8  # 8 折
ticket_price_after_discount = ticket_price * discount

print(f"从{start_station}到{end_station}，票价{ticket_price}元，折后票价为{ticket_price_after_discount:.1f}")

# ========== 过关标准 ==========
# 基础档、进阶档真实运行通过；交通档算出折后 256.0 元；能口述每行作用