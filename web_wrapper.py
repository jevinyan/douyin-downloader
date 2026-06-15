import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def run_downloader(url):
    print(f">>> 开始执行后台任务, URL: {url}", flush=True)
    try:
        # 使用绝对路径执行，强制指定工作目录为 /app
        cmd = ["python", "-u", "run.py", "--url", url]
        
        # 建立子进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd="/app" 
        )
        
        # 实时捕获输出
        for line in iter(process.stdout.readline, ''):
            print(f"RUN.PY: {line.strip()}", flush=True)
            
        process.wait()
        
        if process.returncode == 0:
            print(">>> 任务执行完毕。", flush=True)
        else:
            print(f">>> 脚本异常退出，代码: {process.returncode}", flush=True)
            
    except Exception as e:
        # 必须配套处理异常
        print(f">>> 执行过程中出现错误: {str(e)}", flush=True)

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
    
    return jsonify({"status": "accepted", "message": "下载任务已提交"}), 202

# 结尾不留多余的 try 或缩进块
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
