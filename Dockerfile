FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件到容器
COPY requirements.txt /app/

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目文件到容器
COPY . /app/

# 公开端口（通常Django默认是8000端口）
EXPOSE 8000

# 运行数据库迁移和启动Django开发服务器
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]