import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def znajdz_elementy_i_utworz_liste(url, selektor_css):
    # Inicjalizuj przeglądarkę Chrome (możesz dostosować do innej przeglądarki)
    driver = webdriver.Chrome()

    try:
        # Otwórz stronę
        driver.get(url)

        time.sleep(2)

        # Znajdź elementy za pomocą selektora CSS
        elementy = driver.find_elements(By.CSS_SELECTOR, selektor_css)

        # Inicjalizuj listę na dane
        lista_danych = []

        # Iteruj po znalezionych elementach
        for element in elementy:
            # Pobierz tekst z elementu
            tekst_elementu = element.text

            # Dodaj tekst do listy
            lista_danych.append(tekst_elementu)

        return lista_danych

    finally:
        # Zamknij przeglądarkę
        driver.quit()

# Przykładowe użycie
url = 'https://pallet.exchange/collections'
selektor_css = 'body > div.css-1kh77jd > div:nth-child(2) > div > table > tbody > tr'
dane = znajdz_elementy_i_utworz_liste(url, selektor_css)

# Wyświetl dane
for indeks, element in enumerate(dane, start=1):
    print(f"{indeks}. {element}")
