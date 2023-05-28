import os

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def schedule_email():
    current_time = datetime.now().time()
    if current_time.hour == 22 and current_time.minute == 42:
        #Todo: add rapport
        print("this function runs every 10 seconds")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    scheduler.add_job(schedule_email, 'interval', days=1, start_date='2023-05-28 22:42:00')
    if os.environ.get('RUN_MAIN'):
        scheduler.start()

