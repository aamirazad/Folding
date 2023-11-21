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
    q = request.args.get("q")
    if not q:
        return render_template("user.html")
    database_dict = lookup_user(q)
    if database_dict is None:
        return render_template("error.html")
    logging.debug(database_dict)
    return render_template("user.html", database=database_dict, arg=q)
