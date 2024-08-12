
import sys
import os
import datetime
# 'C:\Users\fatih\Source\Repos\dinoai' path'ini eklemek için:
sys.path.append('C:\\Users\\fatih\\Source\\Repos\\dinoai')
from db_connection import connect_to_db
from trefle_api import fetch_species_taxonomy

def update_or_insert(c, table, id_field, id_value, extra_fields=None, extra_values=None):
    # Güncelleme alanlarına 'update_date' ekle
    if extra_fields is not None:
        extra_fields.append('update_date')
        extra_values.append(datetime.datetime.now())
    
    c.execute(f'SELECT 1 FROM {table} WHERE {id_field} = ?', (id_value,))
    if c.fetchone():
        # Kayıt zaten varsa güncelleme yapma
        print(f"{table} tablosunda {id_field} = {id_value} zaten mevcut. Güncelleme yapılmadı.")
    else:
        # Yeni kayıt ekle
        if extra_fields and extra_values:
            fields = f'{id_field}, ' + ', '.join(extra_fields)
            placeholders = ', '.join(['?'] * (1 + len(extra_fields)))
            values = (id_value,) + tuple(extra_values)
            c.execute(f'INSERT INTO {table} ({fields}) VALUES ({placeholders})', values)
            print(f"{table} tablosuna yeni kayıt eklendi: {id_value}")
        else:
            c.execute(f'INSERT INTO {table} ({id_field}) VALUES (?)', (id_value,))
            print(f"{table} tablosuna yeni kayıt eklendi: {id_value}")

def save_to_db(c, plant_id, conn):
    print(f"Fetching species taxonomy for plant_id: {plant_id}")
    species_taxonomy = fetch_species_taxonomy(plant_id)
    
    if not species_taxonomy:
        print(f"Failed to fetch data for plant_id: {plant_id}")
        c.execute('''INSERT INTO log (plant_id, table_name, reason, timestamp)
                     VALUES (?, ?, ?, ?)''', (plant_id, "N/A", "Failed to fetch data", datetime.datetime.now()))
        conn.commit()
        return False

    # Always update plant_taxonomy table
    update_or_insert(
        c, "plant_taxonomy", "species_id",
        species_taxonomy.get("species_id"),
        extra_fields=["genus_id", "family_id", "division_order_id", "division_class_id", "division_id", "subkingdom_id", "kingdom_id"],
        extra_values=[
            species_taxonomy.get("genus_id"),
            species_taxonomy.get("family_id"),
            species_taxonomy.get("division_order_id"),
            species_taxonomy.get("division_class_id"),
            species_taxonomy.get("division_id"),
            species_taxonomy.get("subkingdom_id"),
            species_taxonomy.get("kingdom_id")
        ]
    )

    # Ensure species, genus, and family tables are populated
    if species_taxonomy.get("species"):
        update_or_insert(
            c, "species", "id",
            species_taxonomy.get("species_id"),
            extra_fields=["name", "origin", "image_url"],
            extra_values=[species_taxonomy.get("species"), species_taxonomy.get("observations"), species_taxonomy.get("image_url")]
        )

    if species_taxonomy.get("genus_id") and species_taxonomy.get("genus"):
        update_or_insert(c, "genus", "id", species_taxonomy.get("genus_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("genus")])

    if species_taxonomy.get("family_id") and species_taxonomy.get("family"):
        update_or_insert(c, "family", "id", species_taxonomy.get("family_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("family")])

    # Conditionally populate division_order and later tables only if they are not None
    if species_taxonomy.get("division_order_id") and species_taxonomy.get("division_order"):
        update_or_insert(c, "division_order", "id", species_taxonomy.get("division_order_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("division_order")])

    if species_taxonomy.get("division_class_id") and species_taxonomy.get("division_class"):
        update_or_insert(c, "division_class", "id", species_taxonomy.get("division_class_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("division_class")])

    if species_taxonomy.get("division_id") and species_taxonomy.get("division"):
        update_or_insert(c, "division", "id", species_taxonomy.get("division_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("division")])

    if species_taxonomy.get("subkingdom_id") and species_taxonomy.get("subkingdom"):
        update_or_insert(c, "subkingdom", "id", species_taxonomy.get("subkingdom_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("subkingdom")])

    if species_taxonomy.get("kingdom_id") and species_taxonomy.get("kingdom"):
        update_or_insert(c, "kingdom", "id", species_taxonomy.get("kingdom_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("kingdom")])

    print(f"Data successfully processed: {plant_id} (Stored species_id: {species_taxonomy.get('species_id')})")
    conn.commit()  # Commit the changes


def process_plant_id(plant_id):
    conn = connect_to_db()
    if conn:
        c = conn.cursor()
        try:
            save_to_db(c, plant_id, conn)
        finally:
            c.close()
            conn.close()
