# import sqlalchemy.orm

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    addresses = relationship('Address', uselist=True)

    def __init__(self, name, username):
        self.name = name
        self.username = username


class Address(Base):
    __tablename__ = 'user_address'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, address):
        self.address = address


engine = create_engine('sqlite:///:memory:', echo=True)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

user = User('Jeff', 'jeff1111')
session.add(user)
session.commit()

user = session.query(User).first()
print(user.addresses)
print(user.addresses)