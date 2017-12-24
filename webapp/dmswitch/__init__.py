import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit

app = Flask(__name__)
app.config.from_object('dmswitch.default_settings')
app.config.from_envvar('DMSWITCH_SETTINGS')
print(app.config['SERVER_NAME'])

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'dmswitch.log'), 'midnight')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

from . import dmswitch, views


@app.before_first_request
def init():
    apsched = BackgroundScheduler()
    apsched.start()
    now = datetime.now()
    # start at next round minute
    start = now.replace(minute=now.timetuple().tm_min + 1, second=0, microsecond=0)
    apsched.add_job(dmswitch.interval_check, trigger='interval',
                    start_date=start, minutes=1)  # hours=2)
    atexit.register(lambda: apsched.shutdown())
