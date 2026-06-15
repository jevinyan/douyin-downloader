import os
import threading
import subprocess
from flask import Flask, request, jsonify

# 1. 确保 Flask 实例在全局定义
app = Flask(__name__)

# 2. 函数定义
def run_downloader(url):
    try:
        # 使用 -u 让 Python 输出不缓存
        cmd = ["python", "-u", "run.py", "--url", url]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd="/app" 
        )
        for line in iter(process.stdout.readline, ''):
            print(f"RUN.PY: {line.strip()}", flush=True)
        process.wait()
    except Exception as e:
        print(f"ERROR: {str(e)}", flush=True)

# 3. 路由定义 (确保 @app.route 紧贴函数定义，无任何缩进错误)
@app.route('/')
def home():
    return "Douyin Downloader API is running."

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    thread = threading.Thread(target=run_downloader, args=(url,))
    thread.daemon = True
    thread.start()
    return jsonify({"status": "accepted", "message": "下载任务已提交"}), 202

# 4. 结尾确保只有这几行
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
