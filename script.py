import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460)
    # РАБОЧИЙ: Петер Ярош (Q12044733)
    target_id = "Q460" 

    # SPARQL-запрос: достаем имя и дату смерти напрямую из мозга Wikidata
    query = f"""
    SELECT ?itemLabel ?death WHERE {{
      BIND(wd:{target_id} AS ?item)
      OPTIONAL {{ ?item wdt:P570 ?death. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
    }}
    """
    
    url = "https://query.wikidata.org/sparql"
    headers = {
        'User-Agent': 'JarosChecker/2.0',
        'Accept': 'application/sparql-results+json'
    }

    try:
        response = requests.get(url, params={'query': query, 'format': 'json'}, headers=headers)
        data = response.json()
        results = data.get('results', {}).get('bindings', [])

        if results:
            res = results[0]
            name = res.get('itemLabel', {}).get('value', 'Неизвестно')
            death_date = res.get('death', {}).get('value')

            if death_date:
                print(f"DEBUG: Нашел объект {name}. Дата смерти: {death_date}")
                msg = f"❗ ТРЕВОГА! Объект {name} ({target_id}) — найдена дата смерти: {death_date}"
            else:
                print(f"DEBUG: Нашел объект {name}. Дата смерти отсутствует.")
                msg = f"🇸🇰 Статус объекта {name}: Жив. Все в порядке."
        else:
            msg = f"⚠️ Ошибка: Wikidata не нашла объект {target_id} через SPARQL."

        # Отправка в TG
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
