from flask import Flask, render_template, request
from helpers import lookup_user
import logging

logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == 'POST':
        user = request.form.get("user")
        user_data = lookup_user(user)
        return render_template("/stats/user.html", user_data=user_data)
    else:
        return render_template("user.html")


@app.route("/back/user", methods=["POST"])
def back_user():
    return 