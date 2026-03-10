import os
from pathlib import Path

ROOT = Path(__file__).parent.parent


def load_env_file(path: str = None) -> None:
    """
    Минималистичный парсер .env:
    - поддерживает строки вида KEY=VALUE
    - игнорирует пустые строки и комментарии (# ...)
    - ПЕРЕЗАПИСЫВАЕТ переменные окружения (чтобы .env имел приоритет)
    """
    p = Path(path) if path else ROOT / ".env"
    if not p.exists():
        return

    for raw_line in p.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            os.environ[key] = value  # важно: перезаписываем


def get_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN (и не найден в .env)")
    return token
