from flask import render_template, make_response, request
from . import app, dmswitch, declarative
from functools import wraps
import os


def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator


@app.route('/')
@add_response_headers({'Cache-Control': 'no-cache'})
def index():
    return 'welcome'


@app.route('/<username>')
@add_response_headers({'Cache-Control': 'no-cache'})
def user_landing(username):
    return render_template('index.html')


@app.route('/<username>/info')
def user_info(username):
    return dmswitch.user_info(username)


@app.route('/checkin', methods=["POST"])
def beep():
    username = request.form['username']
    token = request.form['token']
    if username == '' or token == '':
        return 'invalid username or token'
    return dmswitch.validate(username, token)


@app.route('/checkin/<username>/<token>', methods=["GET"])
def checkin(username, token):
    return dmswitch.validate(username, token)


@app.route('/test_alert')
def test_alert():
    dmswitch.interval_check(debug=True)
    return 'send alert'


@app.route('/create_db')
def create_db():
    os.unlink(app.config['DB_FILE'])
    declarative.create()
    return 'created db'


@app.route('/newuser/<username>')
def newuser(username):
    create_db()  # REMOVE THIS AFET TESTING
    dmswitch.create_user(username, otp_secret='TANX PIGC TPJY WQBW')
    return f'<a href="/{username}">{username}</a> created'
