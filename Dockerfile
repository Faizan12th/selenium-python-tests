# ✅ Dockerfile for Selenium Test Container (Python + Chrome + ChromeDriver)
FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    google-chrome-stable chromium-driver --no-install-recommends

# Download ChromeDriver dynamically
RUN CHROME_VERSION=$(google-chrome-stable --version | grep -oP "\d+\.\d+\.\d+") && \
    DRIVER_VERSION=$(curl -sSL "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json" | \
    grep -B3 $CHROME_VERSION | grep "version" | head -1 | cut -d '"' -f4) && \
    curl -sSLO "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

ENV DISPLAY=:99

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "tests.py"]
