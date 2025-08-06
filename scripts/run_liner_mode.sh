#!/bin/bash
# run_liner_mode.sh - Запуск мониторинга только ЖК Лайнер

echo "🚀 Запускаю мониторинг ЖК Лайнер..."

export MONITOR_MODE=liner
export CHECK_INTERVAL=60

python ../src/bot_liner_monitor.py
