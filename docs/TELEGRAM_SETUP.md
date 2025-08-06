# Настройка Telegram для уведомлений

## 1. Создание Telegram бота

1. Откройте Telegram и найдите бота [@BotFather](https://t.me/botfather)
2. Отправьте команду `/newbot`
3. Придумайте имя для вашего бота (например: "Мониторинг квартир")
4. Придумайте username для бота (должен заканчиваться на "bot", например: "apartment_monitor_bot")
5. Скопируйте токен бота (выглядит как `123456789:ABC123DEF456GHI789JKL`)

## 2. Получение Chat ID

### Способ 1: Через @userinfobot
1. Найдите в Telegram бота [@userinfobot](https://t.me/userinfobot)
2. Отправьте ему любое сообщение
3. Он ответит с вашим Chat ID

### Способ 2: Через API
1. Отправьте сообщение вашему боту в Telegram
2. Откройте в браузере: `https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates`
3. Найдите в ответе `"chat":{"id":123456789}` - это ваш Chat ID

## 3. Тестирование

Проверьте настройки, запустив:
```bash
export TG_TOKEN="ваш_токен"
export TG_CHAT_ID="ваш_chat_id"
python -c "
import requests
import os
token = os.getenv('TG_TOKEN')
chat_id = os.getenv('TG_CHAT_ID')
response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', 
                        data={'chat_id': chat_id, 'text': '🤖 Тест уведомлений'})
print('✅ Успешно!' if response.ok else '❌ Ошибка:', response.text)
"
```

## 4. Использование в проекте

Добавьте переменные в `.env` файл:
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими данными
```

Или экспортируйте в терминале:
```bash
export TG_TOKEN="ваш_токен"
export TG_CHAT_ID="ваш_chat_id"
```
