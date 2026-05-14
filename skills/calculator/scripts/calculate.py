#!/usr/bin/env python3
"""
计算器脚本 - 支持加减乘除运算，显示计算过程
"""

import sys
from decimal import Decimal, getcontext


# 设置高精度计算
getcontext().prec = 50


def format_number(num):
    """格式化数字，去除不必要的末尾零，避免科学计数法"""
    if isinstance(num, Decimal):
        # 转换为字符串，不使用 normalize() 避免科学计数法
        num_str = format(num, 'f')
    else:
        num_str = str(num)

    # 去除末尾的零
    if '.' in num_str:
        num_str = num_str.rstrip('0').rstrip('.')

    return num_str


def parse_expression(expression):
    """解析数学表达式，提取数字和运算符"""
    # 移除空格
    expression = expression.replace(' ', '')

    numbers = []
    operators = []
    current_num = ''

    i = 0
    while i < len(expression):
        char = expression[i]

        if char in '+-*/':
            # 处理运算符
            # 检查是否是负号（在开头或前一个字符是运算符时）
            if char == '-' and (i == 0 or expression[i-1] in '+-*/'):
                current_num += char
            else:
                if current_num:
                    numbers.append(Decimal(current_num))
                    current_num = ''
                operators.append(char)
        else:
            current_num += char

        i += 1

    # 添加最后一个数字
    if current_num:
        numbers.append(Decimal(current_num))

    return numbers, operators


def calculate(expression):
    """
    计算表达式并返回结果和计算过程
    支持格式：数字 运算符 数字 [运算符 数字 ...]
    示例：10 + 20 * 3 - 5 / 2
    """
    try:
        # 清理表达式
        expression = expression.strip()

        if not expression:
            return None, "请输入计算表达式"

        # 解析表达式
        numbers, operators = parse_expression(expression)

        if len(numbers) == 0:
            return None, "无法解析表达式，请使用数字和运算符（+ - * /）"

        if len(numbers) == 1:
            return numbers[0], f"输入的数字是：{format_number(numbers[0])}"

        if len(operators) != len(numbers) - 1:
            return None, "表达式格式不正确，运算符和数字数量不匹配"

        # 显示原始表达式
        steps = [f"计算表达式：{expression}"]
        steps.append("")

        # 创建数字和运算符的副本用于计算
        nums = list(numbers)
        ops = list(operators)

        # 第一轮：处理乘除（从左到右）
        i = 0
        while i < len(ops):
            if ops[i] in ['*', '/']:
                a, b = nums[i], nums[i + 1]
                op = ops[i]

                if op == '*':
                    result = a * b
                    steps.append(f"{format_number(a)} × {format_number(b)} = {format_number(result)}")
                else:  # op == '/'
                    if b == 0:
                        return None, "错误：除数不能为零"
                    result = a / b
                    steps.append(f"{format_number(a)} ÷ {format_number(b)} = {format_number(result)}")

                # 更新数组
                nums[i] = result
                del nums[i + 1]
                del ops[i]
            else:
                i += 1

        # 第二轮：处理加减（从左到右）
        i = 0
        while i < len(ops):
            a, b = nums[i], nums[i + 1]
            op = ops[i]

            if op == '+':
                result = a + b
                steps.append(f"{format_number(a)} + {format_number(b)} = {format_number(result)}")
            else:  # op == '-'
                result = a - b
                steps.append(f"{format_number(a)} - {format_number(b)} = {format_number(result)}")

            # 更新数组
            nums[i] = result
            del nums[i + 1]
            del ops[i]

        final_result = nums[0]
        steps.append("")
        steps.append(f"最终结果：{format_number(final_result)}")

        return final_result, "\n".join(steps)

    except Exception as e:
        return None, f"计算错误：{str(e)}"

def main():
    if len(sys.argv) < 2:
        print("用法：python calculate.py '表达式'")
        print("示例：python calculate.py '10 + 20 * 3'")
        sys.exit(1)

    expression = sys.argv[1]
    result, process = calculate(expression)

    print(process)

    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
