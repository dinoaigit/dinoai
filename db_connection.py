import pyodbc

def connect_to_db():
    try:
        print("Attempting to connect to the database...")  # Ba�lant� giri�imini izlemek i�in
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'  # Yerel sunucu i�in
            'DATABASE=Plants;'  # Yerel veritaban�n�z�n ad�
            'Trusted_Connection=yes;'
        )
        print("Connection successful!")  # Ba�lant� ba�ar�l� oldu�unda
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

# Ba�lant� fonksiyonunu �a��r ve sonu�lar� kontrol et
connection = connect_to_db()
if connection:
    print("Connection object created successfully.")
else:
    print("Failed to create connection object.")
