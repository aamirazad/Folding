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
    save = request.args.get("save")
    # Change save's value to make sure html can read it
    if save == "on":
        save = "checked"
    # If the form wasn't submitted, show the form
    if not q:
        return render_template("user.html")
    database_dict = lookup_user(q, save)
    if database_dict is None:
        return render_template("error.html")
    return render_template("user.html", database=database_dict, username=q, save=save)