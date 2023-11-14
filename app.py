from flask import Flask, render_template, request
from helpers import lookup_user
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

@app.route("/")
def index():
    logging.info("enter getJSONReuslt")
    user_data = lookup_user("AamirA")
    logging.info(user_data)
    return render_template("index.html", user_data=user_data)

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == 'POST':
        return TODO
    else:
        return render_template("user.html")