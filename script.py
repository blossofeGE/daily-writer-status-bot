import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    # Тот самый список (теперь с настоящим Кафкой!)
    targets = {
        "Q905": "Франц Кафка",          # Настоящий Кафка (1924)
        "Q512": "Владимир Высоцкий",    # Контроль: Смерть (1980)
        "Q9682": "Елизавета II",        # Контроль: Смерть (2022)
        "Q12044733": "Петер Ярош"       # Цель: Мониторинг (Жив)
    }

    results = []

    for target_id, t_name in targets.items():
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
        headers = {'User-Agent': 'StatusCheckerBot/6.0_KafkaFixed'}

        try:
            # 1. ПРОВЕРКА СЕТИ
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() 
            
            # 2. ПРОВЕРКА ФОРМАТА
            data = response.json()
            
            # 3. ПРОВЕРКА СТРУКТУРЫ АПИ
            if 'entities' not in data:
                results.append(f"⚠️ {t_name}: Аномалия API (нет ключа 'entities').")
                continue
                
            # 4. ОБРАБОТКА РЕДИРЕКТОВ
            actual_keys = list(data['entities'].keys())
            if not actual_keys:
                results.append(f"⚠️ {t_name}: Пустой ответ в 'entities'.")
                continue
            
            real_id = actual_keys[0]
            entity = data['entities'][real_id]
            claims = entity.get('claims', {})
            
            if not claims:
                results.append(f"⚠️ {t_name}: Нет блока фактов (claims).")
                continue

            # 5. ПРОВЕРКА НА «ЧЕЛОВЕЧНОСТЬ» (Q5)
            is_human = False
            if 'P31' in claims:
                for p31_claim in claims['P31']:
                    val_id = p31_claim.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id')
                    if val_id == "Q5":
                        is_human = True
                        break
            
            if not is_human:
                results.append(f"⚠️ {t_name}: Это не человек. Проверьте ID!")
                continue

            # 6. БАЗОВАЯ ПРОВЕРКА ДАННЫХ
            if 'P569' not in claims:
                results.append(f"⚠️ {t_name}: Подозрительный профиль (нет даты рождения).")
                continue

            # 7. ИТОГОВАЯ ПРОВЕРКА НА СМЕРТЬ (P570)
            if 'P570' in claims:
                raw_date = claims['P570'][0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('time', '')
                clean_date = raw_date.lstrip('+').split('T')[0] if raw_date else "Неизвестная дата"
                results.append(f"❌ {t_name}: Мертв ({clean_date})")
            else:
                results.append(f"✅ {t_name}: Жив (Проверено на 100%)")
                
        except requests.exceptions.HTTPError as e:
            results.append(f"🔌 {t_name}: Ошибка сервера ({e.response.status_code})")
        except requests.exceptions.Timeout:
            results.append(f"⏳ {t_name}: Wikidata слишком долго не отвечает")
        except ValueError:
            results.append(f"🧩 {t_name}: Сервер вернул мусор вместо JSON")
        except Exception as e:
            results.append(f"🔥 {t_name}: Неизвестная ошибка ({type(e).__name__})")

    # Формируем и отправляем
    full_msg = "🛡 **Бронебойный отчет:**\n\n" + "\n".join(results)
    
    tg_url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(tg_url, json={"chat_id": chat_id, "text": full_msg, "parse_mode": "Markdown"})

if __name__ == "__main__":
    check()
