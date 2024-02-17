from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Konfiguracja opcji przeglądarki
chrome_options = Options()
chrome_options.add_argument("--headless")  # Opcja do uruchamiania przeglądarki bez interfejsu graficznego

# Inicjalizacja przeglądarki
driver = webdriver.Chrome(options=chrome_options)

# Adres URL do scrapowania
url = "https://www.tradeport.xyz/?tab=trending"

# Otwórz stronę
driver.get(url)

# Pobierz i wyświetl źródło strony
print(driver.page_source)

# Zamknij przeglądarkę
driver.quit()
