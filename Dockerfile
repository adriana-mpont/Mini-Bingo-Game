FROM python:3.11.9-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HISTORY_DIR=/app/data

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN mkdir -p /app/data

CMD ["python", "-m", "src.main"]
