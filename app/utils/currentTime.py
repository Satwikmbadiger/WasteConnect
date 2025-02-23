from datetime import datetime


def get_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")