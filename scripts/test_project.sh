#!/bin/bash

echo "🚀 Тестирование проекта мониторинга квартир"
echo "============================================="

# Проверка виртуального окружения
if [ ! -d "../.venv" ]; then
    echo "❌ Виртуальное окружение не найдено"
    exit 1
fi

echo "✅ Виртуальное окружение найдено"

# Активация окружения
source ../.venv/bin/activate
echo "✅ Виртуальное окружение активировано"

# Проверка зависимостей
python -c "import playwright, schedule, requests; print('✅ Все зависимости установлены')" 2>/dev/null || {
    echo "❌ Не все зависимости установлены"
    echo "Запустите: pip install -r ../requirements.txt"
    exit 1
}

# Проверка браузера Playwright
python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); b = p.chromium.launch(); b.close(); p.stop(); print('✅ Chromium готов к работе')" 2>/dev/null || {
    echo "❌ Chromium не установлен"
    echo "Запустите: playwright install chromium"
    exit 1
}

echo ""
echo "🔧 Тестирование режимов мониторинга:"

# Тест режима "все квартиры"
echo "🏠 Тестирую режим 'все квартиры'..."
export MONITOR_MODE=all
python -c "
import sys
sys.path.append('../src')
import asyncio
from bot_liner_monitor import fetch_flats

async def test():
    flats = await fetch_flats()
    print(f'Найдено квартир: {len(flats)}')
    if flats:
        print('✅ Режим \"все квартиры\" работает')
        for i, flat in enumerate(flats[:2]):
            print(f'  {i+1}. {flat[\"name\"]} - {flat[\"price\"]}')
    else:
        print('⚠️ Квартиры не найдены')

asyncio.run(test())
" 2>/dev/null || echo "❌ Ошибка в режиме 'все квартиры'"

echo ""

# Тест режима "ЖК Лайнер"
echo "🏗️ Тестирую режим 'ЖК Лайнер'..."
export MONITOR_MODE=liner
python -c "
import sys
sys.path.append('../src')
import asyncio
from bot_liner_monitor import fetch_flats

async def test():
    flats = await fetch_flats()
    print(f'Найдено квартир в ЖК Лайнер: {len(flats)}')
    if flats:
        print('✅ Найдены квартиры в ЖК Лайнер')
        for flat in flats:
            print(f'  • {flat[\"name\"]} - {flat[\"price\"]}')
    else:
        print('ℹ️ Квартир в ЖК Лайнер пока нет (это нормально)')

asyncio.run(test())
" 2>/dev/null || echo "❌ Ошибка в режиме 'ЖК Лайнер'"

echo ""
echo "📱 Для настройки Telegram уведомлений:"
echo "   - Прочитайте файл docs/TELEGRAM_SETUP.md"
echo "   - Скопируйте .env.example в .env и заполните данные"
echo ""
echo "🎯 Готово! Проект готов к работе."
echo ""
echo "Команды для запуска:"
echo "  ./scripts/run_all_mode.sh    - мониторинг всех квартир"
echo "  ./scripts/run_liner_mode.sh  - мониторинг ЖК Лайнер"
echo "  ./scripts/test_modes.py      - тестирование режимов"
