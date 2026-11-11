"""循环练习：for/while、continue、累加、嵌套判断、死循环加 break。

覆盖知识点：for 遍历、while 条件循环、continue 跳过本次、累加求和、异常输入处理。
"""

# 1. 输入正整数 n：<=0 提示重新输入；>0 依次打印 1~n 并求和
n = int(input("请输入一个数字："))
total2 = 0
if n <= 0:
    print("请输入正整数")
else:
    for i in range(1, n + 1):
        total2 = total2 + i
        print(i)
    print(f"1到{n}的总和为：{total2}")

# 2. 场景1：模型回答失败时自动重试（用 while 模拟"没成功且次数没到就继续"）
new_retry = 5
attempt = 1
success = False
while attempt <= new_retry and not success:
    print(f"第{attempt}次尝试失败，请重试")
    attempt = attempt + 1
if not success:
    print("请稍等")

# 3. 场景2：批量处理检索到的资料，逐条打印序号和作者
retrieved_name = ["张三", "李四", "王五"]
for index, name in enumerate(retrieved_name):
    index = index + 1
    print(f"第{index}个资料的作者叫作：{name}")

# 4. 用 continue 跳过第 3 个苹果（while 版本）
i = 1
while i <= 5:
    if i == 3:
        print(f"小红没有吃第{i}个苹果，因为第{i}个苹果是毒的")
        i = i + 1
        continue
    else:
        print(f"小红在吃第{i}个苹果")
    i = i + 1

# 5. 用 continue 跳过第 3 个苹果（for 版本）
for i in range(1, 6):
    if i == 3:
        print(f"小红没有吃第{i}个苹果，因为第{i}个苹果是毒的")
        continue
    else:
        print(f"小红在吃第{i}个苹果")

# 6. while 循环打印 100 次
i = 1
while i <= 100:
    print(f"好好学习，天天向上,第{i}次")
    i = i + 1

# 7. while 累加 1~100
total3 = 0
i = 1
while i <= 100:
    total3 = total3 + i
    i = i + 1
print(f"1到100 的和为：{total3}")

# 8. for 累加 1~100（每步都打印）
total3 = 0
for i in range(1, 101):
    total3 = total3 + i
    print(f"1到{i}  的和为：{total3}")
print(f"1到100 的和为：{total3}")

# 9. 嵌套判断：先查是否买票，再看体温是否正常
has_ticket = input("是否买票（是/否）：") == "是"
temperature = float(input("请输入体温："))
if has_ticket:
    if temperature >= 37.5 or temperature <= 36.5:
        print("您不能上车，因为您体温异常了")
    elif 36.5 < temperature < 37.5:
        print("您可以上车")
    else:
        print("请重试")
elif not has_ticket:
    print("请买票并测试体温")
else:
    print("请重试")

# 10. 死循环加 break：输入 0 退出，正数累加，负数忽略
total = 0
int_number = 0
while True:
    i = int(input("请输入整数："))
    if i == 0:
        break
    elif i > 0:
        total = total + i
        int_number = int_number + 1
    elif i < 0:
        print(f"{i}是负数忽略不计")
print(f"运算结束，当前和为：{total},当前有{int_number}个正数")