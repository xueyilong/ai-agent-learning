"""第六块（三档版）：读写文件 —— 程序和文件打交道。

岗位对应：RAG 第一步就是读文档（PDF/Word/TXT），结果也要写进文件。
过关标准：全部真实运行通过，能讲清每行作用。
"""

# ========== 基础档（必做，15 分钟） ==========

# 写文件：open(路径, "w") 打开，"w" 表示写入（会覆盖原内容）
# encoding="utf-8" 防止中文乱码
with open("测试文件.txt", "w", encoding="utf-8") as f:
    f.write("第一行：你好\n")
    f.write("第二行：好好学习\n")
print("已写入 测试文件.txt")

# 读文件："r" 表示读取，read() 一次读全部
with open("测试文件.txt", "r", encoding="utf-8") as f:
    content = f.read()
print("读到的内容：")
print(content)

# with 的好处：用完自动关闭文件，不用手动 close

# ========== 进阶档（必做，25 分钟） ==========

# 按行读取：readlines() 得到列表，每行一个元素
with open("测试文件.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("一共几行：", len(lines))
for line in lines:
    print("这一行：", line.strip())   # strip 去掉首尾换行和空格

# 追加内容："a" 表示在末尾追加，不覆盖
with open("测试文件.txt", "a", encoding="utf-8") as f:
    f.write("第三行：追加的内容\n")

# ========== 贴近岗位档（选做，阶段1 总验收就考这个） =========
# 完整任务：读一个文本 → 统计字数 → 结果写进新文件
def count_text(input_path, output_path):
    # 1. 读原
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    # 2. 统计：总字符数（去掉换行）、行数；splitlines 能正确处理末尾换行
    char_count = len(text.replace("\n", ""))
    line_count = len(text.splitlines())
    # 3. 结果写进新文件
    result = f"总字符数：{char_count}\n总行数：{line_count}\n"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    return char_count, line_count

# 先造一个待统计的原文
with open("原文.txt", "w", encoding="utf-8") as f:
    f.write("人工智能正在改变交通。\n智能体可以调用工具。\n")

c, l = count_text("原文.txt", "统计结果.txt")
print(f"统计完成：{c} 个字符，{l} 行")

# ========== 过关标准 ==========
# 会写/读/追加；理解 with、encoding、read/readlines；岗位档独立完成“读→统计→写”