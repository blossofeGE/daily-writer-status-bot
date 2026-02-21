import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Q460 (Должен быть Франц Кафка -> Тревога)
    # РАБОЧИЙ: Q12044733 (Петер Ярош -> Жив)
    target_id = "Q460" 

    # Используем SPARQL - самый точный метод запроса в Wikidata
    query = f"""
    SELECT ?item ?itemLabel ?deathDate WHERE {{
      BIND(wd:{target_id} AS ?item)
      OPTIONAL {{ ?item wdt:P570 ?deathDate. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
    }}
    """
    
    url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'JarosStatusBot/2.0',
        'Accept': 'application/sparql-results+json'
    }

    try:
        response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers)
        data = response.json()
        results = data.get('results', {}).get('bindings', [])

        if results:
            item_info = results[0]
            name = item_info.get('itemLabel', {}).get('value', target_id)
            death_date = item_info.get('deathDate', {}).get('value')

            if death_date:
                print(f"✅ DEBUG: Объект {name} ({target_id}). Дата смерти найдена: {death_date}")
                msg = f"❗ Внимание! У объекта {name} ({target_id}) обнаружена дата смерти: {death_date}"
            else:
                print(f"ℹ️ DEBUG: Объект {name} ({target_id}). Дата смерти НЕ найдена.")
                msg = f"🇸🇰 Статус объекта {name}: Жив. Все в порядке."
        else:
            msg = f"⚠️ Ошибка: Объект {target_id} не найден в базе."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

if __name__ == "__main__":
    check()
