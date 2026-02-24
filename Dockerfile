FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

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
    && tar -xzf /tmp/piper.tar.gz -C /usr/local/bin --strip-components=1 \
    && chmod +x /usr/local/bin/piper \
    && chmod +x /usr/local/bin/piper_phonemize \
    && rm /tmp/piper.tar.gz

COPY dependencies.txt /app/

RUN pip install --no-cache-dir -r dependencies.txt

ENV PYTHONPATH=/app

CMD ["python", "-m", "main.py"]
