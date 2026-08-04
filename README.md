# Daily Writer Status Bot

Telegram-бот на Python, который ежедневно получает данные о выбранном человеке через API Wikidata, определяет наличие информации о смерти и отправляет результат в Telegram.

## Возможности

- получение информации через API Википедии;
- обработка JSON-ответов;
- автоматическая ежедневная отправка сообщений;
- работа с Telegram Bot API.

## Стек

- Python
- Telegram Bot API
- REST API
- JSON

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
