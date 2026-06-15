import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# 后台运行下载任务
def run_downloader(url):
    try:
        print(f"正在后台启动任务，URL: {url}")
        
        # 增加 check=True，这样如果脚本运行出错，它会抛出异常
        # 增加 stdout=subprocess.PIPE, stderr=subprocess.PIPE 来捕获详细日志
        result = subprocess.run(
            ["python", "run.py", "--url", url], 
            capture_output=True, 
            text=True,
            check=True 
        )
        print(f"任务成功: {result.stdout}")
        
    except subprocess.CalledProcessError as e:
        # 如果脚本退出码不为0，这里会捕获到详细的错误信息
        print(f"--- 脚本执行失败 ---")
        print(f"错误代码: {e.returncode}")
        print(f"标准错误输出 (stderr): {e.stderr}")
        print(f"标准输出 (stdout): {e.stdout}")
        
    except Exception as e:
        print(f"任务执行时发生异常: {str(e)}")

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

