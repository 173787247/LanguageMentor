#!/bin/bash
# Docker 镜像构建脚本

echo "Building LanguageMentor Docker image..."

# 构建镜像
docker build -t language-mentor:latest .

echo "Docker image built successfully!"
echo "To run the container:"
echo "  docker run -p 7860:7860 -e OPENAI_API_KEY=your_key language-mentor:latest"

