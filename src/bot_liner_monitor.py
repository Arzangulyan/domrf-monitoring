"""
bot_liner_monitor.py
Мониторинг свободных квартир в ЖК «Лайнер» (аренда.дом.рф)
"""

import os, json, hashlib, asyncio, time, signal
import schedule, requests, re
from datetime import datetime
from playwright.async_api import async_playwright

# --- Константы --------------------------------------------------------------
BASE_URL = "https://xn--80aald4bq.xn--d1aqf.xn--p1ai"

# Режимы мониторинга
MONITOR_MODE = os.getenv("MONITOR_MODE", "all")  # "all" или "liner"

# URL для разных режимов
URLS = {
    "all": f"{BASE_URL}/catalog/filter/place_id-is-moskva/apply/?sort=price_asc",
    "liner": f"{BASE_URL}/catalog/filter/place_id-is-moskva/complex_id-is-liner/room-is-studiya-or-1-komnatnaya/price-from-64600-to-113684/apply/?sort=price_asc"
}

URL = URLS[MONITOR_MODE]
STATE_FILE = f"state_{MONITOR_MODE}.json"
CHECK_EVERY_MIN = int(os.getenv("CHECK_INTERVAL", "60"))

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT = os.getenv("TG_CHAT_ID")

# --- Вспомогательные функции -------------------------------------------------
def md5(obj: list) -> str:
    data = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    return hashlib.md5(data.encode()).hexdigest()

def clean_price(price_str: str) -> str:
    """Очищает цену от HTML и лишних символов"""
    if not price_str:
        return "Цена не указана"
    # Убираем HTML теги
    price_clean = re.sub(r'<[^>]+>', ' ', str(price_str))
    price_clean = re.sub(r'\s+', ' ', price_clean).strip()
    return price_clean

async def fetch_flats() -> list[dict]:
    """Возвращает список квартир из каталога."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            page = await context.new_page()
            await page.goto(URL, timeout=60000, wait_until="networkidle")
            
            # Ждем загрузки компонента каталога
            await page.wait_for_selector('.js--catalog-filter', timeout=30000)
            
            # Ждем немного для полной загрузки данных
            await asyncio.sleep(3)
            
            # Получаем данные из Vue компонента или DOM
            apartments_data = await page.evaluate('''
                () => {
                    try {
                        // Пытаемся найти Vue компонент с данными
                        const catalogFilter = document.querySelector('.js--catalog-filter');
                        if (catalogFilter && catalogFilter.__vue__) {
                            const vueInstance = catalogFilter.__vue__;
                            
                            // Проверяем разные возможные пути к данным
                            let items = null;
                            if (vueInstance.renderData && vueInstance.renderData.items) {
                                items = vueInstance.renderData.items;
                            } else if (vueInstance.$data && vueInstance.$data.renderData && vueInstance.$data.renderData.items) {
                                items = vueInstance.$data.renderData.items;
                            } else if (vueInstance.filtersData && vueInstance.filtersData.items) {
                                items = vueInstance.filtersData.items;
                            }
                            
                            if (items && items.length > 0) {
                                console.log('Found Vue data:', items.length, 'items');
                                return items;
                            }
                        }
                        
                        // Альтернативный способ - ищем все элементы на странице
                        const items = [];
                        
                        // Ищем разные варианты селекторов
                        const selectors = [
                            '.catalog-card',
                            '[class*="card"]',
                            '.layout-card',
                            '.apartment-card',
                            '.flat-card'
                        ];
                        
                        let cards = [];
                        for (const selector of selectors) {
                            cards = document.querySelectorAll(selector);
                            if (cards.length > 0) {
                                console.log('Found cards with selector:', selector, cards.length);
                                break;
                            }
                        }
                        
                        cards.forEach((card, index) => {
                            // Ищем разные варианты элементов
                            const titleSelectors = [
                                '[class*="title"]',
                                'h2', 'h3', 'h4',
                                '.name',
                                '[class*="name"]'
                            ];
                            
                            const priceSelectors = [
                                '[class*="price"]',
                                '.cost',
                                '[class*="cost"]'
                            ];
                            
                            const areaSelectors = [
                                '[class*="area"]',
                                '[class*="square"]',
                                '.size'
                            ];
                            
                            let titleEl = null, priceEl = null, areaEl = null;
                            
                            for (const selector of titleSelectors) {
                                titleEl = card.querySelector(selector);
                                if (titleEl) break;
                            }
                            
                            for (const selector of priceSelectors) {
                                priceEl = card.querySelector(selector);
                                if (priceEl) break;
                            }
                            
                            for (const selector of areaSelectors) {
                                areaEl = card.querySelector(selector);
                                if (areaEl) break;
                            }
                            
                            const linkEl = card.querySelector('a[href*="/catalog/"]') || card.querySelector('a');
                            
                            if (titleEl && priceEl) {
                                const item = {
                                    id: 'item_' + index,
                                    name: titleEl.textContent.trim(),
                                    price: priceEl.textContent.trim(),
                                    area_total: areaEl ? areaEl.textContent.trim() : '',
                                    detail_page_url: linkEl ? linkEl.getAttribute('href') : '',
                                    apartment_count: 1,
                                    complex_name: ''
                                };
                                
                                // Ищем название комплекса
                                const complexSelectors = [
                                    '[class*="complex"]',
                                    '[class*="address"]',
                                    '.location'
                                ];
                                
                                for (const selector of complexSelectors) {
                                    const complexEl = card.querySelector(selector);
                                    if (complexEl) {
                                        item.complex_name = complexEl.textContent.trim();
                                        break;
                                    }
                                }
                                
                                items.push(item);
                            }
                        });
                        
                        console.log('DOM parsing result:', items.length, 'items');
                        return items;
                        
                    } catch (e) {
                        console.error('Error extracting data:', e);
                        return [];
                    }
                }
            ''')
            
            await browser.close()
            
            # Обрабатываем полученные данные
            flats = []
            if apartments_data:
                for item in apartments_data:
                    flat = {
                        "id": item.get("id", "unknown"),
                        "name": item.get("name", "Без названия"),
                        "price": clean_price(item.get("price", "")),
                        "area": str(item.get("area_total", "")).replace(" м²", "").strip(),
                        "complex": item.get("complex_name", "ЖК Лайнер" if MONITOR_MODE == "liner" else "Москва"),
                        "url": f"{BASE_URL}{item.get('detail_page_url', '')}" if item.get("detail_page_url") else "",
                        "apartment_count": item.get("apartment_count", 1)
                    }
                    flats.append(flat)
            
            print(f"Найдено квартир: {len(flats)}")
            return flats
            
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return []

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"hash": None, "count": 0, "last_flats": []}

def save_state(h, cnt, flats_data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"hash": h, "count": cnt, "last_flats": flats_data, "last_check": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)

def tg_notify(text: str):
    if not TG_TOKEN or not TG_CHAT:
        print("Telegram не настроен, сообщение пропущено")
        print(f"Сообщение: {text}")
        return
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            data={"chat_id": TG_CHAT, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
        if response.status_code == 200:
            print("Уведомление отправлено в Telegram")
        else:
            print(f"Ошибка отправки в Telegram: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при отправке в Telegram: {e}")

# --- Основная проверка -------------------------------------------------------
async def check_once():
    print(f"[{datetime.now():%H:%M:%S}] Запускаю проверку…")
    
    try:
        flats = await fetch_flats()
        
        if not flats:
            print("Не удалось получить данные о квартирах")
            return
        
        h_now = md5(flats)
        state = load_state()
        
        if state["hash"] is None:  # первый запуск
            mode_name = "ЖК Лайнер" if MONITOR_MODE == "liner" else "все квартиры в Москве"
            message = f"🤖 Мониторинг запущен ({mode_name})\n\n📊 Найдено квартир: {len(flats)}\n\n"
            if flats:
                message += "Текущие предложения:\n"
                for flat in flats[:5]:  # показываем первые 5
                    message += f"• {flat['name']} — {flat['price']}"
                    if flat['area']:
                        message += f" — {flat['area']} м²"
                    if flat['complex'] and flat['complex'] != "Москва":
                        message += f" ({flat['complex']})"
                    message += "\n"
            tg_notify(message)
            
        elif h_now != state["hash"]:
            delta = len(flats) - state["count"]
            mode_name = "ЖК Лайнер" if MONITOR_MODE == "liner" else "Москва"
            
            if delta > 0:
                head = f"🆕 Появились новые квартиры ({mode_name})!"
                new_flats = flats[-delta:]  # берем последние добавленные
            elif delta < 0:
                head = f"⚠️ Часть квартир больше недоступна ({mode_name})"
                new_flats = flats[:3]  # показываем первые доступные
            else:
                head = f"🔄 Обновлена информация о квартирах ({mode_name})"
                new_flats = flats[:3]
            
            message = f"{head}\n\n📊 Всего доступно: {len(flats)} кв.\n\n"
            
            for flat in new_flats[:5]:  # максимум 5 квартир
                message += f"🏠 {flat['name']}\n"
                message += f"💰 {flat['price']}\n"
                if flat['area']:
                    message += f"📐 {flat['area']} м²\n"
                if flat['complex'] and flat['complex'] not in ["Москва", "ЖК Лайнер"]:
                    message += f"🏢 {flat['complex']}\n"
                if flat['url']:
                    message += f"🔗 <a href='{flat['url']}'>Подробнее</a>\n"
                message += "\n"
            
            tg_notify(message)
        else:
            print("Изменений не обнаружено")
        
        save_state(h_now, len(flats), flats)
        
    except Exception as e:
        print(f"Ошибка при проверке: {e}")
        error_msg = f"❌ Ошибка мониторинга: {str(e)}"
        tg_notify(error_msg)

def job():
    asyncio.run(check_once())

# --- Планировщик -------------------------------------------------------------
mode_name = "ЖК Лайнер" if MONITOR_MODE == "liner" else "все квартиры в Москве"
print(f"🚀 Запускаю бота мониторинга: {mode_name}...")
print(f"🔗 URL: {URL}")
schedule.every(CHECK_EVERY_MIN).minutes.do(job)

# Запускаем первую проверку сразу
job()

def graceful_exit(*_):
    print("Получен сигнал завершения, останавливаю бота...")
    raise SystemExit

signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)

print(f"⏰ Мониторинг запущен. Проверка каждые {CHECK_EVERY_MIN} минут.")
print("Для остановки нажмите Ctrl+C")

while True:
    schedule.run_pending()
    time.sleep(10)
