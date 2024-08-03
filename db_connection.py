import pyodbc

def connect_to_db():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=dinoai.database.windows.net;'
            'DATABASE=Plants;'
            'UID=dinoaicode;'
            'PWD=FaSe_310794'
        )
        print("Baglanti basarili!")
        return conn
    except Exception as e:
        print(f"Baglanti hatasi: {e}")
        return None
