from trefle_api import get_plant_data
from folder_structure import create_folders
from google_drive import upload_file_to_drive
import schedule
import time

def job():
    plants = get_plant_data()
    create_folders(plants)
    # Dosya yolunu ve folder_id'yi uygun şekilde güncelleyin
    upload_file_to_drive('path/to/your/file.txt', 'your_folder_id')

# Her 1 saatte bir `job` fonksiyonunu çalıştır
schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)