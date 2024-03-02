# app/main.py
from flask import Flask, render_template, jsonify, session, g, request
from flask_bootstrap import Bootstrap  # Importuj Flask-Bootstrap
import sqlite3
import sys
import requests

# Dodaj ścieżkę do folderu z kluczami_api do sys.path
sys.path.append(r'C:\Users\kryst\OneDrive\Dokumenty\Projekty Pycharm\XYZ\XXX')

from binance_keys import API_KEY, SECRET_KEY

app = Flask(__name__)
Bootstrap(app)  # Inicjalizacja Flask-Bootstrap
app.secret_key = "321"
app.config["SESSION_COKIE_NAME"] = "123"


# Dodaj funkcję, która pobiera dane Dogecoin z Binance
def pobierz_dane_doge_binance():
    base_url = "https://api.binance.com/api/v3/ticker/price"
    symbol = "DOGEUSDT"  # Symbol pary handlowej Dogecoin do dolara amerykańskiego

    params = {"symbol": symbol}

    try:
        response = requests.get(base_url, params=params, headers={"X-MBX-APIKEY": API_KEY})
        response.raise_for_status()  # Sprawdź, czy wystąpił błąd w zapytaniu HTTP
        dane = response.json()
        cena_dogecoin = float(dane["price"])
        print(f'Aktualna cena Dogecoin na Binance: {cena_dogecoin} USD')
        return cena_dogecoin  # Dodaj return, aby funkcja zwracała cenę
    except requests.exceptions.RequestException as e:
        print(f'Błąd podczas pobierania danych: {e}')
        return None  # Zwróć None w przypadku błędu

if __name__ == "__main__":
    pobierz_dane_doge_binance()


# Strona główna z różnymi ramkami
@app.route('/')
def index():
    session["all_items"], session["shopping_items"] = get_db()
    cena_dogecoin = pobierz_dane_doge_binance()


    return render_template("indexx.html", all_items=session["all_items"],
                           shopping_items=session["shopping_items"],
                           cena_dogecoin=cena_dogecoin)

def is_nft_added(name):
    return any(item[0] == name for item in session["shopping_items"])


@app.route('/add_items', methods=["POST"])
def add_items():
    selected_item = request.form['selected_items']
    quantity = int(request.form['quantity'])
    item_name, item_price, waluta, price_doge = selected_item.split('|')

    # Usuń przecinki z wartości item_price
    item_price = item_price.replace(',', '')

    # Oblicz wartość dla nowego przedmiotu
    total_value = int(quantity) * float(item_price)
    total_value_portfolio = int(quantity) * float(item_price) * float(price_doge)

    print(total_value_portfolio)
    # Sprawdź, czy przedmiot już istnieje na liście przedmiotów
    if not is_nft_added(item_name):
        session["shopping_items"].append([item_name, float(item_price), waluta, float(price_doge), quantity, total_value, total_value_portfolio])
        session.modified = True

    cena_dogecoin = pobierz_dane_doge_binance()

    return render_template("indexx.html", all_items=session["all_items"], shopping_items=session["shopping_items"],
                           cena_dogecoin=cena_dogecoin)


def total_value_sum():
    return sum(item[4] * item[3] for item in session["shopping_items"])

# Użyj dekoratora @app.context_processor
@app.context_processor
def inject_functions():
    return dict(total_value_sum=total_value_sum)

def calculate_total_portfolio_value(shopping_items):
    total_portfolio_value = sum(item[6] for item in shopping_items)
    return total_portfolio_value
# Użyj dekoratora @app.context_processor
@app.context_processor
def inject_functions():

    return dict(
        total_value_sum=total_value_sum,
        total_portfolio_value=calculate_total_portfolio_value(session["shopping_items"])
    )

@app.route('/portfolio', methods=["POST"])
def portfolio():
    checked_boxes = request.form.getlist("check")
    print(f"Checked boxes: {checked_boxes}")

    # Utwórz nową listę zakupów, pomijając zaznaczone przedmioty
    session["shopping_items"] = [item for item in session["shopping_items"] if item[0] not in checked_boxes]
    session.modified = True
    print(f"Updated shopping items: {session['shopping_items']}")

    # Przekaz dodatkowe informacje do szablonu HTML
    total_value = total_value_sum()
    total_value_dolar = sum(item[4] * item[3] for item in session["shopping_items"])  # Suma wartości w dolarach
    total_value_doge = sum(item[4] for item in session["shopping_items"])  # Suma wartości w Dogecoin

    # Oblicz nową wartość całkowitą portfela
    total_portfolio_value = calculate_total_portfolio_value(session["shopping_items"])

    return render_template("indexx.html", all_items=session["all_items"], shopping_items=session["shopping_items"],
                           total_value=total_value, total_value_dolar=total_value_dolar, total_value_doge=total_value_doge,
                           total_portfolio_value=total_portfolio_value)



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('resources/Doggymarket_nft_database.db')
        cursor = db.cursor()
        cursor.execute("SELECT collection_name, price, waluta, price_doge from NFTs WHERE status = 1")
        all_data = cursor.fetchall()
        all_data = [(str(val[0]), val[1], str(val[2]), val[3]) for val in all_data]

        shopping_list = all_data.copy()
        shopping_list.clear()


    return all_data, shopping_list

if __name__ == '__main__':
    app.run(debug=True)