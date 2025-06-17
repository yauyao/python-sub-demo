FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY scripts/ scripts/

ENV PYTHONUNBUFFERED=1
ENV REDIS_URL=redis://localhost:6379
ENV MODE=api
ENV PYTHONPATH=/app

CMD if [ "$MODE" = "pubsub" ]; then \
        python scripts/run_pubsub.py; \
    else \
        python -m src.my_project.main; \
    fi
