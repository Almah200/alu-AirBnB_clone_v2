
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.city import City
from models.state import State
from models.place import Place
from models.user import User


class DBStorage:
    __engine = None
    __session = None
    classes = {
        'City': City,
        'State': State,
        'Place': Place,
        'User': User
    }

    def __init__(self):
        """innitialize instance"""
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        user = os.getenv('HBNB_MYSQL_USER')
        self.__engine = sqlalchemy.create_engine(
            'mysql+mysqldb://{}:{}@{}:3306/{}'.format(user, password, host, database), pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """get all objects or objects of certain type"""
        data = {}
        if cls == None or cls.__name__ not in self.classes:
            for i in self.classes.keys():
                queried = self.__session.query(self.classes[i]).all()
                for j in queried:
                    key = j.__class__.__name__ + "." + j.id
                    data[key] = j.to_dict()
        else:
            queried = self.__session.query(cls).all()
            for j in queried:
                key = j.__class__.__name__ + "." + j.id
                data[key] = j.to_dict()
        return data

    def new(self, obj):
        """add a new obj"""
        self.__session.add(obj)

    def save(self):
        """commit to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj"""
        if obj != None:
            self.__session.delete(obj)

    def reload(self):
        """reload db"""
        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(session_maker)
        self.__session = session()