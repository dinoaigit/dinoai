
# -*- coding: utf-8 -*-

import sys
from datetime import datetime
import requests
sys.path.append('C:\\Users\\fatih\\source\\repos\\dinoai')
from db_connection import connect_to_db
from get_species_info import get_species_info
from inaturalist_get_image import get_inaturalist_images

def save_image_to_db(species_id, image_url):
    conn = connect_to_db()
    cursor = conn.cursor()

    update_date = datetime.now()

    cursor.execute("""
        INSERT INTO [Plants].[dbo].[images] 
        (species_id, image_url, source, update_date) 
        VALUES (?, ?, ?, ?)
    """, (species_id, image_url, 'inaturalist', update_date))

    conn.commit()
    conn.close()

def log_error_to_db(species_id, error_message):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()

        log_date = datetime.now()
        log_source = 'inaturalist'  # Log kaynaðý olarak 'inaturalist' yazýlýyor

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
            scientific_name = species_info[0][1]  # Assuming scientific name is at index 1
            print(f"Fetching images for: {scientific_name}")

            # Use get_inaturalist_images to get image URLs
            image_urls = get_inaturalist_images(scientific_name, per_page=5)

            if image_urls:
                for image_url in image_urls:
                    save_image_to_db(species_id, image_url)
                    print(f"Image saved for species_id {species_id}: {image_url}")
            else:
                log_error_to_db(species_id, 'No images found on iNaturalist')
                print(f"No images found for species_id {species_id}")
        else:
            log_error_to_db(species_id, 'Species info not found')
            print(f"Species info not found for species_id {species_id}")

    except Exception as e:
        log_error_to_db(species_id, str(e))
        print(f"Error processing species_id {species_id}: {e}")

if __name__ == "__main__":
    # Test için bir species_id verebilirsin.
    process_and_save_images(1)
