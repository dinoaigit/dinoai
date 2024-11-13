from tropico_db_write import process_and_save_images
from db_connection import connect_to_db

def get_max_species_id_from_images(c):
    try:
        c.execute("SELECT MAX(species_id) FROM [Plants].[dbo].[images]")
        result = c.fetchone()
        return result[0] if result[0] is not None else 0
    except Exception as e:
        print(f"Error loading max species_id from images: {e}")
        return 0

def get_max_species_id_from_imagelogs(c):
    try:
        c.execute("SELECT MAX(species_id) FROM [Plants].[dbo].[imagelogs]")
        result = c.fetchone()
        return result[0] if result[0] is not None else 0
    except Exception as e:
        print(f"Error loading max species_id from imagelogs: {e}")
        return 0

def find_next_available_species_id(c):
    max_species_id_images = get_max_species_id_from_images(c)
    max_species_id_imagelogs = get_max_species_id_from_imagelogs(c)
    
    return max(max_species_id_images, max_species_id_imagelogs) + 1

def run_scheduler():
    conn = connect_to_db()
    if conn:
        c = conn.cursor()

        while True:
            # En yüksek species_id'yi bul
            species_id = find_next_available_species_id(c)

            if species_id > 450000:
                print("Reached species_id 450000, stopping process.")
                break

            try:
                print(f"Processing species_id: {species_id}")
                process_and_save_images(species_id)  # species_id'yi sýrayla iþliyoruz
            except Exception as e:
                print(f"Error processing species_id {species_id}: {e}")

        c.close()
        conn.close()

if __name__ == "__main__":
    run_scheduler()
