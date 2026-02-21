import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460) — ДОЛЖЕН ВЫДАТЬ ТРЕВОГУ
    # РАБОЧИЙ: Петер Ярош (Q12044733) — ДОЛЖЕН БЫТЬ "ЖИВ"
    target_id = "Q460" 

    # Прямой запрос к конкретному заявлению (claim) о дате смерти
    api_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetclaims",
        "entity": target_id,
        "property": "P570", # Спрашиваем ТОЛЬКО про дату смерти
        "format": "json"
    }
    
    headers = {'User-Agent': 'JarosStatusBot/1.3 (https://github.com/yourusername)'}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        
        # Если в ответе есть ключ 'claims' и в нем есть 'P570' — значит дата смерти ЗАПИСАНА
        claims = data.get('claims', {})
        
        if "P570" in claims:
            print(f"✅ DEBUG: Дата смерти (P570) для {target_id} НАЙДЕНА.")
            msg = f"❗ Внимание! У объекта {target_id} обнаружена дата смерти в Wikidata."
        else:
            # Проверка: а есть ли вообще такой объект, чтобы исключить ошибку API
            test_res = requests.get(api_url, params={"action":"wbgetentities","ids":target_id,"props":"labels","format":"json"}, headers=headers).json()
            name = test_res.get('entities', {}).get(target_id, {}).get('labels', {}).get('ru', {}).get('value', 'Неизвестный')
            
            print(f"ℹ️ DEBUG: Дата смерти для {target_id} ({name}) отсутствует в базе.")
            msg = f"🇸🇰 Статус объекта {target_id} ({name}): Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check()
