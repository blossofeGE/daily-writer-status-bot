import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460) - должен выдать тревогу
    # РАБОЧИЙ: Петер Ярош (Q12044733) - должен быть "Жив"
    target_id = "Q460" 
    
    wiki_url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
    headers = {'User-Agent': 'JarosStatusBot/1.0'}

    try:
        response = requests.get(wiki_url, headers=headers)
        text_data = response.text # Берем сырой текст ответа
        
        # Если в тексте вообще встречается "P570" (код даты смерти в Wikidata)
        if '"P570"' in text_data:
            print(f"DEBUG: Метка смерти P570 найдена в тексте для {target_id}")
            msg = f"❗ Внимание! У объекта {target_id} обнаружены критические изменения (дата смерти) в Wikidata."
        else:
            print(f"DEBUG: Метка смерти P570 не обнаружена для {target_id}")
            msg = f"🇸🇰 Статус объекта {target_id}: Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
