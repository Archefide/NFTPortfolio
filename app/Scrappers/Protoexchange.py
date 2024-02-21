import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def stworz_polaczenie_bazy_danych(nazwa_bazy):
    connection = sqlite3.connect(nazwa_bazy)
    return connection

def stworz_tabele(connection):
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS NFTs (
            id INTEGER PRIMARY KEY,
            nazwa_produktu TEXT,
            cena_sei TEXT,
            cena_dolar TEXT,
            volume_sei TEXT,
            volume_dolar TEXT,
            volume24_sei TEXT,
            volume24_dolar TEXT,
            owners TEXT,
            supply TEXT,
            source TEXT,
            timestamp INTEGER
        )
    ''')
    connection.commit()

def wstaw_dane_do_bazy(connection, dane, source, timestamp):
    cursor = connection.cursor()

    for klucz, tekst_elementu in dane.items():
        # Rozdziel tekst na poszczególne elementy
        elementy = tekst_elementu.split(',')

        # Wstaw dane do odpowiednich kolumn
        cursor.execute('INSERT INTO NFTs (nazwa_produktu, cena_sei, cena_dolar, volume_sei, volume_dolar,volume24_sei,volume24_dolar ,owners, supply, source, timestamp) VALUES (?, ?, ?, ?,?,?, ?, ?, ?, ?, ?)',
                       (elementy[1], elementy[2], elementy[3], elementy[4], elementy[5],elementy[6], elementy[7], elementy[8], elementy[9], source, timestamp))

    connection.commit()

def znajdz_elementy_i_utworz_slownik(url, selektor_css):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(2)

        elementy = driver.find_elements(By.CSS_SELECTOR, selektor_css)

        slownik_danych = {}

        for index, element in enumerate(elementy, 1):
            tekst_elementu = element.text.replace(',','.').replace('\n', ',').replace('🔥,','')
            klucz = f'{index}'
            slownik_danych[klucz] = tekst_elementu

        return slownik_danych

    finally:
        driver.quit()

# Przykładowe użycie
url = 'https://pallet.exchange/collections'
selektor_css = 'body > div.css-1kh77jd > div:nth-child(2) > div > table > tbody > tr'
dane = znajdz_elementy_i_utworz_slownik(url, selektor_css)

# Stwórz połączenie z bazą danych
nazwa_bazy = r'C:\Users\kryst\OneDrive\Pulpit\2024\app\resources\test.db'
polaczenie = stworz_polaczenie_bazy_danych(nazwa_bazy)

# Stwórz tabelę, jeśli nie istnieje
stworz_tabele(polaczenie)

# Pobierz prawdziwy timestamp
timestamp = int(time.time())

# Wstaw dane na koniec tabeli wraz z źródłem i timestampem
wstaw_dane_do_bazy(polaczenie, dane, 'pallet.exchange', timestamp)

# Zamknij połączenie z bazą danych
polaczenie.close()

print("Dane zostały pomyślnie zapisane do bazy danych.")
