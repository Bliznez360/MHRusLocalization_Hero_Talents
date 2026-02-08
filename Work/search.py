import json
import re

INPUT_FILE = "eng.rus.json"
OUTPUT_FILE = "found.json"

ENG_REGEX = re.compile(r"Agent\w*" )
RUS_REGEX = re.compile(r"Агент\w*")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

found = {}

for key, obj in data.items():
    eng = obj.get("eng", "")
    rus = obj.get("rus", "")

    eng_matches = len(ENG_REGEX.findall(eng))
    rus_matches = len(RUS_REGEX.findall(rus))

    # есть Danger Room в eng
    if eng_matches > 0:
        # нет совпадений вообще ИЛИ количество не совпадает
        if rus_matches == 0 or eng_matches > rus_matches:
            found[key] = {
                **obj,
                "_debug": {
                    "eng_matches": eng_matches,
                    "rus_matches": rus_matches
                }
            }

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(found, f, ensure_ascii=False, indent=2)

print(f"Найдено записей: {len(found)}")
print(f"Результат сохранён в {OUTPUT_FILE}")
