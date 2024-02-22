import os
import sqlite3
from selenium import webdriver
from bs4 import BeautifulSoup, Comment
from selenium.webdriver.chrome.options import Options
import time

def utworz_baze_danych():
    db_path = os.path.join(r'C:\Users\kryst\OneDrive\Pulpit\2024\app\resources\Doggymarket_nft_database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Utwórz tabelę NFTs, jeśli nie istnieje
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
            source TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            waluta TEXT,
            status INTEGER DEFAULT 0  -- Zmieniono domyślną wartość statusu
        )
    ''')

    # Zapisz zmiany i zamknij połączenie
    conn.commit()
    conn.close()

def zapisz_do_bazy_danych(dog_data):
    db_path = os.path.join(r'C:\Users\kryst\OneDrive\Pulpit\2024\app\resources\Doggymarket_nft_database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for dog in dog_data:
        # Sprawdź, czy istnieje rekord o takim samym collection_name
        cursor.execute('''
            SELECT id FROM NFTs WHERE collection_name = ? AND status = 1 ORDER BY timestamp DESC LIMIT 1
        ''', (dog['Collection_Name'],))
        existing_record = cursor.fetchone()

        if existing_record:
            # Jeśli istnieje, ustaw status ostatniego rekordu na 0
            cursor.execute('''
                UPDATE NFTs SET status = 0 WHERE id = ?
            ''', (existing_record[0],))

        # Wstaw dane do tabeli NFTs
        cursor.execute('''
            INSERT INTO NFTs (rank, collection_name, price, volume, trades, supply, owners, source, timestamp, waluta, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
        dog['Rank'], dog['Collection_Name'], dog['Price'], dog['Volume'], dog['Trades'], dog['Supply'], dog['Owners'],
        dog['Source'], dog['Timestamp'], 'DOGE'))

    # Zapisz zmiany i zamknij połączenie
    conn.commit()
    conn.close()

def scrape_doggy_data():
    url = 'https://doggy.market/nfts'

    options = Options()
    options.add_argument('--disable-gpu')
    # options.add_argument('--headless')  # Dodaj headless mode
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Poczekaj na załadowanie strony (możesz dostosować ten czas w zależności od potrzeb)
    time.sleep(1)

    # Pobranie źródła strony po załadowaniu JavaScript
    page_source = driver.page_source

    # Zamknięcie przeglądarki
    driver.quit()

    # Parsowanie strony za pomocą BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    dog_data = []
    blocks = soup.find_all('tr', class_='table-row clickable')

    for block in blocks:
        # Ignorowanie komentarzy wewnątrz bloków
        for element in block.find_all(string=lambda text: isinstance(text, Comment)):
            element.extract()

        # Wydobycie informacji z bloku
        rank = block.find('td', class_='rank').text.strip()
        collection_name = block.find('td', class_='name').text.strip()
        price_elem = block.find('td', class_='price').find('div')
        price = price_elem.text.strip() if price_elem else 'N/A'
        volume_elem = block.find('td', class_='volume').find('div')
        volume = volume_elem.text.strip() if volume_elem else 'N/A'
        trades = block.find('td', class_='trades').text.strip()
        supply = block.find('td', class_='supply').text.strip()
        owners = block.find('td', class_='owners').text.strip()

        # Sprawdź, czy istnieje element 'source'
        source_elem = block.find('td', class_='source')
        source = source_elem.text.strip() if source_elem else 'N/A'

        # Dodaj timestamp do słownika dog_data
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        dog_data.append({
            "Rank": rank,
            "Collection_Name": collection_name,
            "Price": price,
            "Volume": volume,
            "Trades": trades,
            "Supply": supply,
            "Owners": owners,
            "Source": "DoggyMarket (drc20).",
            "Timestamp": timestamp
        })

    return dog_data

# Wywołanie testowe
if __name__ == '__main__':
    utworz_baze_danych()
    dog_data = scrape_doggy_data()
    zapisz_do_bazy_danych(dog_data)

    print("Dane zostały zapisane do bazy danych.")
