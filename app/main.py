# app/main.py
from flask import Flask, render_template, jsonify, session, g, request
from Scrappers.ScrapperDoggyMarket import scrape_doggy_data
from flask_bootstrap import Bootstrap  # Importuj Flask-Bootstrap
import sqlite3
import random

app = Flask(__name__)
Bootstrap(app)  # Inicjalizacja Flask-Bootstrap
app.secret_key = "321"
app.config["SESSION_COKIE_NAME"] = "123"

# Strona główna z różnymi ramkami
@app.route('/', methods=["POST", "GET"])
def index():
    session["all_items"], session["shopping_items"] = get_db()
    return render_template("indexx.html", all_items=session["all_items"],
                           shopping_items=session["shopping_items"])

@app.route('/add_items', methods=["post"])
def add_items():
    selected_item = request.form["select_items"]

    if selected_item not in session["shopping_items"]:
        session["shopping_items"].append(selected_item)
        session.modified = True
    return render_template("indexx.html", all_items=session["all_items"],
                           shopping_items=session["shopping_items"])

@app.route('/remove_items', methods=["post"])
def remove_items():
    checked_boxes = request.form.getlist("check")

    for item in checked_boxes:
        if item in session["shopping_items"]:
            idx = session["shopping_items"].index(item)
            session["shopping_items"].pop(idx)
            session.modified = True

    return render_template("indexx.html", all_items=session["all_items"],
                           shopping_items=session["shopping_items"])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('resources/Doggymarket_nft_database.db')
        cursor = db.cursor()
        cursor.execute("SELECT Collection_Name from NFTs")
        all_data = cursor.fetchall()
        all_data = [str(val[0]) for val in all_data]
        shopping_list = all_data.copy()
        shopping_list.clear()

    return all_data, shopping_list



@app.route('/t')
def table_page():
    # Connect to SQLite database
    conn = sqlite3.connect(r'C:\Users\kryst\OneDrive\Pulpit\2024\app\resources\Doggymarket_nft_database.db')
    cursor = conn.cursor()

    # Execute a query to fetch data (assuming you have a table named 'your_table')
    cursor.execute('SELECT * FROM NFTs')
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Render the HTML page with data
    return render_template('table_page.html', data=data)

# Nowa trasa i funkcja dla guzika 1


if __name__ == '__main__':
    app.run(debug=True)