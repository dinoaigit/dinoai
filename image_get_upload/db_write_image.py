
# save_image_to_db.py

from db_connection import connect_to_db

def save_image_to_db(species_id, image_url):
    conn = connect_to_db()
    if conn is None:
        return
    
    cursor = conn.cursor()

    try:
        # species_images tablosuna kay�t ekle
        cursor.execute("INSERT INTO species_images (species_id, image_url) VALUES (?, ?)", (species_id, image_url))
        conn.commit()
        print(f"Species ID: {species_id} i�in g�rsel URL ba�ar�yla kaydedildi: {image_url}")
    except Exception as e:
        print(f"Veritaban�na kaydederken bir hata olu�tu: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # �rnek kullan�m
    species_id = 1  # Bu de�eri veritaban�ndan ald���n�z ID ile de�i�tirin
    image_url = "https://example.com/image.jpg"  # Bu de�eri indirdi�iniz g�rsel URL'si ile de�i�tirin
    save_image_to_db(species_id, image_url)
