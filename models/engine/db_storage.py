#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import os


class DBStorage:
    """This class manages storage of hbnb models in a database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the storage engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')
        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}', pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            objects = self.__session.query(User).all() + self.__session.query(State).all() + self.__session.query(City).all() + self.__session.query(Amenity).all() + self.__session.query(Place).all() + self.__session.query(Review).all()
        else:
            objects = self.__session.query(cls).all()
        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in objects}

    def new(self, obj):
        """Adds new object to storage database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Call remove method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve one object based on class and ID"""
        if cls is None or id is None:
            return None
        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """Count the number of objects in storage matching the given class"""
        if cls is None:
            return sum(len(self.__session.query(model).all()) for model in [User, State, City, Amenity, Place, Review])
        return len(self.__session.query(cls).all())
