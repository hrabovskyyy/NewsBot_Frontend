import aiohttp
from config import API_BASE_URL

async def get_top_headlines(country="ua", category="general", page_size=5):
    url = f"{API_BASE_URL}/News/public?country={country}&category={category}&pageSize={int(page_size)}"
    print(f"🔗 Запит: {url}")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"📡 Статус відповіді: {resp.status}")
            if resp.status == 200:
                data = await resp.json()
                print(f"📊 Тип відповіді: {type(data)}")
                print(f"🔍 Ключі: {list(data.keys())}")

                articles = data.get("articles", [])  # <- тут точно має бути словник
                print(f"📦 Отримано {len(articles)} новин")
                return articles
            else:
                print(f"❌ Помилка: статус {resp.status}")
            return []

# ✅ Пошук новин (API повертає словник з ключем articles)
async def search_news(query: str):
    url = f"{API_BASE_URL}/news/search?q={query}&sortBy=publishedAt"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"🔍 Запит пошуку новин: {url}")
            if resp.status == 200:
                data = await resp.json()
                print(f"🔎 Знайдено: {len(data.get('articles', []))} новин")
                return data.get("articles", [])
            else:
                print(f"❌ Помилка при пошуку новин: статус {resp.status}")
            return []

# ✅ Улюблені новини
async def get_favorites_by_user(telegram_user_id: str):
    url = f"{API_BASE_URL}/Favorites/user/{telegram_user_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"📦 Отримання улюблених для {telegram_user_id}, статус: {resp.status}")
            if resp.status == 200:
                return await resp.json()
            else:
                print(f"❌ Не вдалося отримати улюблені новини")
            return []

async def add_favorite(title: str, url: str, telegram_user_id: str):
    payload = {
        "title": title,
        "url": url,
        "telegramUserId": telegram_user_id
    }
    url_api = f"{API_BASE_URL}/Favorites"
    async with aiohttp.ClientSession() as session:
        async with session.post(url_api, json=payload) as resp:
            print(f"⭐ Додавання в улюблені, статус: {resp.status}")
            return resp.status == 201

async def delete_favorite(fav_id: str):
    url = f"{API_BASE_URL}/favorites/{fav_id}"
    async with aiohttp.ClientSession() as session:
        async with session.delete(url) as resp:
            print(f"🗑 Видалення з улюблених {fav_id}, статус: {resp.status}")
            return resp.status == 204