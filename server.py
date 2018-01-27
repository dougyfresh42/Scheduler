from flask import Flask, request, render_template
import schedulr
app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        True # do_the_login()
        print("Posted")
    else:
        False # show_the_login_form()
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    else:
        False
    return 'Register Page'

@app.route('/schedule', methods=['GET', 'POST'])
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
