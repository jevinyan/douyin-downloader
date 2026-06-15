FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# 安装必要的依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn flask

# 拷贝你的代码
COPY . .

COPY config.example.yml /app/config.yml
RUN chmod 644 /app/config.yml

# 暴露端口
EXPOSE 8080

# 使用 Gunicorn 启动
# web_wrapper 是文件名，app 是文件中定义的 Flask 实例名
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "600", "web_wrapper:app"]
