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

# Copy your full app
RUN git clone https://github.com/JoshuaStabile/deadair.git /app

RUN pip install --no-cache-dir -r /app/dependencies.txt

WORKDIR /app/code

CMD python -m code.main && tail -f /dev/null
