FROM python:3.10.5-slim-buster

COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    wget \
    unzip \
    firefox-esr && \
    wget -q https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar -xf /tmp/geckodriver.tar.gz -C /usr/local/bin/ && \
    rm /tmp/geckodriver.tar.gz && \
    apt-get purge -y --auto-remove \
    wget \
    unzip

RUN pip install -r requirements.txt

CMD ["python3", "server_hypercorn.py"]

