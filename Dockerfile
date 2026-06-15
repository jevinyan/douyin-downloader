FROM python:3.10-slim

# 设置环境变量
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080

WORKDIR /app

# 安装必要依赖
RUN apt-get update && apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt flask --root-user-action=ignore

COPY . .

# 暴露端口
EXPOSE 8080

# 启动 Web 包装器，而不是直接运行 run.py
CMD ["python", "web_wrapper.py"]
