import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# 后台运行下载任务
def run_downloader(url):
    try:
        print(f"DEBUG: 开始执行任务，URL: {url}", flush=True)
        
        # 实时启动子进程
        # bufsize=1 表示行缓冲，这样 print 内容会立刻显示在日志里
        process = subprocess.Popen(
            ["python", "-u", "run.py", "--url", url], # -u 参数让 Python 不缓存输出
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # 将 stderr 合并到 stdout
            text=True,
            bufsize=1
        )
        
        print("DEBUG: 子进程已启动，正在读取实时输出...", flush=True)
        
        # 实时逐行读取输出
        for line in iter(process.stdout.readline, ''):
            print(f"RUN.PY: {line.strip()}", flush=True)
            
        process.stdout.close()
        process.wait()
        
        if process.returncode == 0:
            print("任务完成: 子进程顺利结束。", flush=True)
        else:
            print(f"--- 脚本执行失败，返回码: {process.returncode} ---", flush=True)
            
    except Exception as e:
        print(f"DEBUG: 执行脚本时发生异常: {str(e)}", flush=True)
        
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

