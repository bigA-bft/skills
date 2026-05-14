#!/usr/bin/env python3
"""
用终端输出二维码
"""
import sys
import io
import qrcode

def generate_qr() -> None:
    """
    显示百度链接二维码
    这是一个使用qrcode库生成并显示二维码的函数
    函数不需要返回值，直接在终端打印二维码
    """
    qr = qrcode.QRCode()  # 创建QRCode对象实例
    qr.add_data("https://www.baidu.com")  # 向QRCode对象添加要编码的数据，这里是百度网址
    qr.make(fit=True)

    # 获取二维码矩阵
    matrix = qr.get_matrix()

    # 使用简单的字符打印二维码
    output = []
    for row in matrix:
        line = ''.join(['██' if cell else '  ' for cell in row])
        output.append(line)

    # 打印二维码
    print('\n'.join(output))

def main():
    # 设置标准输出编码为UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    generate_qr()
    sys.exit(0)

if __name__ == "__main__":
    main()
