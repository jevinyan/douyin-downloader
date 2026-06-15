#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path

# 1. 确定项目根目录 (即 /app)
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
os.chdir(project_root)

### 强制修正路径：将当前目录明确加入环境变量或直接指向文件 ###
# 如果 run.py 的子模块是基于当前目录查找的，我们确保当前工作目录就是 project_root
os.environ['CONFIG_PATH'] = str(project_root / 'config.yml')

# 导入你原有的主逻辑
from cli.main import main

def run_with_args(url):
    sys.argv = ["run.py", "--url", url]
    main()

if __name__ == "__main__":
    # 打印一次当前正在运行的路径，方便我们最后一次确认
    print(f"DEBUG: 正在从 {os.getcwd()} 运行，寻找 config.yml...", flush=True)
    
    # 强制验证文件是否存在，不存在直接报错提示
    config_file = project_root / 'config.yml'
    if not config_file.exists():
        print(f"CRITICAL: 仍然在 {config_file} 找不到配置文件！", flush=True)
    else:
        print(f"SUCCESS: 确认配置文件存在于 {config_file}", flush=True)

    parser = argparse.ArgumentParser(description="Douyin Downloader Wrapper")
    parser.add_argument("--url", help="抖音视频链接")
    
    args = parser.parse_args()

    if args.url:
        run_with_args(args.url)
    else:
        main()
