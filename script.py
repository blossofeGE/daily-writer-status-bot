import requests
import os

def check():
    print(f"Пытаюсь отправить сообщение на ID: {chat_id[:4]}***") # Покажет начало ID в логах
    # Проверка, не пустые ли переменные
    if not token or not chat_id:
        print("Ошибка: Токен или ID пустые!")
        return
    # Тянем данные о Петере Яроше из Wikidata
    url = "https://www.wikidata.org/wiki/Special:EntityData/Q12044733.json"
    
    # Берем наши токены из "секретов" GitHub
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    try:
        response = requests.get(url).json()
        # Ищем блок утверждений (claims)
        claims = response['entities']['Q12044733']['claims']
        
        # P570 — это стандартный код свойства "дата смерти" в Wikidata
        if 'P570' not in claims:
            status_text = "🇸🇰 Петер Ярош жив. Все в порядке."
        else:
            status_text = "❗ Внимание! В карточке Петера Яроша зафиксированы изменения (дата смерти)."
            
        # Отправляем в Telegram
        send_url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(send_url, json={"chat_id": chat_id, "text": status_text})
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check()
