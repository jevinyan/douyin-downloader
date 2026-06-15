import os
import threading
from flask import Flask
import subprocess

app = Flask(__name__)

# 定义后台运行下载任务的函数
def start_downloader():
    # 这里根据你的项目实际情况修改启动命令，例如：
    # subprocess.run(["python", "run.py", "-c", "config.yml"])
    print("下载任务已在后台启动...")

@app.route('/')
def home():
    return "Downloader is running and healthy."

if __name__ == "__main__":
    # 启动后台线程运行下载逻辑
    thread = threading.Thread(target=start_downloader)
    thread.daemon = True
    thread.start()
    
    # 启动 Web 服务占用端口，满足 Back4app 要求
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
