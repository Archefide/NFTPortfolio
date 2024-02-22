# app/main.py
from flask import Flask, render_template, jsonify, session, g, request
from flask_bootstrap import Bootstrap  # Importuj Flask-Bootstrap
import sqlite3


app = Flask(__name__)
Bootstrap(app)  # Inicjalizacja Flask-Bootstrap
app.secret_key = "321"
app.config["SESSION_COKIE_NAME"] = "123"

# Strona główna z różnymi ramkami
@app.route('/', methods=["POST", "GET"])
def index():
    session["all_items"], session["shopping_items"] = get_db()
    print(session["all_items"])
    return render_template("indexx.html", all_items=session["all_items"],
                           shopping_items=session["shopping_items"])

def is_nft_added(name):
    return any(item[0] == name for item in session["shopping_items"])


@app.route('/add_items', methods=["POST"])
def add_items():
    selected_item = request.form['selected_items']
    quantity = int(request.form['quantity'])
    item_name, item_price, waluta = selected_item.split('|')

    # Usuń przecinki z wartości item_price
    item_price = item_price.replace(',', '')

    # Oblicz wartość dla nowego przedmiotu
    total_value = int(quantity) * float(item_price)

    # Sprawdź, czy przedmiot już istnieje na liście przedmiotów
    if not is_nft_added(item_name):
        session["shopping_items"].append([item_name, item_price, waluta, quantity, total_value])
        session.modified = True

    return render_template("indexx.html", all_items=session["all_items"], shopping_items=session["shopping_items"])


# Dodaj tę funkcję do pliku main.py
def total_value_sum():
    return sum(item[4] for item in session["shopping_items"])

# Użyj dekoratora @app.context_processor
@app.context_processor
def inject_functions():
    return dict(total_value_sum=total_value_sum)

# Aktualizacja metody portfolio
@app.route('/portfolio', methods=["POST"])
def portfolio():
    checked_boxes = request.form.getlist("check")
    print(f"Checked boxes: {checked_boxes}")

    # Utwórz nową listę zakupów, pomijając zaznaczone przedmioty
    session["shopping_items"] = [item for item in session["shopping_items"] if item[0] not in checked_boxes]
    session.modified = True
    print(f"Updated shopping items: {session['shopping_items']}")

    return render_template("indexx.html", all_items=session["all_items"], shopping_items=session["shopping_items"])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('resources/Doggymarket_nft_database.db')
        cursor = db.cursor()
        cursor.execute("SELECT Collection_Name, Price, waluta from NFTs WHERE status = 1")
        all_data = cursor.fetchall()
        all_data = [(str(val[0]), val[1], str(val[2])) for val in all_data]
        shopping_list = all_data.copy()
        shopping_list.clear()


    return all_data, shopping_list

if __name__ == '__main__':
    app.run(debug=True)