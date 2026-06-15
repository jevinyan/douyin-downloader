#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

# 保留你原有的路径逻辑
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

# 导入你原有的主逻辑
from cli.main import main

def run_with_args(url):
    """
    这是一个包装函数，模拟命令行调用
    通过修改 sys.argv，我们可以把传入的 url 传递给原来的 main()
    """
    # 将 url 拼接成命令行参数列表
    # 假设你的 cli.main.main() 解析的是类似 ["--url", url] 的参数
    sys.argv = ["run.py", "--url", url]
    main()

if __name__ == "__main__":
    # 使用 argparse 处理命令行参数
    parser = argparse.ArgumentParser(description="Douyin Downloader Wrapper")
    parser.add_argument("--url", help="抖音视频链接")
    
    args = parser.parse_args()

    if args.url:
        # 如果通过命令行传入了 --url，直接调用
        run_with_args(args.url)
    else:
        # 否则依然保持原有的启动方式（兼容之前的逻辑）
        main()
