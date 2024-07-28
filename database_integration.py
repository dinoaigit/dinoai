import sqlite3
from datetime import datetime
from trefle_api import fetch_species_taxonomy

def connect_db():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    return conn, c

def insert_if_not_exists(c, table, id_field, id_value, extra_fields=None, extra_values=None):
    c.execute(f'SELECT 1 FROM {table} WHERE {id_field} = ?', (id_value,))
    if c.fetchone():
        print(f"{table} tablosunda zaten mevcut: {id_value}")
        c.execute('''INSERT INTO log (plant_id, table_name, reason, timestamp)
                     VALUES (?, ?, ?, ?)''', (id_value, table, "Zaten mevcut", datetime.now()))
        return False
    else:
        if extra_fields and extra_values:
            fields = f'{id_field}, ' + ', '.join(extra_fields)
            placeholders = ', '.join(['?'] * (1 + len(extra_fields)))
            values = (id_value,) + tuple(extra_values)
            c.execute(f'INSERT INTO {table} ({fields}) VALUES ({placeholders})', values)
        else:
            c.execute(f'INSERT INTO {table} ({id_field}) VALUES (?)', (id_value,))
        return True

def save_to_db(c, plant_id):
    species_taxonomy = fetch_species_taxonomy(plant_id)
    if not species_taxonomy:
        print(f"Veri çekme başarısız oldu: {plant_id}")
        c.execute('''INSERT INTO log (plant_id, table_name, reason, timestamp)
                     VALUES (?, ?, ?, ?)''', (plant_id, "N/A", "Veri çekme başarısız", datetime.now()))
        return False

    # Tablolara veri eklemeden önce kontrol et
    if not insert_if_not_exists(
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
    ):
        return False

    if not insert_if_not_exists(
        c, "species", "id",
        species_taxonomy.get("species_id"),
        extra_fields=["name", "origin", "image_url"],
        extra_values=[species_taxonomy.get("species"), species_taxonomy.get("observations"), species_taxonomy.get("image_url")]
    ):
        return False

    if not insert_if_not_exists(c, "genus", "id", species_taxonomy.get("genus_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("genus")]):
        return False

    if not insert_if_not_exists(c, "family", "id", species_taxonomy.get("family_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("family")]):
        return False

    if not insert_if_not_exists(c, "division_order", "id", species_taxonomy.get("division_order_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("division_order")]):
        return False

    if not insert_if_not_exists(c, "division_class", "id", species_taxonomy.get("division_class_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("division_class")]):
        return False

    if not insert_if_not_exists(c, "division", "id", species_taxonomy.get("division_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("division")]):
        return False

    if not insert_if_not_exists(c, "subkingdom", "id", species_taxonomy.get("subkingdom_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("subkingdom")]):
        return False

    if not insert_if_not_exists(c, "kingdom", "id", species_taxonomy.get("kingdom_id"), extra_fields=["name"], extra_values=[species_taxonomy.get("kingdom")]):
        return False

    print(f"Veri başarıyla eklendi: {plant_id}")
    return True

def process_plant_id(c, plant_id):
    return save_to_db(c, plant_id)
