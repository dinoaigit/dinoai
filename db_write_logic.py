from db_write import connect_to_db, process_plant_id
from datetime import datetime, timedelta

def get_max_species_id(c):
    try:
        c.execute("SELECT MAX(species_id) FROM plant_taxonomy")
        result = c.fetchone()
        return result[0] if result[0] is not None else 1
    except Exception as e:
        print(f"Error loading max species_id: {e}")
        return 1

def check_log_for_species_id(c, species_id):
    c.execute("SELECT COUNT(*) FROM log WHERE plant_id = ?", (species_id,))
    result = c.fetchone()
    return result[0] > 0

def find_next_available_species_id(c):
    species_id = get_max_species_id(c) + 1

    while check_log_for_species_id(c, species_id):
        species_id += 1

    return species_id

def save_error(c, plant_id):
    try:
        c.execute("INSERT INTO log (plant_id, table_name, reason, timestamp) VALUES (?, ?, ?, GETDATE())",
                  (plant_id, 'N/A', 'Data fetch failed'))
        c.commit()
    except Exception as e:
        print(f"Error saving error: {e}")

def remove_error(c, plant_id):
    try:
        c.execute("DELETE FROM log WHERE plant_id = ? AND reason = 'Data fetch failed'", (plant_id,))
        c.commit()
    except Exception as e:
        print(f"Error removing error: {e}")

def reprocess_log_errors(c):
    try:
        c.execute("SELECT plant_id FROM log WHERE reason = 'Data fetch failed'")
        error_ids = [row[0] for row in c.fetchall()]

        for plant_id in error_ids:
            try:
                process_plant_id(plant_id)
                remove_error(c, plant_id)
                print(f"Successfully reprocessed plant_id {plant_id}")
            except Exception as e:
                print(f"Error reprocessing plant_id {plant_id}: {e}")

    except Exception as e:
        print(f"Error fetching log errors: {e}")

def run_scheduler():
    conn = connect_to_db()
    if conn:
        c = conn.cursor()

        while True:
            species_id = find_next_available_species_id(c)

            if species_id > 450000:
                print("Reached plant_id 450000, switching to reprocess log errors.")
                reprocess_log_errors(c)
                break

            try:
                process_plant_id(species_id)
            except Exception as e:
                print(f"Error processing species_id {species_id}: {e}")
                save_error(c, species_id)

        c.close()
        conn.close()

if __name__ == "__main__":
    run_scheduler()
