import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # Ссылка (меняй ID только здесь для теста)
    # Петер Ярош: Q12044733 | Франц Кафка: Q460
    target_id = "Q460" 
    wiki_url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
    
    headers = {'User-Agent': 'JarosStatusBot/1.0'}

    try:
        response = requests.get(wiki_url, headers=headers)
        data = response.json()
        
        # Автоматически берем данные по тому ID, который указан в ссылке
        entity = data['entities'][target_id]
        claims = entity.get('claims', {})
        
        # Проверяем наличие даты смерти (P570)
        is_alive = 'P570' not in claims
        
        if is_alive:
            msg = f"🇸🇰 Статус объекта {target_id}: Жив. Все в порядке."
        else:
            msg = f"❗ Внимание! У объекта {target_id} обнаружена дата смерти в Wikidata."

        # Отправка в TG
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        print(f"Запрос выполнен для {target_id}. Сообщение отправлено.")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
