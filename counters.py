
import json
from datetime import datetime

DATA_FILE = "daily_counts.json"

def load_counts():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_counts(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def increment_counter(dhikr):
    data = load_counts()
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in data:
        data[today] = {}
    if dhikr not in data[today]:
        data[today][dhikr] = 0
    data[today][dhikr] += 1
    save_counts(data)

def get_all_counts():
    data = load_counts()
    today = datetime.now().strftime("%Y-%m-%d")
    return data.get(today, {})
