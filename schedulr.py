import sqlite3

conn = sqlite3.connect('schedulr.db')

loggedIn = False
userID = 0

def login(username = None, password = None):
    global loggedIn, userID
    if loggedIn:
        print("You already logged in")
        return False
    if username is None:
        username = input("Username: ")
    if password is None:
        password = input("Password: ")
    c = conn.cursor()
    c.execute('SELECT * FROM main.tusers WHERE Username = ? AND Password = ?',
        (username, password))

    userrow = c.fetchone()
    c.close()
    if userrow is None:
        print("Login Failed")
        return False
    
    loggedIn = True
    userID = userrow[0]

    return True

def signup():
    username = input("What username would you like to use? ")
    password = input("Input a password: ")
    c = conn.cursor()
    c.execute('INSERT INTO main.tusers (Username, Password) values (?, ?)',
        (username, password))
    conn.commit()
    c.close()

    return login(username = username, password = password)

def scheduleBlock():
    return False

def addFriend():
    return False

def checkAvailable():
    return False

def showUsers():
    c = conn.cursor()
    c.execute('SELECT * FROM main.tusers')
    
    return False

if __name__ == "__main__":
    command = ''
    while command != 'q':
        command = input('What would you like to do? ')
        if command == 'h':
            print('Help Menu')
        elif command == 's':
            signup()
        elif command == 'l':
            login()
        elif command == 'f':
            addFriend()
        elif command == 'c':
            scheduleBlock()
        elif command == 'u':
            showUsers()
        elif command == '?':
            checkAvailable()
