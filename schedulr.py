import sqlite3

def login(username, password):
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('SELECT * FROM main.tusers WHERE Username = ? AND Password = ?',
        (username, password))

    userrow = c.fetchone()
    c.close()
    if userrow is None:
        print("Login Failed")
        return False
    
    userID = userrow[0]
    return True

def signup(username, password):
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('INSERT INTO main.tusers (Username, Password) values (?, ?)',
        (username, password))
    conn.commit()
    c.close()

    return login(username, password)

def scheduleBlock():
    return False

def addFriend():
    return False

def checkAvailable():
    return False

def showUsers():
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('SELECT * FROM main.tusers')
    
    return False
