import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Франц Кафка (Q460) — должен выдать ТРЕВОГУ
    # РАБОЧИЙ: Петер Ярош (Q12044733) — должен быть "ЖИВ"
    target_id = "Q460" 

    # 1. Сначала узнаем актуальный ID (на случай редиректов)
    search_url = f"https://www.wikidata.org/w/api.php"
    search_params = {
        "action": "wbgetentities",
        "ids": target_id,
        "format": "json",
        "redirects": "yes"
    }
    
    headers = {'User-Agent': 'JarosStatusBot/1.1 (https://github.com/yourusername)'}

    try:
        # Получаем реальный ID (если Q460 перенаправляет куда-то еще)
        res = requests.get(search_url, params=search_params, headers=headers).json()
        real_id = list(res.get('entities', {}).keys())[0]
        
        # 2. Запрашиваем конкретно свойство P570 (дата смерти)
        claims_url = "https://www.wikidata.org/w/api.php"
        claims_params = {
            "action": "wbgetclaims",
            "entity": real_id,
            "property": "P570",
            "format": "json"
        }
        
        claims_res = requests.get(claims_url, params=claims_params, headers=headers).json()
        
        # Если в ответе есть ключ 'claims' и он не пустой — дата смерти существует
        death_claims = claims_res.get('claims', {})
        
        if death_claims and 'P570' in death_claims:
            print(f"DEBUG: Метка смерти P570 НАЙДЕНА для {real_id}")
            msg = f"❗ Внимание! У объекта {target_id} обнаружена дата смерти в Wikidata."
        else:
            print(f"DEBUG: Метка смерти P570 НЕ найдена для {real_id}")
            msg = f"🇸🇰 Статус объекта {target_id}: Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    check()
