from flask import Flask, render_template, request, redirect
from helpers import lookup_user, get_db, query_db, auto_save, get_user
import logging
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.DEBUG)

scheduler = BackgroundScheduler(daemon=True)

app = Flask(__name__)

# Start auto saver
with app.app_context():
    scheduler.add_job(auto_save, 'interval', minutes=10)
    scheduler.start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "POST":
        username = request.form.get("auto-save")
        user_data,user_id = get_user(username)
        logging.debug(user_id)
        conn = get_db()
        conn.execute('REPLACE INTO saves (user_id) VALUES (?)', [str(user_id)])
        conn.commit()
        conn.close()
        return redirect(f"/user?q={username}")
    else:
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

