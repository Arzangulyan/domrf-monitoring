# ДОМ.РФ Мониторинг Квартир

Telegram бот для мониторинга новых квартир на сайте аренда.дом.рф

## 🚀 Возможности

- ✅ **Двойной режим мониторинга**: ЖК Лайнер или все квартиры в Москве
- ✅ **Мгновенные уведомления** в Telegram с подробной информацией
- ✅ **Умное отслеживание** состояния (без дубликатов)
- ✅ **Автоматические проверки** каждые 60 минут
- ✅ **Docker контейнеризация** для простого деплоя
- ✅ **CI/CD через GitHub Actions** для автоматического обновления
- ✅ **Production-ready** с health checks и restart policies

## ⚡ Быстрый старт

### 1. Настройка Telegram бота

1. Создайте бота: напишите @BotFather → `/newbot`
2. Получите токен бота
3. Получите Chat ID: напишите @userinfobot

### 2. Запуск с Docker Compose (рекомендуется)

```bash
# Клонирование
git clone https://github.com/your-username/domrf-monitoring.git
cd domrf-monitoring

# Настройка окружения
cp .env.example .env
nano .env  # Укажите ваши TG_TOKEN и TG_CHAT_ID

# Запуск
cd deploy && docker-compose up -d

# Мониторинг логов
cd deploy && docker-compose logs -f domrf-monitor
```

### 3. Локальный запуск для разработки

```bash
# Установка зависимостей
pip install -r requirements.txt
playwright install chromium

# Настройка переменных
export TG_TOKEN="your_bot_token"
export TG_CHAT_ID="your_chat_id" 
export MONITOR_MODE="all"

# Запуск
python src/bot_liner_monitor.py
```

## 🔧 Конфигурация

| Переменная | Описание | Значения | По умолчанию |
|------------|----------|----------|--------------|
| `TG_TOKEN` | Токен Telegram бота | string | **обязательно** |
| `TG_CHAT_ID` | ID чата для уведомлений | number | **обязательно** |
| `MONITOR_MODE` | Режим мониторинга | `all`/`liner` | `all` |
| `CHECK_INTERVAL` | Интервал проверки (мин) | number | `60` |

### Режимы мониторинга

- **`all`**: Все квартиры в Москве (~5 квартир обычно)
- **`liner`**: Только ЖК Лайнер (фильтрация по названию)

## 🚢 Автоматический деплой

### Настройка GitHub Actions

1. **Форкните репозиторий**
2. **Добавьте секреты** в `Settings > Secrets and variables > Actions`:
   ```
   TG_TOKEN=ваш_токен_бота
   TG_CHAT_ID=ваш_chat_id
   HOST=ip_адрес_сервера
   USERNAME=имя_пользователя_ssh
   SSH_KEY=приватный_ssh_ключ
   ```
3. **Push в main** → автоматический деплой!

Подробные инструкции: [docs/GITHUB_SECRETS.md](docs/GITHUB_SECRETS.md)

## 📁 Архитектура проекта

```
├── 📂 src/                     # Исходный код
│   ├── 🤖 bot_liner_monitor.py # Основной бот с двумя режимами  
│   └── 🔍 debug_parser.py      # Отладка парсинга сайта
├── 📂 scripts/                 # Скрипты запуска и тестирования
│   ├── 🚀 run_all_mode.sh      # Запуск режима "все квартиры"
│   ├── 🏠 run_liner_mode.sh    # Запуск режима "ЖК Лайнер"  
│   ├── 🧪 test_modes.py        # Тестирование всех режимов
│   └── ✅ test_project.sh      # Комплексное тестирование
├── � deploy/                  # Конфигурация деплоя
│   ├── �🐳 Dockerfile           # Multi-stage production build
│   ├── 🐙 docker-compose.yml   # Локальный запуск
│   └── ⚙️  liner.service       # Systemd сервис
├── 📂 docs/                    # Документация
│   ├── 🚀 QUICK_DEPLOY.md      # Быстрый деплой
│   ├── 🔑 GITHUB_SECRETS.md    # Настройка секретов
│   ├── 📱 TELEGRAM_SETUP.md    # Настройка Telegram
│   └── 💻 DEVELOPMENT.md       # Техническая документация
├── 📂 .github/workflows/       # CI/CD автоматизация
│   └── ⚙️  deploy.yml          # GitHub Actions
├── 📋 requirements.txt         # Python зависимости
├── 🔧 .env.example             # Пример конфигурации
└── � LICENSE                  # MIT лицензия
```

## 🛠️ Отладка и тестирование

### Проверка парсинга сайта
```bash
python src/debug_parser.py
```

### Тестирование уведомлений
```bash
python scripts/test_modes.py
```

### Просмотр логов Docker
```bash
# Все логи
cd deploy && docker-compose logs -f

# Только ошибки  
cd deploy && docker-compose logs --tail=100 domrf-monitor | grep -i error
```

### Проверка состояния контейнера
```bash
cd deploy && docker-compose ps
cd deploy && docker-compose exec domrf-monitor python -c "import requests; print('OK')"
```

## 📊 Мониторинг в production

Бот автоматически:
- 🔄 Перезапускается при ошибках (`restart: unless-stopped`)
- 💓 Проверяет health status каждые 5 минут
- 📝 Ведет подробные логи с timestamp
- 💾 Сохраняет состояние в `state_all.json`

## 🤝 Разработка

```bash
# Установка dev зависимостей
pip install -r requirements.txt

# Проверка кода
python -m py_compile *.py

# Тестирование режимов
./scripts/test_project.sh
```

## 📞 Поддержка

Подробная документация в папке `docs/`:
- 📖 [Быстрый деплой](docs/QUICK_DEPLOY.md)
- 🔑 [Настройка GitHub Secrets](docs/GITHUB_SECRETS.md)  
- 📱 [Настройка Telegram](docs/TELEGRAM_SETUP.md)
- 💻 [Техническая документация](docs/DEVELOPMENT.md)

При проблемах проверьте:
1. 🔑 Правильность токенов в `.env`
2. 🌐 Доступность сайта аренда.дом.рф
3. 📱 Работу Telegram API
4. 🐳 Логи Docker контейнера
