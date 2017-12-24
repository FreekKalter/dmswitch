from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from . import app
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(250), nullable=False)
    otp_secret      = Column(String(100), nullable=False)
    alert_type      = Column(String(250), nullable=False)
    action          = Column(String(250), nullable=False)
    missed_alerts   = Column(Integer, nullable=True)
    alert_times     = Column(String(250), nullable=False)
    threshold       = Column(Integer, nullable=False)

    @property
    def smallest_diff(self):
        diff = 100000000
        for t in self.alert_times.split(' '):
            hours, minutes = t.split(':')
            now = datetime.now()
            db_time = now.replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
            seconds_diff = abs(db_time - now).total_seconds()
            if seconds_diff < diff:
                diff = seconds_diff
        return diff

    def __str__(self):
        return f'name: {self.name}\nalert_type: {self.alert_type}\naction: {self.action}\n\
                missed_alerts: {self.missed_alerts}\n threshold: {self.threshold}'


def create():
    engine = create_engine('sqlite:///' + app.config['DB_FILE'])
    Base.metadata.create_all(engine)
