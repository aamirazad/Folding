from flask import Flask, render_template, request
from helpers import lookup_user, get_db, query_db
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def user():
    # if request.args.get("q") is None:
    #     return render_template("user.html")
    # user = request.args.get("q")
    # user_data = lookup_user(user)
    # # Check to make sure that user exists
    # if not user_data:
    #     return render_template("error.html")
    # # Add the user's score to the database
    # conn = get_db()
    # # conn.execute('INSERT INTO user (score, user_id) VALUES (?, ?)', (user_data["score"],user_data['id']),)
    # conn.commit()
    # conn.close()
    # database = query_db('SELECT * FROM user WHERE user_id = ?', [user_data["id"]])
    # database_dict = [dict(row) for row in database]
    # # Render the username input form
    # return render_template("user.html", database=database_dict)
    database_dict = lookup_user(request.args.get("q"))

    if database_dict is None:
        return render_template("error.html")
    return render_template("user.html", database=database_dict)
