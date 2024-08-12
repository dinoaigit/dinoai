# get_genus_info.py
import sys
import os
# 'C:\Users\fatih\Source\Repos\dinoai' path'ini eklemek i�in:
sys.path.append('C:\\Users\\fatih\\Source\\Repos\\dinoai')
from db_connection import connect_to_db

def get_genus_info(genus_id=None):
    conn = connect_to_db()
    if conn is None:
        return []
    
    cursor = conn.cursor()

    if genus_id is not None:
        # Belirli bir genus_id'ye sahip t�r� almak i�in sorgu
        cursor.execute("SELECT id, name FROM genus WHERE id = ?", (genus_id,))
        genus = cursor.fetchone()
        conn.close()
        return [genus] if genus else []
    else:
        # T�m listeyi almak i�in sorgu
        cursor.execute("SELECT id, name FROM genus")
        genus_list = cursor.fetchall()
        conn.close()
        return genus_list

if __name__ == "__main__":
    genus_id = None  # Buray� ID ile de�i�tirin, None t�m listeyi d�nd�r�r
    genus_info = get_genus_info(genus_id)
    for genus in genus_info:
        print(f"Genus ID: {genus[0]}, Genus Name: {genus[1]}")
