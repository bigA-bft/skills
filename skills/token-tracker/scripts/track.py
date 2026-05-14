#!/usr/bin/env python3
import os
import sys
from datetime import datetime


def get_project_root():
    """获取项目根目录（当前工作目录）"""
    return os.getcwd()


def get_token_usage_path():
    """获取 token 使用记录文件路径"""
    project_root = get_project_root()
    claude_dir = os.path.join(project_root, ".claude")
    if not os.path.exists(claude_dir):
        os.makedirs(claude_dir)
    return os.path.join(claude_dir, "token-usage.md")


def get_or_create_file():
    """获取或创建记录文件"""
    file_path = get_token_usage_path()
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# Token 使用记录\n\n")
    return file_path


def get_date_str():
    """获取当前日期字符串"""
    return datetime.now().strftime("%Y-%m-%d")


def get_time_str():
    """获取当前时间字符串"""
    return datetime.now().strftime("%H:%M")


def read_file_content(file_path):
    """读取文件内容"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file_content(file_path, content):
    """写入文件内容"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def add_record(user_input, claude_output, input_tokens=0, output_tokens=0):
    """添加新记录"""
    file_path = get_or_create_file()
    content = read_file_content(file_path)

    date_str = get_date_str()
    time_str = get_time_str()

    # 生成对话标题（取用户输入前20字）
    title = user_input[:20]
    if len(user_input) > 20:
        title += "..."

    # 生成 token 使用行
    if input_tokens > 0 or output_tokens > 0:
        token_line = f"**Token 使用：** 输入 {input_tokens}, 输出 {output_tokens}, 总计 {input_tokens + output_tokens}"
    else:
        token_line = "**Token 使用：** （待补充）"

    # 生成新记录条目
    new_entry = f"""### {time_str} - {title}
**用户输入：** {user_input}
**Claude 输出：** {claude_output}
{token_line}

---

"""

    # 检查今日日期是否已存在
    date_header = f"## {date_str}"
    if date_header not in content:
        content += f"\n\n{date_header}\n\n"

    # 在日期部分后插入新记录
    import re

    date_pattern = f"(## {date_str}\n\n?)"
    if re.search(date_pattern, content):
        content = re.sub(date_pattern, rf"\1{new_entry}", content)
    else:
        content += f"\n\n{date_header}\n\n{new_entry}"

    write_file_content(file_path, content)

    return file_path, input_tokens + output_tokens


def interactive_mode():
    """交互模式"""
    print("[Token Tracker] - 交互模式")
    print("=" * 50)

    user_input = input("请输入用户输入内容: ").strip()
    claude_output = input("请输入 Claude 输出内容: ").strip()

    input_tokens_str = input("请输入输入 tokens (可选，直接回车跳过): ").strip()
    output_tokens_str = input("请输入输出 tokens (可选，直接回车跳过): ").strip()

    input_tokens = int(input_tokens_str) if input_tokens_str else 0
    output_tokens = int(output_tokens_str) if output_tokens_str else 0

    return user_input, claude_output, input_tokens, output_tokens


def main():
    if len(sys.argv) == 1:
        # 交互模式
        user_input, claude_output, input_tokens, output_tokens = interactive_mode()
    elif len(sys.argv) == 3:
        # 只记录对话内容
        user_input = sys.argv[1]
        claude_output = sys.argv[2]
        input_tokens = 0
        output_tokens = 0
    elif len(sys.argv) == 5:
        # 完整记录
        user_input = sys.argv[1]
        claude_output = sys.argv[2]
        input_tokens = int(sys.argv[3])
        output_tokens = int(sys.argv[4])
    else:
        print("使用方法:")
        print("  交互模式: python track.py")
        print("  仅记录内容: python track.py \"<用户输入>\" \"<Claude 输出>\"")
        print("  完整记录: python track.py \"<用户输入>\" \"<Claude 输出>\" <输入tokens> <输出tokens>")
        sys.exit(1)

    if not user_input or not claude_output:
        print("[ERROR] 用户输入和 Claude 输出不能为空")
        sys.exit(1)

    try:
        file_path, total = add_record(user_input, claude_output, input_tokens, output_tokens)
        print(f"\n[OK] 已记录到 {file_path}")
        print(f"时间: {get_date_str()} {get_time_str()}")
        if input_tokens > 0 or output_tokens > 0:
            print(f"输入 tokens: {input_tokens}")
            print(f"输出 tokens: {output_tokens}")
            print(f"总计: {total}")
        else:
            print("（token 数据待补充）")
    except Exception as e:
        print(f"\n[ERROR] 记录失败: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
