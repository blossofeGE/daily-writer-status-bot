import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # Wikidata ID Петера Яроша
    wiki_url = "https://www.wikidata.org/wiki/Special:EntityData/Q12044733.json"
    # Добавляем заголовок, чтобы Wikidata нас не банила
    headers = {'User-Agent': 'JarosStatusBot/1.0 (contact: your_email@example.com)'}

    try:
        response = requests.get(wiki_url, headers=headers)
        print(f"Статус ответа Wikidata: {response.status_code}")
        
        if response.status_code != 200:
            print("Ошибка: Wikidata не ответила кодом 200")
            return

        data = response.json()
        claims = data['entities']['Q12044733']['claims']
        
        if 'P570' not in claims:
            msg = "🇸🇰 Петер Ярош жив. Все в порядке."
        else:
            msg = "❗ Внимание: В данных Петера Яроша появились изменения."

        # Отправка в TG
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        tg_res = requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        print(f"Статус отправки в Telegram: {tg_res.status_code}")
        if tg_res.status_code != 200:
            print(f"Детали ошибки TG: {tg_res.text}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    check()
