FROM python:3.10-slim

# 1. 设置非交互式安装
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 2. 安装系统依赖 (如有)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 3. 升级 pip 并安装项目依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --root-user-action=ignore

COPY . .

CMD ["python", "main.py"]
