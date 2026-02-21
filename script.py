import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460) — должен выдать ТРЕВОГУ
    # РАБОЧИЙ: Петер Ярош (Q12044733) — должен быть "ЖИВ"
    target_id = "Q460" 

    # Используем официальный API для получения полных данных (claims)
    api_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": target_id,
        "format": "json",
        "props": "claims"
    }
    
    headers = {'User-Agent': 'JarosStatusBot/1.0'}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        
        # Получаем список утверждений (claims)
        entity = data.get('entities', {}).get(target_id, {})
        claims = entity.get('claims', {})
        
        # Проверяем наличие свойства P570 (дата смерти)
        if "P570" in claims:
            print(f"DEBUG: Метка смерти P570 НАЙДЕНА для {target_id}")
            msg = f"❗ Внимание! У объекта {target_id} обнаружена дата смерти в Wikidata."
        else:
            print(f"DEBUG: Метка смерти P570 НЕ найдена для {target_id}")
            msg = f"🇸🇰 Статус объекта {target_id}: Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Ошибка в скрипте: {e}")

if __name__ == "__main__":
    check()
