from folder_structure import create_folder_structure
from google_drive import authenticate_google_drive, upload_folder_to_drive
import schedule
import time


def job():
    # Klasör yapısını oluştur
    create_folder_structure()

    # Google Drive'a bağlan
    service = authenticate_google_drive()

    # Yerel klasör yolunu belirtin
    local_folder_path = 'path/to/your/local/folder'

    # Google Drive'a yükle
    upload_folder_to_drive(service, local_folder_path)


# Her 5 dakikada bir `job` fonksiyonunu çalıştır
schedule.every(5).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
