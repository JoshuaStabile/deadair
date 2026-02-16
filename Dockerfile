FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ffmpeg \
        curl \
        sqlite3 \
        openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Install Piper (ARM64)
RUN curl -L https://github.com/rhasspy/piper/releases/latest/download/piper_linux_aarch64.tar.gz -o /tmp/piper.tar.gz \
    && tar -xzf /tmp/piper.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/piper \
    && rm /tmp/piper.tar.gz

WORKDIR /app

# Copy dependency file first (better caching)
COPY dependencies.txt .
RUN pip install --no-cache-dir -r dependencies.txt

# Copy your full app
COPY . .

CMD ["python", "main.py"]
