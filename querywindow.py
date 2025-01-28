#!/usr/bin/env python3
import subprocess
def queryWindowInfo():
    # 调用 qdbus 命令并捕获输出
    output = subprocess.check_output(
        ['qdbus', 'org.kde.KWin', '/KWin', 'org.kde.KWin.queryWindowInfo'],
        text=True
    )

    # 初始化一个空字典
    window_info = {}

    # 按行分割输出
    lines = output.strip().split('\n')

    # 解析每一行
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value.isdigit():
                value = int(value)
            elif value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            elif value.startswith('{') and value.endswith('}'):
                value = value.strip('{}')

            window_info[key] = value
    return window_info

