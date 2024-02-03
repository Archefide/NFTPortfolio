from selenium import webdriver
from bs4 import BeautifulSoup, Comment
import time

def scrape_doggy_data():
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

    dog_data = []
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

        dog_data.append({
            "Rank": rank,
            "Name": name,
            "Price": price,
            "Volume": volume,
            "Trades": trades,
            "Supply": supply,
            "Owners": owners
        })

    return dog_data

"""# Wywołanie testowe
if __name__ == '__main__':
    dog_data = scrape_doggy_data()

    for dog in dog_data:
        print(f"Rank: {dog['Rank']}")
        print(f"Name: {dog['Name']}")
        print(f"Price: {dog['Price']}")
        print(f"Volume: {dog['Volume']}")
        print(f"Trades: {dog['Trades']}")
        print(f"Supply: {dog['Supply']}")
        print(f"Owners: {dog['Owners']}")
        print("------------------------------")
"""