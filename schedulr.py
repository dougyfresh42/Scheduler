#Alex Meddin Doug Moyer
#January 27, 2017
#scheduler.py

from sqlalchemy.orm import *
from sqlalchemy import *

from icalendar import Calendar

from db_model import *

engine = create_engine('mysql://testuser:1234@localhost:3306/schedulr_db', 
        echo=True)

Session = sessionmaker(bind=engine)
session = Session()
session.rollback()

def login(username, password):

    return session.query(User).filter(func.lower(User.username) == 
            func.lower(username), User.password == password).count()

def signup(username, password):
    
    if (session.query(User).filter(func.lower(User.username) == 
        func.lower(username)).count()):
        print("User exists")
        return False

    try:
        session.add(User(username=username, password=password))
        session.commit()
    except SQLAlchemyError as exception:
        session.rollback()
        return False

    uid = session.query(User.user_id).filter(User.username == 
            username)

    try:
        session.add(Group(group_name='friends', owner_id=uid))
        session.commit()
    except SQLAlchemyError as exception:
        session.rollback()
        return False
    
    return login(username, password)

def scheduleBlock():
    return False

def addFriend(user_id, username):

    friend_id = session.query(User.user_id).filter(func.lower(User.username) ==
            func.lower(username))
    fg_id = session.query(Group.group_id).filter(Group.owner_id == user_id,
            Group.group_name == 'friends')

    print("friend_id='%i'",friend_id)

    try:
        session.add(InGroup(group_id=fg_id,
            user_id=friend_id))
        session.commit()
    except SQLAlchemyError as exception:
        session.rollback()
        return False

    return True

def checkAvailable(user_id):

    fg_id = session.query(Group.group_id).filter(Group.owner_id == user_id,
            Group.group_name == 'friends')

    return session.query(InGroup.user_id).filter(InGroup.group_id == fg_id)

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
            print(component.get('dtstart').dt)
    calendar.close()
