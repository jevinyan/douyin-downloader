import os
import threading
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

def run_downloader(url):
    """
    后台下载逻辑，与 Web 启动过程完全隔离
    """
    print(f">>> 开始执行后台任务, URL: {url}", flush=True)
    try:
        # 强制指定在 /app 目录下执行
        work_dir = "/app"
        
        # 验证配置文件是否存在
        config_path = os.path.join(work_dir, "config.yml")
        if not os.path.exists(config_path):
            print(">>> 警告: 未找到 config.yml，程序可能以默认模式运行。", flush=True)

        # 构建执行命令
        cmd = ["python", "-u", "run.py", "--url", url]
        
        # 执行子进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=work_dir,
            env={**os.environ} # 继承当前环境变量
        )
        
        # 实时打印子进程输出
        for line in iter(process.stdout.readline, ''):
            print(f"RUN.PY: {line.strip()}", flush=True)
            
        process.wait()
        
        if process.returncode == 0:
            print(">>> 下载任务执行成功。", flush=True)
        else:
            print(f">>> 下载脚本异常退出，错误代码: {process.returncode}", flush=True)
            
    except Exception as e:
        print(f">>> 下载逻辑发生严重异常: {str(e)}", flush=True)

@app.route('/')
def home():
    return "Douyin Downloader API is running."

@app.route('/download')
def download():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "缺少 url 参数"}), 400
    
    # 异步线程，不阻塞 Web 主进程
    thread = threading.Thread(target=run_downloader, args=(url,))
    thread.daemon = True
    thread.start()
    
    return jsonify({"status": "accepted", "message": "下载任务已触发，请查看日志获取详细进度。"}), 202

if __name__ == "__main__":
    # 仅在本地运行测试时使用
    app.run(host='0.0.0.0', port=8080)
