import os
import shutil
import schedule
import time
from dotenv import load_dotenv

def load_configuration():
    load_dotenv()
    backup_interval = int(os.getenv('BACKUP_TIME'))
    return backup_interval

def backup_database():
    source = 'database.db'
    destination = 'backup.db'
    shutil.copy2(source, destination)
    print(f"Backup created at {time.strftime('%Y-%m-%d %H:%M:%S')}")

def schedule_backup(interval):
    schedule.every(interval).hours.do(backup_database)

def start_backup():
    backup_interval = load_configuration()
    schedule_backup(backup_interval)
    while True:
        schedule.run_pending()
        time.sleep(1)
