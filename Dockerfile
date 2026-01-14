# ベースイメージ [cite: 1]
FROM python:3.11-slim

# OSレベルの依存パッケージ [cite: 1]
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/heredic_tree

# 依存ライブラリのインストール [cite: 1, 2]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションとフォントファイルをコピー 
COPY app/ . 
COPY README.md .

# 環境変数の設定 
ENV STREAMLIT_SERVER_PORT=8300
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

CMD ["streamlit", "run", "app.py"]