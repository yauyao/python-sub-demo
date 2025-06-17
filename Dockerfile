# 使用官方 Python 映像
FROM python:3.12-slim

# 安裝 git
RUN apt-get update && apt-get install -y git && apt-get clean

# 設定工作目錄
WORKDIR /app

# Clone GitHub 專案
RUN git clone https://github.com/yauyao/python-sub-demo.git .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數（可選）
ENV PYTHONUNBUFFERED=1
ENV REDIS_URL=redis://localhost:6379
ENV MODE=api
ENV PYTHONPATH=/app

# 預設執行指令
CMD if [ "$MODE" = "pubsub" ]; then \
        python scripts/run_pubsub.py; \
    else \
        python -m src.my_project.main; \
    fi
