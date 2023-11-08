from flask import Flask, render_template
import urllib.request, json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/user")
def user():
    url = "https://api.foldingathome.org/user-count"

    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    return render_template('user.html', response='response')