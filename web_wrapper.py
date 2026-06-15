import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def run_downloader(url):
    print(f">>> 开始执行后台任务, URL: {url}", flush=True)
    try:
        # 获取当前环境变量并添加 CONFIG_PATH
        my_env = os.environ.copy()
        my_env["CONFIG_PATH"] = "/app/config.yml" # 强行指定配置路径
        
        cmd = ["python", "-u", "run.py", "--url", url]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd="/app",
            env=my_env  # 注入环境变量
        )
        
        for line in iter(process.stdout.readline, ''):
            print(f"RUN.PY: {line.strip()}", flush=True)
            
        process.wait()

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    
    thread = threading.Thread(target=run_downloader, args=(url,))
    thread.daemon = True
    thread.start()
    return jsonify({"status": "accepted", "message": "下载任务已提交"}), 202

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
