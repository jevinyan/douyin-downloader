FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn flask
RUN find . -name "*.pyc" -delete
COPY . .
# 强制拷贝配置并赋予读取权限，确保文件在容器内物理存在
RUN cp config.example.yml config.yml && chmod 644 config.yml
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "600", "web_wrapper:app"]
