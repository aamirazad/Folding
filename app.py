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
        # Lookup username submitted though the form
        user = request.form.get("user")
        user_data = lookup_user(user)
        # Check to make sure that user exists
        if not user_data:
            return render_template("error.html")
        # Add the user's score to the database
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO user (score) VALUES (?)', (user_data["score"],))
            conn.commit()
            data = conn.execute('SELECT * FROM user').fetchall()
        finally:
            conn.close()
        return render_template("/stats/user.html", data=data)
    else:
        # Render the username input form
        return render_template("user.html")

