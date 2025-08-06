# 🚀 БЫСТРЫЙ ДЕПЛОЙ

## Готово к коммиту на GitHub!

### ✅ Что готово:
- 🤖 Рабочий бот с двумя режимами (all/liner)
- 🐳 Docker контейнеризация с multi-stage build
- 🔄 GitHub Actions для автоматического деплоя
- 📝 Полная документация
- 🛡️ Безопасность: non-root пользователь, health checks
- 📊 Production-ready конфигурация

### 🎯 Следующие шаги:

#### 1. Создать GitHub репозиторий
```bash
git init
git add .
git commit -m "Initial commit: DOM.RF monitoring bot"
git remote add origin https://github.com/username/domrf-monitoring.git
git push -u origin main
```

#### 2. Настроить GitHub Secrets
Перейти в `Settings > Secrets and variables > Actions` и добавить:
- `TG_TOKEN` - токен бота (@BotFather)
- `TG_CHAT_ID` - ID чата (@userinfobot)  
- `HOST` - IP сервера
- `USERNAME` - SSH пользователь
- `SSH_KEY` - приватный SSH ключ

#### 3. Локальный тест
```bash
cp .env.example .env
# Заполнить .env своими данными
cd deploy && docker-compose up -d
cd deploy && docker-compose logs -f
```

#### 4. Автоматический деплой
Каждый push в main → автоматическое обновление на сервере!

### 📋 Файлы в репозитории:
```
├── 📂 src/                     # Исходный код
│   ├── 🤖 bot_liner_monitor.py # Основной бот
│   └── 🔍 debug_parser.py      # Отладка
├── 📂 scripts/                 # Скрипты запуска и тестирования
│   ├── 🚀 run_all_mode.sh      # Запуск режима "все квартиры"
│   ├── 🏠 run_liner_mode.sh    # Запуск режима "ЖК Лайнер"
│   ├── 🧪 test_modes.py        # Тестирование всех режимов
│   └── ✅ test_project.sh      # Комплексное тестирование
├── 📂 deploy/                  # Конфигурация деплоя
│   ├── 🐳 Dockerfile           # Multi-stage build
│   ├── 🐙 docker-compose.yml   # Локальный запуск
│   └── ⚙️  liner.service       # Systemd сервис
├── 📂 docs/                    # Документация
│   ├── � QUICK_DEPLOY.md      # Этот файл
│   ├── 🔑 GITHUB_SECRETS.md    # Настройка секретов
│   ├── � TELEGRAM_SETUP.md    # Настройка Telegram
│   └── 💻 DEVELOPMENT.md       # Техническая документация
├── 📂 .github/workflows/       # CI/CD автоматизация
├── 📋 requirements.txt         # Зависимости
├── 🔧 .env.example             # Пример конфигурации
└── 📄 LICENSE                  # MIT лицензия
```

### 🎉 ГОТОВО!
Проект полностью подготовлен для production деплоя с автоматизацией через GitHub Actions.
