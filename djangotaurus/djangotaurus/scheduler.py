from datetime import datetime
from tzlocal import get_localzone
from apscheduler.schedulers.background import BackgroundScheduler
from djangotaurus.models import StockPriceCurrent


def start():
    sched = BackgroundScheduler()

    # Update stock prices every 20 mins from Mon - Fri, 9am - 5pm
    sched.add_job(StockPriceCurrent.objects.update_prices, 'cron', #next_run_time=datetime.now(),
                  day_of_week='mon-fri', hour='9-17', minute='*/20', timezone=get_localzone())

    sched.start()