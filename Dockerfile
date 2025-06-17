FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    ca-certificates \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

ENV CHROMEDRIVER_VERSION=137.0.7151.70
RUN wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

ENV DISPLAY=:99

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "tests.py"]
