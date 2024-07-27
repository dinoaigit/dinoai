import json
from datetime import datetime, timedelta

TIMESTAMP_FILE = 'timestamps.json'
INTERVAL_DAYS = 90  # 3 months

def load_timestamps():
    try:
        with open(TIMESTAMP_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "kingdoms": "1970-01-01T00:00:00",
            "subkingdoms": {},
            "divisions": {},
            "classes": {},
            "orders": {},
            "families": {},
            "genuses": {},
            "species": {}
        }

def save_timestamps(timestamps):
    with open(TIMESTAMP_FILE, 'w') as f:
        json.dump(timestamps, f)

def should_update(timestamps, category, key=None):
    if key:
        last_update = datetime.fromisoformat(timestamps[category].get(key, "1970-01-01T00:00:00"))
    else:
        last_update = datetime.fromisoformat(timestamps[category])
    return datetime.now() - last_update > timedelta(days=INTERVAL_DAYS)

def update_timestamp(timestamps, category, key=None):
    if key:
        timestamps[category][key] = datetime.now().isoformat()
    else:
        timestamps[category] = datetime.now().isoformat()
    save_timestamps(timestamps)
