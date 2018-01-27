from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import schedulr

# App setup
app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret tunnel'
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

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    if request.method == 'POST':
        True
    else:
        False
    return 'Scheduling page'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello_world():
    return 'Hello, World!'
