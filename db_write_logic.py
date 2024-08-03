from db_write import connect_to_db, process_plant_id

STATE_FILE = 'state.txt'
ERROR_FILE = 'errors.txt'

def load_state():
    try:
        with open(STATE_FILE, 'r') as file:
            content = file.read().strip()
            return int(content) if content else 1
    except FileNotFoundError:
        return 1

def save_state(plant_id):
    with open(STATE_FILE, 'w') as file:
        file.write(str(plant_id))

def load_errors():
    try:
        with open(ERROR_FILE, 'r') as file:
            errors = [line.strip() for line in file.readlines() if line.strip()]
            return [int(line) for line in errors]
    except FileNotFoundError:
        return []

def save_error(plant_id):
    with open(ERROR_FILE, 'a') as file:
        file.write(f"{plant_id}\n")

def remove_error(plant_id):
    errors = load_errors()
    if plant_id in errors:
        errors.remove(plant_id)
        with open(ERROR_FILE, 'w') as file:
            for error in errors:
                file.write(f"{error}\n")

def run_scheduler():
    plant_id = load_state()

    try:
        process_plant_id(plant_id)
        remove_error(plant_id)
    except Exception as e:
        print(f"Error processing plant_id {plant_id}: {e}")
        save_error(plant_id)

    plant_id += 1
    if plant_id > 100000:
        plant_id = 1

    save_state(plant_id)

if __name__ == "__main__":
    run_scheduler()
