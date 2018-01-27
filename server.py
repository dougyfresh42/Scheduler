from flask import Flask, request
app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        True # do_the_login()
    else:
        False # show_the_login_form()
    return 'Login Page'

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    return 'Hello, World!'
