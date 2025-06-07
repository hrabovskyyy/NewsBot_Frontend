# Telegram-бот для актуальних новин

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-done-brightgreen)

**ХвиляНовин** — це Telegram-бот, який надає свіжі добірки новин з авторитетних світових джерел.  
🟦 Інтерфейс повністю україномовний і побудований виключно на кнопках.

---

## 🔧 Функціонал

- 🗞 Отримання **топ-новин** за країною та категорією
- 🌍 Вибір **країни**: 🇺🇦 Україна, 🇺🇸 США, 🇬🇧 Велика Британія тощо
- 📂 Вибір **категорії**: технології, спорт, бізнес, здоров’я
- ⏱ **Режим**: ручний запит або автоматична щоденна розсилка
- 🔢 Вибір кількості новин: топ-5, топ-10
- 🌐 Деталі новин: заголовок, опис, посилання
- 👍 Реакції: лайк / дизлайк на кожну новину
- 🔍 Пошук за ключовими словами
- 🧠 Побудовано на `aiogram`, підтримка `FSM`, `.env` та `Docker`

---

## 🚀 Запуск локально

1. **Клонувати репозиторій**
```bash
git clone https://github.com/your-username/NewsBot_Frontend.git
cd NewsBot_Frontend
```

2. **Створити `.env` файл**
```env
BOT_TOKEN=your_telegram_bot_token
NEWS_API_KEY=your_newsapi_key
```

3. **Встановити залежності**
```bash
pip install -r requirements.txt
```

4. **Запустити бота**
```bash
python bot.py
```

> 🐳 **Або за допомогою Docker**:
```bash
docker-compose up --build
```

---

## 📁 Структура проєкту

```
hvylianovyn/
├── bot.py                      # Точка входу
├── config.py                   # Налаштування токенів
├── state.py                    # Стейти FSM
├── keyboards/                  # Всі клавіатури
│   ├── main.py
│   ├── countries.py
│   ├── categories.py
│   ├── reactions.py
│   └── search_keyboard.py
├── requirements.txt            # Залежності
├── Dockerfile                  # Docker-інструкції
├── docker-compose.yml          # Compose конфіг
└── .env                        # (не зберігається в репозиторії)
```

---

## 🌐 Використовувані API

- 🔗 [NewsAPI.org](https://newsapi.org/) — джерело актуальних новин

---

## 📜 Ліцензія

Ліцензовано за умовами **MIT License**  
📄 [LICENSE](./LICENSE)

---

## 👤 Автор

👨‍💻 [@hrabovskyy](https://t.me/hrabovskyy) — студент КПІ, розробник Telegram-ботів та API  
