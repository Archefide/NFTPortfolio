import sqlite3

def utworz_baze_danych():
    conn = sqlite3.connect('nft_database.db')
    cursor = conn.cursor()

    # Utwórz tabelę NFTs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NFTs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            collection_name TEXT NOT NULL,
            price REAL,
            volume INTEGER,
            trades INTEGER,
            supply INTEGER,
            owners INTEGER,
            source TEXT
        )
    ''')

    # Zapisz zmiany i zamknij połączenie
    conn.commit()
    conn.close()

if __name__ == "__main__":
    utworz_baze_danych()
    print("Baza danych została utworzona.")
