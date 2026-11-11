"""第二块（三档版）：条件判断 —— 让程序会做选择。

岗位对应：Agent 里"要不要调用工具、置信度够不够、要不要重试"全靠 if。
过关标准：全部真实运行通过，改变量/输入时输出正确变化，并能讲清每行作用。
"""

# ========== 基础档（必做，10 分钟） ==========

# 比较：>  <  >=  <=  ==（等于）  !=（不等于），结果是 True/False
# 结构：if 条件: → 满足执行；elif → 再判断；else → 都不满足
score = float(input("输入分数："))
if score >= 60:
    print("及格")
else:
    print("不及格")

# ========== 进阶档（必做，25 分钟） ==========

# 多分支：把一个区间分成几档，注意判断顺序从高到低
score2 = float(input("再输入一个分数："))
if score2 >= 90:
    print("优秀")
elif score2 >= 80:
    print("良好")
elif score2 >= 60:
    print("及格")
else:
    print("不及格")

# 逻辑组合：and 并且、or 或者、not 取反
age = int(input("输入年龄："))
has_time = input("是否能连续实习3个月（是/否）：") == "是"
if age >= 18 and has_time:
    print("符合实习基本条件")
else:
    print("不符合")

# ========== 贴近岗位档（选做，Agent 味） ==========

# 场景1：Agent 根据“检索到的资料数量”决定怎么走
#   命中 0 条 → 直接告诉用户“资料不足”
#   命中 1-3 条 → 用这些资料回答
#   命中 >3 条 → 先做重排序（Rerank）再回答
retrieved = int(input("输入检索到的资料条数："))
if retrieved == 0:
    print("资料不足，无法回答")
elif retrieved <= 3:
    print("直接用检索资料回答")
else:
    print("先重排序，再回答")

# 场景2：根据模型回答的“置信度”决定是否重试（0~1 之间，越高越可信）
confidence = float(input("输入模型置信度："))
if confidence >= 0.8:
    print("直接采用回答")
elif confidence >= 0.5:
    print("补充检索后再回答")
else:
    print("重新生成（重试）")

# ========== 过关标准 ==========
# 基础档：60 为界；进阶档：90/80/60 三档正确；岗位档：0、2、5 条与 0.9、0.6、0.3 各测一遍