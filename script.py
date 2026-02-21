import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # Список для проверки
    targets = {
        "Q512": "Владимир Высоцкий",
        "Q9682": "Елизавета II",
        "Q12044733": "Петер Ярош"
    }

    results = []

    for target_id, t_name in targets.items():
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
        headers = {'User-Agent': 'StatusCheckerBot/4.0'}

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            entity = data.get('entities', {}).get(target_id, {})
            claims = entity.get('claims', {})
            
            # 1. ПРОВЕРКА НА КОРРЕКТНОСТЬ ОБЪЕКТА (P31 == Q5 означает 'человек')
            instance_of = claims.get('P31', [{}])[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id')
            
            if instance_of != "Q5":
                results.append(f"⚠️ {t_name}: Ошибка! Это не человек (ID: {instance_of}). Проверьте ID!")
                continue

            # 2. ПРОВЕРКА НА ПУСТОЙ JSON (должна быть хотя бы дата рождения P569)
            if 'P569' not in claims:
                results.append(f"⚠️ {t_name}: Получены неполные данные (нет даты рождения).")
                continue

            # 3. ПРОВЕРКА НА СМЕРТЬ (P570)
            death_info = claims.get('P570')

            if death_info:
                raw_date = death_info[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('time', '')
                clean_date = raw_date.lstrip('+').split('T')[0]
                results.append(f"❌ {t_name}: Мертв ({clean_date})")
            else:
                results.append(f"✅ {t_name}: Жив")
                
        except Exception as e:
            results.append(f"⚠️ {t_name}: Критическая ошибка запроса")

    full_msg = "📊 **Валидированный отчет:**\n\n" + "\n".join(results)
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": full_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    check()
