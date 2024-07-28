import sqlite3
from datetime import datetime
from trefle_api import fetch_species_taxonomy

def connect_db():
    conn = sqlite3.connect('plants.db')
    c = conn.cursor()
    return conn, c

def insert_if_not_exists(c, table, id_field, name_field, id_value, name_value, extra_fields=None, extra_values=None):
    c.execute(f'SELECT 1 FROM {table} WHERE {id_field} = ?', (id_value,))
    if c.fetchone():
        print(f"{table} tablosunda zaten mevcut: {id_value}")
        c.execute('''INSERT INTO log (plant_id, table_name, reason, timestamp)
                     VALUES (?, ?, ?, ?)''', (id_value, table, "Zaten mevcut", datetime.now()))
    else:
        if extra_fields and extra_values:
            fields = f'{id_field}, {name_field}, ' + ', '.join(extra_fields)
            placeholders = ', '.join(['?'] * (2 + len(extra_fields)))
            values = (id_value, name_value) + tuple(extra_values)
            c.execute(f'INSERT INTO {table} ({fields}) VALUES ({placeholders})', values)
        else:
            c.execute(f'INSERT INTO {table} ({id_field}, {name_field}) VALUES (?, ?)', (id_value, name_value))

def save_to_db(c, plant_id):
    species_taxonomy = fetch_species_taxonomy(plant_id)
    if not species_taxonomy:
        print(f"Veri çekme başarısız oldu: {plant_id}")
        c.execute('''INSERT INTO log (plant_id, table_name, reason, timestamp)
                     VALUES (?, ?, ?, ?)''', (plant_id, "N/A", "Veri çekme başarısız", datetime.now()))
        return False

    # plant_taxonomy tablosuna veri eklemeden önce kontrol et
    c.execute('SELECT 1 FROM plant_taxonomy WHERE species_id = ?', (species_taxonomy.get("species_id"),))
    if c.fetchone():
        print(f"plant_taxonomy tablosunda zaten mevcut: {plant_id}")
        c.execute('''INSERT INTO log (plant_id, table_name, reason, timestamp)
                     VALUES (?, ?, ?, ?)''', (plant_id, "plant_taxonomy", "Zaten mevcut", datetime.now()))
    else:
        c.execute('''INSERT INTO plant_taxonomy (species_id, genus_id, family_id, division_order_id, division_class_id, division_id, subkingdom_id, kingdom_id)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (
                         species_taxonomy.get("species_id"),
                         species_taxonomy.get("genus_id"),
                         species_taxonomy.get("family_id"),
                         species_taxonomy.get("division_order_id"),
                         species_taxonomy.get("division_class_id"),
                         species_taxonomy.get("division_id"),
                         species_taxonomy.get("subkingdom_id"),
                         species_taxonomy.get("kingdom_id")
                     ))

    # species tablosuna veri eklemeden önce kontrol et ve ek verilerle ekle
    insert_if_not_exists(
        c, "species", "id", "name",
        species_taxonomy.get("species_id"),
        species_taxonomy.get("species"),
        extra_fields=["origin", "image_url"],
        extra_values=[species_taxonomy.get("observations"), species_taxonomy.get("image_url")]
    )

    # genus tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "genus", "id", "name", species_taxonomy.get("genus_id"), species_taxonomy.get("genus"))

    # family tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "family", "id", "name", species_taxonomy.get("family_id"), species_taxonomy.get("family"))

    # division_order tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "division_order", "id", "name", species_taxonomy.get("division_order_id"), species_taxonomy.get("division_order"))

    # division_class tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "division_class", "id", "name", species_taxonomy.get("division_class_id"), species_taxonomy.get("division_class"))

    # division tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "division", "id", "name", species_taxonomy.get("division_id"), species_taxonomy.get("division"))

    # subkingdom tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "subkingdom", "id", "name", species_taxonomy.get("subkingdom_id"), species_taxonomy.get("subkingdom"))

    # kingdom tablosuna veri eklemeden önce kontrol et
    insert_if_not_exists(c, "kingdom", "id", "name", species_taxonomy.get("kingdom_id"), species_taxonomy.get("kingdom"))

    print(f"Veri başarıyla eklendi: {plant_id}")
    return True

def process_plant_id(c, plant_id):
    return save_to_db(c, plant_id)
