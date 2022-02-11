import datetime
import schedule

def kuku():
    now = datetime.datetime.now()
    now_tuple = datetime.datetime.timetuple(now)
    hour = now_tuple[3]
    if hour > 12:
        hour = hour % 12
    print('Ку' * hour)


schedule.every().hour.at(':00').do(kuku)

while True:
    schedule.run_pending()