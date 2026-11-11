"""列表与字典练习：遍历列表、切片、用字典模拟站点的客流量管理。

覆盖知识点：列表遍历 enumerate、切片、append、字典增改查、while 循环输入。
"""

# 列表：一排有序盒子，位置从 0 开始
stations = ["北京", "上海", "广州", "深圳", "成都"]

# enumerate 同时给出"序号"和"内容"，序号从 0 开始，这里 +1 从 1 开始显示
for index, station in enumerate(stations):
    index = index + 1
    print(f"第{index}站：{station}")

print(stations[0])      # 取第 1 个：北京
print(stations[-1])     # 取最后一个：成都
print(stations[1:3])    # 切片：第 2、3 个（含头不含尾）
print(stations[2:])     # 从第 3 个到最后
print(stations[:3])     # 从开头到第 3 个（不含下标 3）
stations.append("东莞")  # 末尾追加一个
print(stations)
print(len(stations))    # 列表长度

# 字典：带标签的盒子，存"站名 -> 客流量"
stations = {"南昌": 120, "东莞": 80, "南京": 320, "八一广场": 150}
zkl = 0      # 累计客流量
count = 0    # 统计的站数
while True:
    station = input("请输入站名：")
    xkl = (input("请输入新增客流量："))
    # 站名不存在，或输入的不是数字，就报错退出
    if station not in stations.keys() or not xkl.isdigit():
        print("输入错误或未收录")
        break
    elif station in stations:
        print(f"{station}站的客流量为{stations[station]}")
        stations[station] = int(xkl) + stations[station]  # 更新该站客流量
        print(f"{station}站更新后客流量为{stations[station]}")
        zkl = zkl + stations[station]
        count = count + 1
        print(f"统计的客流量为{zkl},当前一共有{zkl}的客流量")
        print(f"当前一共有{count}站的客流量")
print(f"当前一共有{zkl}的客流量，当前一共有{count}站的客流量")