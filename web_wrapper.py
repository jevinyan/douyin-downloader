import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# 后台运行下载任务
def run_downloader(url):
    try:
        print(f"DEBUG: 开始执行任务，URL: {url}", flush=True)
        print(f"DEBUG: 当前工作目录: {os.getcwd()}", flush=True)
        print(f"DEBUG: 检查目录下文件: {os.listdir('.')}", flush=True)

        # 使用 Popen 实时获取输出，而不是等待执行完毕
        process = subprocess.Popen(
            ["python", "run.py", "--url", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("DEBUG: 子进程已启动，正在等待输出...", flush=True)
        
        # 实时读取输出
        stdout, stderr = process.communicate(timeout=300)
        
        if process.returncode == 0:
            print(f"任务成功: {stdout}", flush=True)
        else:
            print(f"--- 脚本执行失败，返回码: {process.returncode} ---", flush=True)
            print(f"错误信息: {stderr}", flush=True)
            
    except subprocess.TimeoutExpired:
        print("DEBUG: 任务超时！", flush=True)
    except Exception as e:
        print(f"DEBUG: 发生未捕获异常: {str(e)}", flush=True)
        
@app.route('/')
def home():
    return "Douyin Downloader API is running."

@app.route('/download')
def download():
    # 这一行是新增的，用于在日志中留下“指纹”
    print(f">>> 收到下载请求，参数 url: {request.args.get('url')}", flush=True)
    
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    
    # 异步开启下载线程
    thread = threading.Thread(target=run_downloader, args=(url,))
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "accepted", "message": "下载任务已提交", "url": url}), 202

