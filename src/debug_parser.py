#!/usr/bin/env python3
"""
debug_parser.py
Отладочная версия для проверки парсинга сайта
"""

import asyncio
from playwright.async_api import async_playwright
import os

BASE_URL = "https://xn--80aald4bq.xn--d1aqf.xn--p1ai"

async def debug_parse():
    """Отладочная функция для проверки парсинга"""
    
    # Пробуем разные URL
    urls = {
        "all": f"{BASE_URL}/catalog/filter/place_id-is-moskva/apply/?sort=price_asc",
        "liner": f"{BASE_URL}/catalog/filter/place_id-is-moskva/complex_id-is-liner/room-is-studiya-or-1-komnatnaya/price-from-64600-to-113684/apply/?sort=price_asc",
        "simple": f"{BASE_URL}/catalog/"
    }
    
    for mode, url in urls.items():
        print(f"\n{'='*60}")
        print(f"🧪 Тестирую URL ({mode}): {url}")
        print(f"{'='*60}")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)  # Включаем UI для отладки
                
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                )
                
                page = await context.new_page()
                
                print("📡 Загружаю страницу...")
                await page.goto(url, timeout=60000, wait_until="networkidle")
                
                print("⏳ Жду загрузки контента...")
                await asyncio.sleep(5)
                
                # Проверяем заголовок страницы
                title = await page.title()
                print(f"📄 Заголовок страницы: {title}")
                
                # Проверяем наличие основных элементов
                print("🔍 Ищу основные элементы...")
                
                # Проверяем Vue компонент
                vue_check = await page.evaluate('''
                    () => {
                        const catalogFilter = document.querySelector('.js--catalog-filter');
                        if (catalogFilter && catalogFilter.__vue__) {
                            const vue = catalogFilter.__vue__;
                            return {
                                hasVue: true,
                                hasRenderData: !!(vue.renderData),
                                hasItems: !!(vue.renderData && vue.renderData.items),
                                itemsCount: (vue.renderData && vue.renderData.items) ? vue.renderData.items.length : 0
                            };
                        }
                        return { hasVue: false };
                    }
                ''')
                
                print(f"🎭 Vue компонент: {vue_check}")
                
                # Проверяем DOM элементы
                dom_check = await page.evaluate('''
                    () => {
                        const selectors = [
                            '.catalog-card',
                            '[class*="card"]',
                            '.layout-card',
                            '.apartment-card',
                            '.flat-card'
                        ];
                        
                        const results = {};
                        for (const selector of selectors) {
                            const elements = document.querySelectorAll(selector);
                            results[selector] = elements.length;
                        }
                        
                        return results;
                    }
                ''')
                
                print(f"🏗️ DOM элементы: {dom_check}")
                
                # Ищем текст с ценами
                price_check = await page.evaluate('''
                    () => {
                        const allText = document.body.innerText;
                        const priceMatches = allText.match(/\d+\s*₽/g) || [];
                        return {
                            foundPrices: priceMatches.length,
                            examples: priceMatches.slice(0, 5)
                        };
                    }
                ''')
                
                print(f"💰 Найдено цен: {price_check}")
                
                # Сохраняем скриншот для анализа
                screenshot_path = f"debug_screenshot_{mode}.png"
                await page.screenshot(path=screenshot_path, full_page=True)
                print(f"📸 Сохранен скриншот: {screenshot_path}")
                
                # Сохраняем HTML для анализа
                html_content = await page.content()
                with open(f"debug_page_{mode}.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"💾 Сохранен HTML: debug_page_{mode}.html")
                
                await browser.close()
                
                print(f"✅ Тест {mode} завершен")
                
        except Exception as e:
            print(f"❌ Ошибка в тесте {mode}: {e}")

if __name__ == "__main__":
    print("🚀 Запускаю отладку парсера...")
    asyncio.run(debug_parse())
    print("\n🎉 Отладка завершена! Проверьте файлы debug_* для анализа.")
