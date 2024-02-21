# app/main.py
from flask import Flask, render_template, jsonify, session, g, request
from Scrappers.ScrapperDoggyMarket import scrape_doggy_data
from flask_bootstrap import Bootstrap  # Importuj Flask-Bootstrap
import sqlite3
import random

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
    #print("debug:", doggy_data)

    return render_template('button1.html', data=doggy_data)

@app.route('/get_data')
def get_data():
    # Connect to SQLite database
    conn = sqlite3.connect(r'C:\Users\kryst\OneDrive\Pulpit\2024\app\resources\Doggymarket_nft_database.db')
    cursor = conn.cursor()

    # Execute a query to fetch data (assuming you have a table named 'your_table')
    cursor.execute('SELECT * FROM NFTs')
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert data to a list of dictionaries
    data_list = [{'Chain': row[0], 'name': row[1], 'email': row[2]} for row in data]

    # Return data as JSON
    return jsonify(data_list)

@app.route('/po')
def indexx():
    data = get_db()
    return render_template("indexx.html", all_data= data)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('resources/Doggymarket_nft_database.db')
        cursor = db.cursor()
        cursor.execute("SELECT Collection_Name from NFTs")
        all_data = cursor.fetchall()
        all_data = [str(val[0]) for val in all_data]
    return all_data

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