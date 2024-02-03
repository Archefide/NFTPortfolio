from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import time

url = 'https://doggy.market/nfts'



# Inicjalizacja przeglądarki Selenium
driver = webdriver.Chrome()
driver.get(url)

# Poczekaj na załadowanie strony (możesz dostosować ten czas w zależności od potrzeb)
time.sleep(5)

# Pobranie źródła strony po załadowaniu JavaScript
page_source = driver.page_source

# Zamknięcie przeglądarki
driver.quit()

# Parsowanie strony za pomocą BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Wyodrębnienie bloków danych
blocks = soup.find_all('tr', class_='table-row clickable')

for block in blocks:
    # Ignorowanie komentarzy wewnątrz bloków
    for element in block.find_all(text=lambda text: isinstance(text, Comment)):
        element.extract()

    # Wydobycie informacji z bloku
    rank = block.find('td', class_='rank').text.strip()
    name = block.find('td', class_='name').text.strip()

    # Sprawdzenie, czy istnieje element 'price'
    price_elem = block.find('td', class_='price').find('div')
    price = price_elem.text.strip() if price_elem else 'N/A'

    # Sprawdzenie, czy istnieje element 'volume'
    volume_elem = block.find('td', class_='volume').find('div')
    volume = volume_elem.text.strip() if volume_elem else 'N/A'

    trades = block.find('td', class_='trades').text.strip()
    supply = block.find('td', class_='supply').text.strip()
    owners = block.find('td', class_='owners').text.strip()

    # Wyświetlenie informacji
    print(f"Rank: {rank}")
    print(f"Name: {name}")
    print(f"Price: {price}")
    print(f"Volume: {volume}")
    print(f"Trades: {trades}")
    print(f"Supply: {supply}")
    print(f"Owners: {owners}")
    print("------------------------------")