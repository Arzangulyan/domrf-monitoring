# Многоэтапная сборка для оптимизации размера
FROM python:3.11-slim as builder

# Установка системных зависимостей для сборки
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Создание виртуального окружения
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chromium

# Финальный образ
FROM python:3.11-slim

# Установка runtime зависимостей
RUN apt-get update && apt-get install -y \
    # Зависимости для Playwright
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Копирование виртуального окружения из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копирование браузера Playwright
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

# Создание рабочей директории
WORKDIR /app

# Копирование кода приложения
COPY src/bot_liner_monitor.py .
COPY src/debug_parser.py .

# Переменные окружения по умолчанию
ENV TG_TOKEN=""
ENV TG_CHAT_ID=""
ENV MONITOR_MODE="all"
ENV CHECK_INTERVAL="60"

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
# Копируем playwright данные в домашнюю директорию пользователя app
RUN cp -r /root/.cache/ms-playwright /home/app/.cache/ && chown -R app:app /home/app/.cache/
USER app

# Healthcheck
HEALTHCHECK --interval=5m --timeout=30s --start-period=1m --retries=3 \
  CMD python -c "import requests; requests.get('https://api.telegram.org', timeout=10)" || exit 1

# Запуск приложения
CMD ["python", "bot_liner_monitor.py"]
