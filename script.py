import requests
import os

def check():
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    
    targets = {
        "Q512": "Владимир Высоцкий",
        "Q9682": "Елизавета II",
        "Q12044733": "Петер Ярош"
    }

    results = []

    for target_id, t_name in targets.items():
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{target_id}.json"
        headers = {'User-Agent': 'StatusCheckerBot/5.0_ParanoiaEdition'}

        try:
            # 1. ПРОВЕРКА СЕТИ (Ждем максимум 10 секунд, проверяем HTTP статус)
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status() # Бросит исключение, если статус не 200 OK
            
            # 2. ПРОВЕРКА ФОРМАТА (Точно ли это JSON?)
            data = response.json()
            
            # 3. ПРОВЕРКА СТРУКТУРЫ АПИ
            if 'entities' not in data:
                results.append(f"⚠️ {t_name}: Аномалия API (нет ключа 'entities').")
                continue
                
            # 4. ОБРАБОТКА РЕДИРЕКТОВ (Если ID изменился)
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

            # 5. ПРОВЕРКА НА «ЧЕЛОВЕЧНОСТЬ» (P31 должно содержать Q5)
            is_human = False
            if 'P31' in claims:
                for p31_claim in claims['P31']:
                    val_id = p31_claim.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id')
                    if val_id == "Q5":
                        is_human = True
                        break
            
            if not is_human:
                results.append(f"⚠️ {t_name}: Это не человек (ID объекта не Q5).")
                continue

            # 6. БАЗОВАЯ ПРОВЕРКА ДАННЫХ (Есть ли дата рождения)
            if 'P569' not in claims:
                results.append(f"⚠️ {t_name}: Подозрительный профиль (нет даты рождения).")
                continue

            # 7. ИТОГОВАЯ ПРОВЕРКА НА СМЕРТЬ
            if 'P570' in claims:
                raw_date = claims['P570'][0].get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('time', '')
                clean_date = raw_date.lstrip('+').split('T')[0] if raw_date else "Неизвестная дата"
                results.append(f"❌ {t_name}: Мертв ({clean_date})")
            else:
                results.append(f"✅ {t_name}: Жив (Проверено на 100%)")
                
        # ОТЛОВ СПЕЦИФИЧНЫХ ОШИБОК
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
