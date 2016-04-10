import os
import sys
import psycopg2
#from datetime import datetime
from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from sqlalchemy_utils import ArrowType
import arrow,string
from sqlalchemy import Column, types,ForeignKey, Integer, String, Boolean, Binary, CHAR,DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref ,sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime
from sqlalchemy_utils import database_exists, create_database
import json

#this object will help set up when writing the class code
Base = declarative_base()


#create an instance of create_engine class
#and point to the database to be used
#engine = create_engine('postgresql://postgres:bury148few951@localhost:5432/postgres',echo=True)
engine = create_engine('postgresql://postgres:0102443167@localhost:5432/culturedb',echo=True)

Base.metadata.bind = (engine)

DBSession = sessionmaker(bind=engine,autoflush=True,expire_on_commit=True, _enable_transaction_accounting=True, autocommit=False)
session = DBSession()

#constant postgres database
DATABASE = engine

class User(UserMixin , Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    title = Column(CHAR(3), nullable = True)
    fname = Column(String(100), nullable = True)
    lname = Column(String(100), nullable = True)
    DateOfBirth = Column(ArrowType, default = arrow.utcnow())
    username = Column(String(100), nullable = False, unique = True)
    email = Column (String(50), nullable =False, unique = True)
    password = Column(String(100), nullable = False)
    address = Column(String(250), nullable = True)
    state = Column(String(50), nullable = True)
    is_Admin = Column(Boolean ,default = False)
    is_Logged = Column(Boolean, default = False)
    is_Active = Column (Boolean , default = False)
    is_Block = Column(Boolean, default = False)
    joined_On = Column(ArrowType, default=arrow.utcnow())
    


    @classmethod
    def create_user(self,fname, lname,username,email,password,address,state,title, is_Admin = False):
        try:
            session = DBSession()
            myFirstUser = User(
                title = title,
                fname = fname,
                lname = lname,
                username = username,
                email = email,
                password = generate_password_hash(password),
                address = address,
                state = state,
                is_Admin = is_Admin)


            session.add(myFirstUser)
            session.commit()

        except IntegrityError :
            # recreate the session and re-add your object
            session = DBSession()
            session.add(User)
            raise ValueError('user Already Exist !')



    def is_authenticated(self):
        return self.is_Logged

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return True;\

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key =True)
    title = Column(String(250), nullable = False)
    description = Column(String(500), nullable = False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User',backref=backref("products", cascade="all, delete-orphan"),lazy='joined')

class ProductItem(Base):
    __tablename__ ='product_items'
    id = Column(Integer , primary_key = True)
    image_url = Column(String(500) , unique= False)
    image_description = Column(String(500), nullable = False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship('Product',backref=backref("productitems", cascade="all, delete-orphan"),lazy='joined' )

    @property
    def serialize(self):
        return to_json(self, self.__class__)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")
def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        print 'it would hit here'
        print v
        if c.type in convert.keys() and v is not None:
            try:
                if isinstance(v, datetime.datetime):
                    d[c.name] = json_serial(v)
                else :    
                    d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            if isinstance(v, datetime.datetime):
                d[c.name] = json_serial(v)
            else:
                d[c.name] = v
    return json.dumps(d)


#initialize the module. Its called from app.py to initialize process
def initialize(re_createTable= False):
    if re_createTable :
        if not database_exists(engine.url):
            create_database(DATABASE.url)

        print(database_exists(engine.url))
        Base.metadata.drop_all(DATABASE, checkfirst = True)


    Base.metadata.create_all(DATABASE, checkfirst = True)

def InsertRow(table =None):
    session = DBSession()
    session.add(table)
    session.commit()
    session.refresh(table)

    p_key = table.id

    return p_key
#def DeleteRow(table=None):
