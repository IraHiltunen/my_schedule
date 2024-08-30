from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    price = Column(Integer, default=0, nullable=False)

    # def __init__(self, name=None, email=None):
    #     self.name = name
    #     self.email = email
    #
    # def __repr__(self):
    #     return f'<User {self.name!r}>'

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    birth_date = Column(String(30))#, default='1940-01-01')
    racket_tension = Column(String(20))
    phone = Column(String(50), nullable=False)
    email = Column(String(50),  nullable=False)

class Court(Base):
    __tablename__ = 'court'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    coach_payment = Column(Integer, default=0)
    business_time_cost = Column(Integer, nullable=False)
    regular_time_cost = Column(Integer, nullable=False)
    weekend_time_cost = Column(Integer, nullable=False)
    phone = Column(String(50), nullable=False)
    type_of_courts = Column(String(50), nullable=False)

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    court_id = Column(Integer, ForeignKey(Court.id))
    client_id = Column(Integer, ForeignKey(Client.id), nullable=False)
    service_id = Column(Integer, ForeignKey(Service.id), nullable=False)
    date = Column(String(20), nullable=False)
    time = Column(String(10), nullable=False)
    # можливо тут можна додати метод (тільки переробити його)
    # def add_funds(self, amount):
    #     if amount is not None and amount > 0:
    #         self.funds += amount

class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date = Column(String(20), nullable=False)
    service_id = Column(Integer, ForeignKey(Service.id), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)





