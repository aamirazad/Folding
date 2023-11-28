from flask import Flask, render_template, request
from helpers import lookup_user, get_db, query_db, auto_save
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def user():
    today = datetime.utcnow()
    converted = today.strftime('%F %T')
    logging.info(converted)
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
    auto_save()
    return render_template("user.html", database=database_dict, username=q, save=save)
