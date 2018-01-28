#Alex Meddin Doug Moyer
#January 27, 2017
#scheduler.py

from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.exc import SQLAlchemyError

from icalendar import Calendar

from db_model import *

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

def scheduleBlock(username, event_name, start_date, end_date):
    try:
        uid = session.query(User.user_id).filter(User.username == username)
        session.add(Schedule(user_id=uid, event_name=event_name, start_time=start_date, end_time = end_date))
        session.commit()
    except SQLAlchemyError as exception:
        session.rollback()
        print("Couldn't Add Block")
        return False

def addFriend(user_id, username):

    try:
        friend_id = session.query(User.user_id).filter(
                func.lower(User.username) == func.lower(username)).scalar()
    except:
        session.rollback()
        return False

    fg_id = session.query(Group.group_id).filter(Group.owner_id == user_id,
            Group.group_name == 'friends').scalar()

    print('friend_id={}'.format(friend_id))
    print('user_id={}'.format(user_id))
    print('group_id={}'.format(fg_id))

    try:
        session.add(InGroup(group_id=fg_id,
            user_id=friend_id))
        session.commit()
    except:
        session.rollback()
        return False

    return True

def checkAvailable(user_id):

    fg_id = session.query(Group.group_id).filter(Group.owner_id == user_id,
            Group.group_name == 'friends').scalar()

    return session.query(InGroup.user_id, InGroup.user_id).filter(
            InGroup.group_id == fg_id)

def showUsers():
    conn = sqlite3.connect('schedulr.db')

    c = conn.cursor()
    c.execute('SELECT * FROM main.tusers')
    
    return False

def processCalendar(calendar, username):
    gcal = Calendar.from_ical(calendar.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            event_name = component.get('summary')
            datestart = component.decoded('dtstart')#component.get('dtstart').dt
            dateend = component.decoded('dtend')#component.get('dtend').dt
            scheduleBlock(username, event_name, datestart, dateend)
    calendar.close()
