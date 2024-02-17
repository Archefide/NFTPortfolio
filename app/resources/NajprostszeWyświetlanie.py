import sqlite3

# Pełna ścieżka do pliku bazy danych
sciezka_bazy_danych = 'Doggymarket_nft_database.db'

# Utwórz połączenie z bazą danych
conn = sqlite3.connect(sciezka_bazy_danych)
cursor = conn.cursor()

try:
    # Proste zapytanie SQL do pobrania wszystkich rekordów
    cursor.execute('SELECT * FROM NFTs')

    # Pobierz wszystkie rekordy
    rekordy = cursor.fetchall()

    # Wyświetl dane
    for rekord in rekordy:
        print(rekord)

except Exception as e:
    print(f"Błąd: {e}")

finally:
    # Zamknij połączenie z bazą danych
    conn.close()
