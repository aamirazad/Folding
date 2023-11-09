from flask import Flask, render_template, request
from helpers import lookup

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == 'POST':
        return TODO
    else:
        return render_template("user.html")