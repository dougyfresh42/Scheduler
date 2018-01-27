import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
import schedulr

# App setup
app = Flask(__name__)

UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = set(['ics'])

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret tunnel',
    UPLOAD_FOLDER = UPLOAD_FOLDER
)

# Login Manager Setup
# Perhaps we move the user class to a different file
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, username):
        self.name = username + "ABC"
        self.id = username

@login_manager.user_loader
def load_user(username):
    return User(username)

# App endpoints
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if schedulr.login(username, password):
            login_user(User(username))
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if schedulr.signup(username, password):
            login_user(User(username))
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    if request.method == 'POST':
        friend_id = request.form['friend_id']
        schedulr.addFriend(current_user.id, friend_id)
    friends = schedulr.checkAvailable(current_user.id)
    print(friends)
    return render_template('friends.html', friends = friends)

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        True
    else:
        False
    return render_template('schedule.html')

@app.route('/import', methods=['POST'])
@login_required
def import_calendar():
    print(request.files)
    if 'calendar' not in request.files:
        return "You screwed up"
    calendar = request.files['calendar']
    if calendar.filename == '':
        return "Really screwed up"
    if calendar: # and allowed_file(file.filename)
        filename = current_user.id + "calendar.ics"
        schedulr.processCalendar(calendar)
        return redirect(url_for('schedule'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello_world():
    return 'Hello, World!'
