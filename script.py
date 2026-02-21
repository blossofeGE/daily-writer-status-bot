import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460) — ДОЛЖЕН ВЫДАТЬ ТРЕВОГУ
    # РАБОЧИЙ: Петер Ярош (Q12044733) — ДОЛЖЕН БЫТЬ "ЖИВ"
    target_id = "Q460" 

    # Используем API для прямого получения утверждений
    api_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetclaims",
        "entity": target_id,
        "format": "json"
    }
    
    headers = {'User-Agent': 'JarosStatusBot/1.2 (contact: your_email@example.com)'}

    try:
        response = requests.get(api_url, params=params, headers=headers)
        data = response.json()
        
        # Проверяем, получили ли мы вообще список фактов (claims)
        claims = data.get('claims', {})
        
        if not claims:
            # Если пусто, возможно это редирект. Попробуем получить через wbgetentities
            print(f"DEBUG: Раздел claims пуст для {target_id}. Пробую резервный метод...")
            alt_res = requests.get(
                "https://www.wikidata.org/w/api.php", 
                params={"action": "wbgetentities", "ids": target_id, "format": "json", "props": "claims"},
                headers=headers
            ).json()
            entity_data = alt_res.get('entities', {}).get(target_id, {})
            claims = entity_data.get('claims', {})

        # P570 — это дата смерти
        has_death_date = "P570" in claims
        
        if has_death_date:
            print(f"DEBUG: Метка смерти P570 НАЙДЕНА для {target_id}")
            msg = f"❗ Внимание! У объекта {target_id} обнаружена дата смерти в Wikidata."
        else:
            # Если и тут пусто, выводим что именно мы получили для дебага
            print(f"DEBUG: Список ключей в claims: {list(claims.keys())}")
            msg = f"🇸🇰 Статус объекта {target_id}: Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Ошибка в скрипте: {e}")

if __name__ == "__main__":
    check()
