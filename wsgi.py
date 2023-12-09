from app import app
from helpers import auto_save, daily_save
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(daemon=True)

if __name__ == "__main__":
    with app.app_context():
        scheduler.add_job(auto_save, 'cron', minute='1,15,30,45')
        scheduler.add_job(daily_save, 'cron', hour='11', minute='59') 
        scheduler.start()
        scheduler.print_jobs()
    app.run()
