from flask import Flask, render_template, request
from helpers import lookup_user
import logging
import sqlite3

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == 'POST':
        user = request.form.get("user")
        user_data = lookup_user(user)
        logging.info(user_data)
        conn = get_db_connection()
        conn.execute('INSERT INTO user (score) VALUES (?)', user_data[0]['score'])
        data = conn.execute('SELECT * FROM user').fetchall()
        conn.close()
        return render_template("/stats/user.html", data=data)
    else:
        return render_template("user.html")


@app.route("/back/user", methods=["POST"])
def back_user():
    return 