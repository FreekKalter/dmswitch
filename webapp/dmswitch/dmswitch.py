from . import app
import random
import string
from .declarative import Base, User
from pushover import Client as pushoverClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import onetimepass as otp
import subprocess

pc = pushoverClient(app.config['PUSHOVER_USER_KEY'], api_token=app.config['PUSHOVER_API_TOKEN'])

engine = create_engine('sqlite:///' + app.config['DB_FILE'])
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)


def interval_check(debug=False):
    session = Session()
    users = session.query(User).all()
    for user in users:
        if debug or user.smallest_diff < 10:
            print(user.missed_alerts)
            if user.missed_alerts > user.threshold:
                print(user.action)
                try:
                    subprocess.check_call([user.action])
                except subprocess.CalledProcessError as e:
                    print(e)
                continue
            priority = user.missed_alerts if user.missed_alerts < 2 else 2
            app.logger.warning(f'send notification, with prio: {user.missed_alerts}')
            pc.send_message('Confirm please.', url=f'http://{app.config["SERVER_NAME"]}/{user.name}',
                            url_title='I\'m alive', title='Dead man\'s switch',
                            priority=priority, retry=60, expire=3600)
            user.missed_alerts += 1
    session.commit()
    session.close()


def validate(username, token):
    session = Session()
    user = session.query(User).filter(User.name == username).one()
    secret = user.otp_secret
    response = 'invalid'
    if otp.valid_totp(token=token, secret=secret):
        user.missed_alerts = 0
        response = 'valid'
    session.commit()
    session.close()
    return response


def random_otp_secret():
    return [random.choice(string.ascii_uppercase) for _ in range(16)]


def create_user(name, alert_type="pushover", alert_times="19:55 19:56 19:57 19:58", action="./action_test.sh",
                threshold=3, otp_secret=random_otp_secret()):
    u = User()
    u.name          = name
    u.alert_type    = alert_type
    u.action        = action
    u.missed_alerts = 0
    u.alert_times   = alert_times
    u.threshold     = threshold
    u.otp_secret    = otp_secret
    session = Session()
    session.add(u)
    session.commit()
    session.close()


def user_info(username):
    session = Session()
    user = session.query(User).filter(User.name == username).one()
    session.close()
    return str(user)
