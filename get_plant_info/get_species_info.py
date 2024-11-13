# get_species_info.py
import sys
import os
# 'C:\Users\fatih\Source\Repos\dinoai' path'ini eklemek i�in:
sys.path.append('C:\\Users\\fatih\\Source\\Repos\\dinoai')
from db_connection import connect_to_db

def get_species_info(species_id=None):
    conn = connect_to_db()
    if conn is None:
        return []
    
    cursor = conn.cursor()

    if species_id is not None:
        # Belirli bir species_id'ye sahip t�r� almak i�in sorgu
        cursor.execute("SELECT id, name FROM species WHERE id = ?", (species_id,))
        species = cursor.fetchone()
        conn.close()
        return [species] if species else []
    else:
        # T�m listeyi almak i�in sorgu
        cursor.execute("SELECT id, name FROM species")
        species_list = cursor.fetchall()
        conn.close()
        return species_list

if __name__ == "__main__":
    species_id = None  # Buray� ID ile de�i�tirin, None t�m listeyi d�nd�r�r
    species_info = get_species_info(species_id)
    for species in species_info:
        print(f"Species ID: {species[0]}, Species Name: {species[1]}")
