import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # ТЕСТ: Владимир Высоцкий (Q512)
    # РАБОЧИЙ: Петер Ярош (Q12044733)
    target_id = "Q9682" 

    url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        entity = data.get('entities', {}).get(target_id, {})
        claims = entity.get('claims', {})
        
        # Получаем имя для отчета
        name = entity.get('labels', {}).get('ru', {}).get('value', target_id)
        
        # Проверяем дату смерти (P570)
        death_info = claims.get('P570')

        if death_info:
            # Вытаскиваем сырую дату (она там в формате +1980-07-25T00:00:00Z)
            raw_date = death_info[0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('time', '')
            # Очищаем: убираем лишние плюсы и время
            clean_date = raw_date.lstrip('+').split('T')[0] if raw_date else "Дата не указана"
            
            print(f"✅ DEBUG: {name} найден. Дата смерти в базе: {clean_date}")
            msg = f"❗ Внимание! У объекта {name} ({target_id}) обнаружена дата смерти: {clean_date}"
        else:
            print(f"ℹ️ DEBUG: {name} найден. Дата смерти отсутствует.")
            msg = f"🇸🇰 Статус объекта {name}: Жив. Все в порядке."

        # Отправка в Telegram
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                      json={"chat_id": chat_id, "text": msg})
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    check()
