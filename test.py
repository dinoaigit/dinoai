import subprocess
import time


def run_test():
    print("Test başlatılıyor...")
    # main.py dosyasını çalıştır
    process = subprocess.Popen(['python', 'main.py'])

    # Testin çalışmasına izin vermek için bir süre bekleyin
    time.sleep(5)

    # Testi durdur
    process.terminate()
    process.wait()
    print("Test tamamlandı.")


if __name__ == "__main__":
    run_test()
