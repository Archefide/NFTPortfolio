# app/main.py
from flask import Flask, render_template
from Scrappers.ScrapperDoggyMarket import scrape_doggy_data
from flask_bootstrap import Bootstrap  # Importuj Flask-Bootstrap


app = Flask(__name__)
Bootstrap(app)  # Inicjalizacja Flask-Bootstrap

# Strona główna z różnymi ramkami
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint do renderowania button1.html
@app.route('/DoggyMarketCeny', methods=['GET'])
def render_button1():
    # Wywołaj funkcję scrape_doggy_data przy kliknięciu guzika 1
    doggy_data = scrape_doggy_data()

    # Debugowanie - wydrukuj dane o psach
    print("Dane o psach:", doggy_data)

    return render_template('button1.html', data=doggy_data)

# Nowa trasa i funkcja dla guzika 1


if __name__ == '__main__':
    app.run(debug=True)