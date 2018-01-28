#Alex Meddin Doug Moyer
#January 27, 2017
#db_model.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import*

engine = create_engine('mysql://testuser:1234@129.21.104.170:3306/schedulr_db', echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(40), unique=True)
    password = Column(String(40))

    def __repr__(self):
        return "<User(id='%i', username='%s', password='%s')>" % (
                             self.user_id, self.username, self.password)

class Group(Base):
    __tablename__ = 'groups'

    group_id = Column(Integer, primary_key=True, nullable=False)
    group_name = Column(String(40))
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return "<User(id='%i', name='%s', owner id='%i')>" % (
                             self.group_id, self.group_name, self.owner_id)

class InGroup(Base):
    __tablename__ = 'in_group'

    group_id = Column(Integer, primary_key=True, nullable=False,
            unique=False)
    user_id = Column(Integer, ForeignKey('users.user_id'),
            primary_key=True, nullable=False, unique=False)

    def __repr__(self):
        return "<User(id='%i', user id='%i')>" % (
                             self.group_id, self.user_id)
        
class Schedule(Base):
    __tablename__ = 'schedule'

    event_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    event_name = Column(String(40))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    def __repr__(self):
        return "<User(id='%i', user id='%i', event_name='%s')>" % (
                             self.event_id, self.user_id, self.event_name)

Base.metadata.create_all(engine)

