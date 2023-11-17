from flask import Flask, render_template, request
from helpers import lookup_user
import logging
import sqlite3


logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

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
        conn = get_db()
        # conn.execute('INSERT INTO user (score) VALUES (?)', (user_data["score"],))
        # conn.commit()
        database = conn.execute('SELECT * FROM user').fetchall()
        database_dict = [dict(row) for row in database]
        scores = [post['score'] for post in database_dict]
        conn.close()

        return render_template("/stats/user.html", database=database_dict, scores=scores)
    else:
        database = query_db('SELECT * FROM user')
        # Render the username input form
        return render_template("user.html", database=database)

@app.route("/graph_test")
def graph_test():
    database = query_db('SELECT * FROM user')
    database_dict = [dict(row) for row in database]
    logging.debug(database_dict)
    return render_template("graph_test.html", database=database_dict)
