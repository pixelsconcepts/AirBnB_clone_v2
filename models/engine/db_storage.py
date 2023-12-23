#!/usr/bin/python3
"""New engine DBStorage"""


from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """Defines the DBStorage class for database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new instance of DBStorage"""
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """Query objects from the current database session"""
        diction = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for element in query:
                key = "{}.{}".format(type(element).__name__, element.id)
                diction[key] = element
        else:
            list_all = [State, City, User, Place, Review, Amenity]
            for clas in list_all:
                query = self.__session.query(clas)
                for element in query:
                    key = "{}.{}". format(type(element).__name__, element.id)
                    diction[key] = element

        return (diction)

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and the current database session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))()
