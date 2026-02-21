import requests
import os
import time

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    target_id = "Q12044733" # Петер Ярош

    # 1. Попытка через основной API (wbgetentities)
    api_url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={target_id}&format=json&props=labels|claims"
    headers = {'User-Agent': 'JarosGuardBot/2.0 (Contact: your_email@example.com)'}

    try:
        res = requests.get(api_url, headers=headers).json()
        entity = res.get('entities', {}).get(target_id, {})
        
        # Если данных нет, пробуем второй метод (Special:EntityData)
        if not entity or 'claims' not in entity:
            print(f"DEBUG: Первый метод не дал данных для {target_id}. Пробую второй...")
            time.sleep(1) # Небольшая пауза
            alt_url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
            res = requests.get(alt_url, headers=headers).json()
            entity = res.get('entities', {}).get(target_id, {})

        # Проверяем результат
        labels = entity.get('labels', {})
        name = labels.get('ru', {}).get('value') or labels.get('en', {}).get('value') or target_id
        claims = entity.get('claims', {})

        if not claims:
            msg = f"⚠️ Ошибка: Wikidata не отдала данные для {name}. Проверка невозможна."
            print(f"DEBUG: Claims пустые для {target_id}")
        elif "P570" in claims:
            death_date = claims["P570"][0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('time', 'неизвестно')
            clean_date = death_date.lstrip('+').split('T')[0]
            msg = f"❗ Внимание! У объекта {name} обнаружена дата смерти: {clean_date}"
        else:
            msg = f"🇸🇰 Статус объекта {name}: Жив. Все в порядке."

        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    check()
