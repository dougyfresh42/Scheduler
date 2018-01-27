from icalendar import Calendar
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

def addFriend(username, friend):
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('INSERT INTO main.tFriends (User, Friend) values (?, ?)',
        (username, friend))
    conn.commit()
    c.close()
    return True

def checkAvailable(username):
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('SELECT Friend, 1 FROM main.tFriends WHERE User = ?', (username,))
    return c.fetchall()

def showUsers():
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('SELECT * FROM main.tusers')
    
    return False

def processCalendar(calendar):
    gcal = Calendar.from_ical(calendar.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            print(component.get('summary'))
            print(component.get('dtstart'))
    calendar.close()
