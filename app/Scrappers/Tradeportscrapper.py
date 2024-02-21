from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # Dodaj nowy import
import time
# Konfiguracja opcji przeglądarki
chrome_options = Options()
chrome_options.add_argument("--headless")  # Opcja do uruchamiania przeglądarki bez interfejsu graficznego

# Inicjalizacja przeglądarki
driver = webdriver.Chrome(options=chrome_options)

# Adres URL do scrapowania
url = "https://www.tradeport.xyz/?tab=trending"

# Otwórz stronę
driver.get(url)
time.sleep(2)
# Znajdź element za pomocą selektora
selector = "#__next > main > div.Home_homeStyles__f3nyZ > div > div.TabbedContainer_tabbedContainerStyles__LkKT7 > div > div.tabbed-container--content > div.TrendingCollectionsTable_trendingCollectionsTableStyles__NU2SM > div > div > div.table--list"

# Dodaj argumenty by i value
element = driver.find_element(By.CSS_SELECTOR, selector)

# Wyświetl zawartość elementu
print(element.text)

# Zamknij przeglądarkę
driver.quit()
