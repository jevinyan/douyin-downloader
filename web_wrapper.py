import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# 后台运行下载任务
def run_downloader(url):
    try:
        print(f"正在后台处理下载任务: {url}")
        # 这里调用你的 run.py。请确保 run.py 接收 url 参数
        # 如果你的 run.py 逻辑在 main() 函数中，请根据实际情况修改
        result = subprocess.run(
            ["python", "run.py", "--url", url], 
            capture_output=True, 
            text=True
        )
        print(f"下载脚本输出: {result.stdout}")
        if result.stderr:
            print(f"下载脚本错误: {result.stderr}")
    except Exception as e:
        print(f"任务执行异常: {e}")

@app.route('/')
def home():
    return "Douyin Downloader API is running."

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    
    # 异步开启下载线程
    thread = threading.Thread(target=run_downloader, args=(url,))
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "accepted", "message": "下载任务已提交", "url": url}), 202

