#!/bin/bash
# run_all_mode.sh - Запуск мониторинга всех квартир в Москве

echo "🚀 Запускаю мониторинг всех квартир в Москве..."

export MONITOR_MODE=all
export CHECK_INTERVAL=60

python ../src/bot_liner_monitor.py
