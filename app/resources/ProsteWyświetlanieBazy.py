import sqlite3

def wyswietl_baze_danych():
    db_path = 'nft_database.db'

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Wykonaj zapytanie SQL, aby pobrać wszystkie dane z tabeli NFTs
        cursor.execute('SELECT * FROM NFTs')
        rows = cursor.fetchall()

        # Wyświetl dane
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Rank: {row[1]}")
            print(f"Collection Name: {row[2]}")
            print(f"Price: {row[3]}")
            print(f"Volume: {row[4]}")
            print(f"Trades: {row[5]}")
            print(f"Supply: {row[6]}")
            print(f"Owners: {row[7]}")
            print(f"Source: {row[8]}")
            print("------------------------------")

    except sqlite3.Error as e:
        print(f"Błąd podczas łączenia z bazą danych: {e}")

    finally:
        # Zamknij połączenie
        if conn:
            conn.close()

# Wywołanie testowe
if __name__ == '__main__':
    wyswietl_baze_danych()
