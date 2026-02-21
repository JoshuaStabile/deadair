import os

JELLYFIN_DB_PATH = os.getenv("JELLYFIN_DB_PATH")
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")
ICECAST_URL = os.getenv("ICECAST_URL")

PIPER_MODEL_PATH = "/app/resources/piper/en_US-arctic-medium.onmx"
PIPER_OUTPUT_FILE = "/app/output/output.wav"

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.getenv("LOG_FILE", "deadair.log")
LOG_MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", 5 * 1024 * 1024))  # 5MB
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 3))