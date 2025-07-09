FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

COPY . .

RUN pip install .

CMD ["python", "main.py"]
