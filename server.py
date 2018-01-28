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

login_manager.login_view = 'login'

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
            return redirect(url_for('friends'))
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
        schedulr.addFriend(friend_id, current_user.id)
    friends = schedulr.checkAvailable(current_user.id, 'friends')
    return render_template('friends.html', friends = friends)

@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    if request.method == 'POST':
        groupname = request.form['groupname']
        schedulr.addGroup(current_user.id, groupname)
        return redirect(url_for('group', group_name=groupname))
    groups = schedulr.getGroups(current_user.id)
    return render_template('groups.html', groups = groups)

@app.route('/groups/<group_name>', methods=['GET','POST'])
@login_required
def group(group_name):
    if request.method == 'POST':
        membername = request.form['username']
        schedulr.addUserToGroup(membername, group_name)
    groupSchedule = schedulr.getGroupCalendar(group_name)
    table = schedulr.processSchedule(groupSchedule)
    members = schedulr.groupMembers(group_name)
    availability = schedulr.checkAvailable(current_user.id, group_name)
    return render_template('group.html', group_name = group_name, group = availability, members = members, table = table)

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        event_name = request.form['eventname']
        user_name = current_user.id
        start_date = request.form['startDate']
        start_time = request.form['startTime']
        end_date = request.form['endDate']
        end_time = request.form['endTime']
        schedulr.scheduleBlock(user_name,
            event_name,
            start_date+" "+start_time,
            end_date+" "+end_time)
    schedule = schedulr.getCalendar(current_user.id)
    table = schedulr.processSchedule(schedule)
    return render_template('schedule.html', table = table)

@app.route('/import', methods=['POST'])
@login_required
def import_calendar():
    if 'calendar' not in request.files:
        return "You screwed up"
    calendar = request.files['calendar']
    if calendar.filename == '':
        return "Really screwed up"
    if calendar: # and allowed_file(file.filename)
        filename = current_user.id + "calendar.ics"
        schedulr.processCalendar(calendar, current_user.id)
        return redirect(url_for('schedule'))

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('friends'))
    return redirect(url_for('login'))

@app.route('/hello')
def hello_world():
    return 'Hello, World!'
