import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # МЕНЯЕМ ПОДОПЫТНОГО: Владимир Высоцкий (Q512) - точно мертв
    # ПЕТЕР ЯРОШ для работы: Q12044733
    target_id = "Q512" 

    # Прямой запрос к JSON без посредников
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Получаем данные объекта
        entity = data.get('entities', {}).get(target_id, {})
        claims = entity.get('claims', {})
        
        # P570 - это дата смерти
        is_dead = "P570" in claims
        
        # Узнаем имя, чтобы понять, кого мы вообще поймали
        name = entity.get('labels', {}).get('ru', {}).get('value', target_id)

        if is_dead:
            print(f"DEBUG: Объект {name} найден. Статус: МЕРТВ (P570 есть)")
            msg = f"❗ Внимание! У объекта {name} ({target_id}) обнаружена дата смерти."
        else:
            print(f"DEBUG: Объект {name} найден. Статус: ЖИВ (P570 нет)")
            msg = f"🇸🇰 Статус объекта {name}: Жив. Все в порядке."

        # Отправка в Telegram
        tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(tg_url, json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
