# WikiSearch-Bot
---
# РУССКИЙ
## WikiSearch-Bot

WikiSearch-Bot — это Telegram-бот, который превращает поиск информации в мгновенное удовольствие.

### Как это работает
**Ты даёшь боту:**
- Любую тему или категорию (например: "Minecraft", "История Рима").
- Опционально: указываешь, что хочешь всю категорию.

**Бот тебе даёт:**
- Краткий summary статьи.
- Полную статью в текстовом файле.
- Если тема — категория, архив со всеми статьями.
- Автоматический выбор источника: фандом для игр, Википедия для общего.

### Функционал
- Быстрый summary статьи.
- Полная статья в текстовом файле.
- Архив статей для категорий.
- Автоматический выбор источника: фандом для игр, Википедия для общего.

### Технологии
- [Python 3.11+](https://python.org/)
- [aiogram (Telegram API) (3)](https://aiogram.dev/)
- [wikipediaapi](https://pypi.org/project/Wikipedia-API/), [fandom-py](https://pypi.org/project/fandom-py/)
- [google-genai](https://pypi.org/project/google-genai/)


### Установка
* 1. Склонируйте репозиторий
* 2. Установите зависимости:
> ```pip install -r requirements.txt```
* 3. Настройте `.env`:
> TELEGRAM_API (Токен вашего бота) 
> GEMINI_API (Токен Gemini)
> PROJECT_NAME (Название проекта)
> EMAIL (Ваша почта)
* 4. Запустите бота:
> ```python main.py```


### Использование
1. Откройте Telegram и найдите бота.
2. Нажмите «Начать».
3. Введите тему или категорию.
4. Получите summary и текстовые файлы.

## WikiSearch Bot

WikiSearch is a Telegram bot that makes finding information fast and easy.

### How it works
**You give the bot:**
- Any topic or category (e.g., "Minecraft", "History of Rome")
- Optionally: ask for the full category

**The bot gives you:**
- Quick summary of the article
- Full article as a text file
- Archive of all articles if it’s a category
- Automatic source selection: fandom for games, Wikipedia for general topics

### Features
- Quick summary of any article
- Full article in a text file
- Archive of articles for categories
- Automatic source selection: fandom for games, Wikipedia for general topics

### Tech Stack
- [Python 3.11+](https://python.org/)
- [aiogram (Telegram API) (3)](https://aiogram.dev/)
- [wikipediaapi](https://pypi.org/project/Wikipedia-API/), [fandom-py](https://pypi.org/project/fandom-py/)
- [google-genai](https://pypi.org/project/google-genai/)

### Installation
* 1. Clone the repository
* 2. Install dependencies:
> ```pip install -r requirements.txt```
* 3. Setup `.env`:
> TELEGRAM_API (Your bot's Telegram token)
> GEMINI_API (Your Gemini API token)
> PROJECT_NAME (Project name)
> EMAIL (Your email)
* 4. Run the bot:
> ```python main.py```

### Usage
1. Open Telegram and find the bot.
2. Press "Start".
3. Enter a topic or category.
4. Receive summaries and text files.
