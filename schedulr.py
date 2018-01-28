#Alex Meddin Doug Moyer
#January 27, 2017
#scheduler.py

from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import *
import datetime

from icalendar import Calendar

from db_model import *

Session = sessionmaker(bind=engine)
session = Session()
session.rollback()

def getUID(username):

    try:
        return session.query(User.user_id).filter(func.lower(User.username) ==
            func.lower(username)).scalar()
    except:
        session.rollback()
        print("user_id lookup failed")
        return False

def login(username, password):

    try:
        return session.query(User).filter(func.lower(User.username) == 
            func.lower(username), User.password == password).count()
    except:
        session.rollback()
        return False

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
        session.add(Schedule(user_id=uid, event_name=event_name,
            start_time=start_date, end_time = end_date))
        session.commit()
    except SQLAlchemyError as exception:
        session.rollback()
        print("Couldn't Add Block")
        return False

def addFriend(username_, username):

    user_id = getUID(username_)
    
    try:
        friend_id = session.query(User.user_id).filter(
                func.lower(User.username) == func.lower(username)).scalar()
    except:
        session.rollback()
        print("friend_id lookup failed")
        return False

    try:
        fg_id = session.query(Group.group_id).filter(Group.owner_id == user_id,
            Group.group_name == 'friends').scalar()
    except:
        session.rollback()
        print("friend-group lookup failed")
        return False

    try:
        session.add(InGroup(group_id=fg_id,
            user_id=friend_id))
        session.commit()
    except:
        session.rollback()
        print("adding friend failed")
        return False

    return True

def checkAvailable(username):

    user_id = getUID(username)

    try:
        fg_id = session.query(Group.group_id).filter(Group.owner_id == user_id,
            Group.group_name == 'friends').scalar()
    except:
        session.rollback()
        print("friend group lookup failed")
        return False
    
    # retrieve all current events and end times
    try:
        busy = session.query(Schedule.event_id, Schedule.user_id,
            Schedule.end_time).filter(Schedule.start_time <= 
                    datetime.datetime.now(),
                    Schedule.end_time >= datetime.datetime.now()).subquery()
        late_events = session.query(Schedule.event_id, Schedule.user_id,
            Schedule.start_time).filter(Schedule.start_time >= 
                    datetime.datetime.now(),
                    ~exists().where(busy.c.user_id == Schedule.user_id)).\
                    subquery()
        next_event = session.query(late_events.c.event_id,
                func.min(late_events.c.start_time).\
            label("min_id")).group_by(late_events.c.user_id).subquery()
        free = session.query(late_events.c.event_id, late_events.c.user_id,
            late_events.c.start_time).join(next_event,
                    late_events.c.event_id == next_event.c.event_id).subquery()
    except:
        session.rollback()
        print("couldn't retrieve current events")
        return False

    return_array = []
    for row in session.query(busy).all():
        return_array.append([row[0],row[1],None,row[2]])
    for row in session.query(free).all():
        return_array.append([row[0],row[1],row[2],None])

    try:
        return return_array
    except:
        session.rollback()
        print("friend return failed")
        return False

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
