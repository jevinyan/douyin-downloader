FROM python:3.10-slim

# 设置环境变量，防止交互式弹窗
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8080

WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 拷贝并安装项目依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt flask --root-user-action=ignore

# 拷贝所有项目文件
COPY . .

# 暴露端口
EXPOSE 8080

# 使用 Web 包装器作为入口
CMD ["python", "web_wrapper.py"]
