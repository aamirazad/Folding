import logging
from flask import Flask, render_template, request, redirect, jsonify
from helpers import lookup_user, auto_save, get_user, query_db
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.middleware.proxy_fix import ProxyFix
import json

scheduler = BackgroundScheduler(daemon=True)

app = Flask(__name__)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

# Start auto saver
with app.app_context():
    scheduler.add_job(auto_save, 'interval', minutes=30)
    scheduler.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        username = request.form.get("auto-save")
        data = get_user(username)
        user_id = data[0]['id']
        if user_id is None:
            return render_template("error.html")
        db = get_db().bind.raw_connection()
        cursor = db.cursor()
        cursor.execute('REPLACE INTO saves (user_id) VALUES (%s)', user_id)
        db.commit()
        cursor.close()
        db.close()
        return redirect(f"/user?q={username}")
    else:
        return render_template("user.html")

@app.route('/data/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    data = lookup_user(username)
    if data is None:
        return None

    # Format database for graphing
    dates = [date[1] for date in data]  # Extract the date
    scores = [date[2] for date in data]  # Extract the score
    send = json.dumps({"date": dates, "score": scores})
    return jsonify(send)
