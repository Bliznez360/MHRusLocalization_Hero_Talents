import json

def merge_translations():
    # Пути к файлам
    map_file = 'AchievementStringMap.json'
    index_file = 'index_map.json'
    work_file = 'achievement_work.json'
    output_file = 'AchievementStringMap_updated.json'
    
    with open(map_file, 'r', encoding='utf-8') as f:
        string_map = json.load(f)
    with open(index_file, 'r', encoding='utf-8') as f:
        index_map = json.load(f)
    with open(work_file, 'r', encoding='utf-8') as f:
        work_data = json.load(f)

    count = 0
    errors = 0

    for work_id, content in work_data.items():
        english_work = content.get('en_us', '').strip()
        russian_text = content.get('ru_ru')
        
        if not russian_text:
            continue

        target_ids = index_map.get(work_id, [])

        for long_id in target_ids:
            if long_id in string_map:
                original_en = string_map[long_id].get('en_us', '').strip()

                # ПРОВЕРКА: Схож ли английский текст?
                if original_en != english_work:
                    print(f"⚠️  ВНИМАНИЕ (ID {long_id}):")
                    print(f"   В работе: '{english_work}'")
                    print(f"   В файле : '{original_en}'")
                    print("-" * 30)
                    errors += 1
                    # Если хочешь, чтобы скрипт СТОПАЛСЯ при ошибке, раскомментируй строку ниже:
                    # continue 
                
                # Добавляем перевод
                string_map[long_id]['ru_ru'] = russian_text
                count += 1
            else:
                print(f"❌ ОШИБКА: ID {long_id} не найден в {map_file}")

    # Сохраняем результат
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(string_map, f, ensure_ascii=False, indent=2)

    print(f"✅ Успешно влито строк: {count}")
    if errors > 0:
        print(f"⚠️  Найдено расхождений в английском тексте: {errors}")
        print("Совет: Проверь логи выше, возможно индексы сместились.")
    print(f"📁 Результат здесь: {output_file}")

if __name__ == "__main__":
    merge_translations()