#!/usr/bin/env python3
"""
test_modes.py
Тестирование разных режимов мониторинга
"""

import os
import asyncio
import subprocess
import sys

def test_mode(mode):
    """Тестирует определенный режим мониторинга"""
    print(f"\n{'='*50}")
    print(f"🧪 Тестирую режим: {mode}")
    print(f"{'='*50}")
    
    # Устанавливаем переменную окружения
    env = os.environ.copy()
    env["MONITOR_MODE"] = mode
    env["CHECK_INTERVAL"] = "1"  # Быстрая проверка для теста
    
    try:
        # Запускаем бота с ограничением по времени
        result = subprocess.run(
            [sys.executable, "../src/bot_liner_monitor.py"],
            env=env,
            timeout=30,  # Максимум 30 секунд на тест
            capture_output=True,
            text=True
        )
        
        print("📤 Вывод:")
        print(result.stdout)
        
        if result.stderr:
            print("❌ Ошибки:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⏰ Тест завершен по таймауту (это нормально)")
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

def main():
    print("🧪 Запускаю тестирование режимов мониторинга...")
    
    # Тестируем режим "все квартиры"
    test_mode("all")
    
    # Небольшая пауза между тестами
    import time
    time.sleep(2)
    
    # Тестируем режим "только ЖК Лайнер"
    test_mode("liner")
    
    print(f"\n{'='*50}")
    print("✅ Тестирование завершено!")
    print("Проверьте вывод выше, чтобы понять, какой режим работает лучше.")

if __name__ == "__main__":
    main()
