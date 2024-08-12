
# save_image_to_db.py

from db_connection import connect_to_db

def save_image_to_db(species_id, image_url):
    conn = connect_to_db()
    if conn is None:
        return
    
    cursor = conn.cursor()

    try:
        # species_images tablosuna kayýt ekle
        cursor.execute("INSERT INTO species_images (species_id, image_url) VALUES (?, ?)", (species_id, image_url))
        conn.commit()
        print(f"Species ID: {species_id} için görsel URL baþarýyla kaydedildi: {image_url}")
    except Exception as e:
        print(f"Veritabanýna kaydederken bir hata oluþtu: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Örnek kullaným
    species_id = 1  # Bu deðeri veritabanýndan aldýðýnýz ID ile deðiþtirin
    image_url = "https://example.com/image.jpg"  # Bu deðeri indirdiðiniz görsel URL'si ile deðiþtirin
    save_image_to_db(species_id, image_url)
