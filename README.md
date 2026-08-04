# Daily Writer Status Bot

Telegram-бот на Python, который ежедневно получает данные о выбранном человеке через API Wikidata, определяет наличие информации о смерти и отправляет результат в Telegram.

## Возможности

- Получение данных через API Wikidata
- Обработка JSON-ответов
- Автоматический ежедневный запуск через GitHub Actions
- Отправка уведомлений через Telegram Bot API
- Обработка ошибок сети и API

## Стек

- Python
- Requests
- Telegram Bot API
- Wikidata API
- GitHub Actions

## Структура проекта

```
.
├── script.py
└── .github/
    └── workflows/
```

## Запуск

```bash
pip install -r requirements.txt
python script.py
```
