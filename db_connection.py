import pyodbc

def connect_to_db():
    try:
        print("Attempting to connect to the database...")  # Baðlantý giriþimini izlemek için
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'  # Yerel sunucu için
            'DATABASE=Plants;'  # Yerel veritabanýnýzýn adý
            'Trusted_Connection=yes;'
        )
        print("Connection successful!")  # Baðlantý baþarýlý olduðunda
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"SQL Error: {ex}")
        if sqlstate == '28000':
            print("Authentication failed.")
        elif sqlstate == '08001':
            print("Server connection failed.")
        else:
            print(f"Other error: {ex}")
        return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None

# Baðlantý fonksiyonunu çaðýr ve sonuçlarý kontrol et
connection = connect_to_db()
if connection:
    print("Connection object created successfully.")
else:
    print("Failed to create connection object.")
