"""读写文件练习：写文件、读文件、追加内容、统计字数并写回。

覆盖知识点：open 的 w/r/a 三种模式、with 自动关闭、read/readlines、
以及一个完整的"读 -> 统计 -> 写"函数流程（对应 RAG 读文档的第一步）。
"""
# 1. 写文件："w" 模式会覆盖原内容，encoding="utf-8" 防止中文乱码
with open("测试文件.txt", "w", encoding="utf-8") as f:
    f.write("第一行:你好\n")
    f.write("第二行:薛同学\n")
print("已经写入 测试文件.txt")

# 2. 读文件："r" 模式读取，read() 一次读全部
with open("测试文件.txt", "r", encoding="utf-8") as f:
    content = f.read()
print(content)

# 3. 按行读取：readlines() 返回列表，每行一个元素；strip() 去掉首尾换行和空格
with open("测试文件.txt", "r", encoding="utf-8") as f:
    lens = f.readlines()
print("一共有：", len(lens), "行")
for line in lens:
    print("这一行", line.strip())

# 4. 追加内容："a" 模式在末尾追加，不覆盖原有内容
with open("测试文件.txt", "a", encoding="utf-8") as f:
    f.write("第三行:请走这边\n")

with open("测试文件.txt", "r", encoding="utf-8") as f:
    lens = f.readlines()
print("一共有：", len(lens), "行")
for line in lens:
    print("这一行", line.strip())


def count_text(input_path, output_path):
    """读 -> 统计 -> 写：统计文件的字符数和行数，结果写入另一个文件。"""
    # 1. 读这份文件
    with open(input_path, "r", encoding="utf-8") as a:
        text = a.read()
        # 2. 统计字符数（去掉换行符）和行数
        char_count = len(text.replace("\n", ""))
        len_count = len(text.splitlines())
        results = f"这份文件的字符数为{char_count},行数为{len_count}"
    # 3. 结果写进新文件
    with open(output_path, "w", encoding="utf-8") as a:
        a.write(results)
    return char_count, len_count


# 先造一个待统计的文件
with open("测试文件1.txt", "w", encoding="utf-8") as w:
    w.write("第一行:你好\n第二行:薛同学\n")

c, o = count_text(input_path="测试文件1.txt", output_path="统计结果.txt")
print(f"测试文件的字符数为{c},行数为{o}")


def text_processing(input_path, output_path):
    """统计文本字符数（不计空白）和行数，并写回结果文件。"""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
        # 逐个字符判断，非空白字符才算 1 个
        char_count = 0
        for i in text:
            if not i.isspace():
                char_count = char_count + 1
        len_count = len(text.splitlines())
        result = f"文本的字符数为{char_count},行数为{len_count}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result)
    return char_count, len_count


c, e = text_processing("素材.txt", "统计结果.txt")
print(f"字符数为{c}，行数为{e}")
with open("统计结果.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)