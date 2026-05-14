#!/usr/bin/env python3
import os
import re
from datetime import datetime


def get_project_root():
    """获取项目根目录（当前工作目录）"""
    return os.getcwd()


def get_token_usage_path():
    """获取 token 使用记录文件路径"""
    project_root = get_project_root()
    claude_dir = os.path.join(project_root, ".claude")
    return os.path.join(claude_dir, "token-usage.md")


def read_file_content(file_path):
    """读取文件内容"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_records(content):
    """解析所有记录"""
    today_date = datetime.now().strftime("%Y-%m-%d")

    # 匹配所有记录中的 token 使用
    # 格式: **Token 使用：** 输入 450, 输出 280, 总计 730
    pattern = r"\*\*Token 使用：\*\* 输入 (\d+), 输出 (\d+), 总计 (\d+)"
    matches = re.findall(pattern, content)

    total_count = 0
    total_input = 0
    total_output = 0
    total_total = 0

    today_count = 0
    today_input = 0
    today_output = 0
    today_total = 0

    # 先找到今日部分的内容
    today_section = ""
    today_pattern = rf"## {today_date}(.*?)(?=## \d{{4}}-\d{{2}}-\d{{2}}|$)"
    today_match = re.search(today_pattern, content, re.DOTALL)
    if today_match:
        today_section = today_match.group(1)

    # 解析今日记录
    today_matches = re.findall(pattern, today_section)
    for match in today_matches:
        today_count += 1
        today_input += int(match[0])
        today_output += int(match[1])
        today_total += int(match[2])

    # 解析所有记录
    for match in matches:
        total_count += 1
        total_input += int(match[0])
        total_output += int(match[1])
        total_total += int(match[2])

    return {
        "today": {
            "date": today_date,
            "count": today_count,
            "input": today_input,
            "output": today_output,
            "total": today_total,
        },
        "total": {
            "count": total_count,
            "input": total_input,
            "output": total_output,
            "total": total_total,
        },
    }


def display_stats():
    """显示统计信息"""
    file_path = get_token_usage_path()
    content = read_file_content(file_path)

    if not content:
        print("[ERROR] 未找到记录文件")
        print(f"文件路径: {file_path}")
        return

    stats = parse_records(content)

    print("[Stats] Token 使用统计")
    print("=" * 50)

    t = stats["today"]
    print(f"今日 ({t['date']}):")
    print(f"  对话次数: {t['count']}")
    print(f"  输入 tokens: {t['input']:,}")
    print(f"  输出 tokens: {t['output']:,}")
    print(f"  总计: {t['total']:,}")
    print()

    t = stats["total"]
    print("总计:")
    print(f"  对话次数: {t['count']}")
    print(f"  输入 tokens: {t['input']:,}")
    print(f"  输出 tokens: {t['output']:,}")
    print(f"  总计: {t['total']:,}")


def main():
    display_stats()


if __name__ == "__main__":
    main()
