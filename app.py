import logging
from flask import Flask, render_template, request, redirect, jsonify
from helpers import lookup_user, auto_save, get_user, query_db, calculate_daily, daily_save
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

scheduler.add_job(auto_save, 'cron', minute='1,15,30,45')
scheduler.add_job(daily_save, 'cron', hour='11', minute='59') 
scheduler.start()
scheduler.print_jobs()


@app.route("/")
def index():
    return redirect("/user")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        username = request.form.get("auto-save")
        data = get_user(username)
        user_id = data[0]['id']
        if user_id is None:
            return render_template("error.html")
        query_db('REPLACE INTO saves (user_id) VALUES (:user_id)', {'user_id': user_id}, one=True)
        return redirect(f"/user?q={username}")
    else:
        return render_template("user.html")

@app.route('/data/user', methods=['GET'])
def user_total_api():
    username = request.args.get('username')
    save = False
    if request.args.get('save') == 'on':
        save = True
    logging.debug(save)
    data = lookup_user(username, save)
    if data is None:
        return None

    # Format database for graphing
    dates = [date[1] for date in data]  # Extract the date
    scores = [date[2] for date in data]  # Extract the score
    send = json.dumps({"date": dates, "score": scores})
    return jsonify(send)

@app.route('/data/user_daily', methods=['GET'])
def get_user_daily():
    username = request.args.get('username')
    # Get two lists, one with the score differnence, and another with the days that represnt it
    day_score, day_days = calculate_daily(username)
    if day_score is None:
        return None
    # Send as json
    send = json.dumps({"date": day_days, "score": day_score})
    return jsonify(send)