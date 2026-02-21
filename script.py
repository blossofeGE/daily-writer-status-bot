import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460) - должен быть "Мертв"
    # РАБОЧИЙ: Петер Ярош (Q12044733) - должен быть "Жив"
    target_id = "Q460" 
    
    wiki_url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
    headers = {'User-Agent': 'JarosStatusBot/1.0'}

    try:
        response = requests.get(wiki_url, headers=headers)
        data = response.json()
        
        # Заходим внутрь JSON структуры Wikidata
        entity = data.get('entities', {}).get(target_id, {})
        claims = entity.get('claims', {})
        
        # P570 — это свойство "date of death"
        death_date_info = claims.get('P570')
        
        if death_date_info:
            print(f"DEBUG: Найдена дата смерти для {target_id}")
            msg = f"❗ Внимание! У объекта {target_id} (Кафка/Ярош) обнаружена дата смерти в Wikidata."
        else:
            print(f"DEBUG: Дата смерти для {target_id} НЕ найдена")
            msg = f"🇸🇰 Статус объекта {target_id}: Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
