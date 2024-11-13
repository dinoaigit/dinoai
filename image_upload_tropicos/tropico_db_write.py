# -*- coding: utf-8 -*-

import sys
from datetime import datetime
sys.path.append('C:\\Users\\fatih\\source\\repos\\dinoai')
from db_connection import connect_to_db
from tropico_get_image import get_species_info, get_name_id, get_images_by_name_id

def save_image_to_db(species_id, image_id, detail_jpg_url):
    conn = connect_to_db()
    cursor = conn.cursor()

    update_date = datetime.now()

    cursor.execute("""
        INSERT INTO [Plants].[dbo].[images] 
        (species_id, image_url, source, sourcephotoid, update_date) 
        VALUES (?, ?, ?, ?, ?)
    """, (species_id, detail_jpg_url, 'tropicosapi', image_id, update_date))

    conn.commit()
    conn.close()

def log_error_to_db(species_id, error_message):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        log_date = datetime.now()
        log_source = 'tropicoapi'  # Log kaynaðý olarak 'tropicoapi' yazýlýyor

        cursor.execute("""
            INSERT INTO [Plants].[dbo].[imagelogs] 
            (species_id, error_message, log_date, logsource) 
            VALUES (?, ?, ?, ?)
        """, (species_id, error_message, log_date, log_source))

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging to imagelogs for species_id {species_id}: {e}")

def process_and_save_images(species_id):
    try:
        species_info = get_species_info(species_id)

        if species_info:
            scientific_name = species_info[0][1]
            name_id = get_name_id(scientific_name)
            if name_id:
                images = get_images_by_name_id(name_id)
                if images:
                    for image in images:
                        image_id = image.get('ImageId')
                        detail_jpg_url = image.get('DetailJpgUrl')

                        if image_id and detail_jpg_url:
                            save_image_to_db(species_id, image_id, detail_jpg_url)
                            print(f"Image saved for species_id {species_id}: {detail_jpg_url}")
                        else:
                            log_error_to_db(species_id, 'Invalid image data')
                            print(f"Logged error for species_id {species_id}: Invalid image data")
                else:
                    log_error_to_db(species_id, 'No images found')
                    print(f"No images found for species_id {species_id}")
            else:
                log_error_to_db(species_id, 'NameID not found')
                print(f"NameID not found for species_id {species_id}")
        else:
            log_error_to_db(species_id, 'Species info not found')
            print(f"Species info not found for species_id {species_id}")

    except Exception as e:
        log_error_to_db(species_id, str(e))  # Herhangi bir hata olduðunda log'a yaz
        print(f"Error processing species_id {species_id}: {e}")

if __name__ == "__main__":
    # Test için bir species_id verebilirsin.
    process_and_save_images(1)
