import time
import sqlite3
from datetime import datetime, timedelta
from database_integration import connect_db, process_plant_id

STATE_FILE = 'state.txt'

def load_state():
    try:
        with open(STATE_FILE, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 1

def save_state(plant_id):
    with open(STATE_FILE, 'w') as file:
        file.write(str(plant_id))

def run_scheduler():
    conn, c = connect_db()
    plant_id = load_state()

    while plant_id <= 100000:
        c.execute('''SELECT timestamp FROM log WHERE plant_id = ? AND reason = ? ORDER BY timestamp DESC LIMIT 1''',
                  (plant_id, "Veri çekme başarısız"))
        result = c.fetchone()
        if result and datetime.now() - datetime.fromisoformat(result[0]) < timedelta(days=365):
            print(f"{plant_id} ID'si için veri çekme hatası alınmış ve 1 yıl dolmamış.")
            plant_id += 1
            save_state(plant_id)
            continue

        success = process_plant_id(c, plant_id)
        if not success:
            plant_id += 1
            save_state(plant_id)
        else:
            plant_id += 1
            save_state(plant_id)

        conn.commit()
        time.sleep(60)

    conn.close()

if __name__ == "__main__":
    run_scheduler()
