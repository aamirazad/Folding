from helpers import auto_save, daily_save
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
scheduler.add_job(auto_save, 'cron', minute='1')
scheduler.add_job(daily_save, 'cron', hour='11', minute='59') 
scheduler.print_jobs()
scheduler.start()