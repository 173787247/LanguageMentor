# LanguageMentor Dockerfile
# 基于 Python 3.11 的镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY src/ ./src/
COPY config.json.example ./config.json.example

# 创建必要的目录
RUN mkdir -p logs

# 设置 Python 路径
ENV PYTHONPATH=/app

# 暴露端口（如果需要运行 Gradio 等服务）
EXPOSE 7860

# 默认命令（可以根据需要修改）
CMD ["python", "-m", "src.agents.conversation_agent"]

