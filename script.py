import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # Список для проверки: ID и понятное нам имя
    targets = {
        "Q512": "Владимир Высоцкий",
        "Q9682": "Елизавета II",
        "Q12044733": "Петер Ярош"
    }

    results = []

    for target_id, t_name in targets.items():
        # Используем самый надежный метод получения данных
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
        headers = {'User-Agent': 'StatusCheckerBot/3.0 (https://github.com/yourusername)'}

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            entity = data.get('entities', {}).get(target_id, {})
            claims = entity.get('claims', {})
            
            # Ищем P570 (дата смерти)
            death_info = claims.get('P570')

            if death_info:
                raw_date = death_info[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('time', '')
                clean_date = raw_date.lstrip('+').split('T')[0] if raw_date else "дата не указана"
                results.append(f"❌ {t_name}: Мертв ({clean_date})")
            else:
                results.append(f"✅ {t_name}: Жив")
                
        except Exception as e:
            results.append(f"⚠️ {t_name}: Ошибка запроса")

    # Формируем итоговое сообщение
    full_msg = "📊 **Отчет мониторинга:**\n\n" + "\n".join(results)
    
    # Отправка в Telegram
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  json={"chat_id": chat_id, "text": full_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    check()
