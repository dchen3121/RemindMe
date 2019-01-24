import uuid

from flask import session

from src.common.database import Database
from src.models.class_ import Class


class User(object):

    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id
        # note that username is unique, hence we do not set a uuid
        # username will be referenced as user_id in other places

    # methods to save User into database
    def json(self):
        return {
            'username':self.get_username(),
            'password':self.get_password(),
            '_id':self.get__id()
        }
    def save_to_mongo(self):
        Database.insert(collection='users',
                        data=self.json())


    # methods to get user from database
    @classmethod
    def get_user_by_username(cls, username):
        user = Database.find_one(collection='users',
                                 query={'username': username})
        if user is not None:
            return cls(**user)


    # method to get user's classes from database
    def get_classes_of_user(self):
        return Class.get_classes_by_user_id(self.get_username())



    # checking valid login
    @staticmethod
    def isvalid_login_username(username, password):
        user = Database.find_one(collection='users',
                                 query={'username': username,
                                        'password': password})
        if user is not None:
            return True
        return False


    # signup methods
    @classmethod
    def signup_with_username(cls, username, password):
        """Signs up with username and password, returns boolean on whether successful signup"""
        user = cls.get_user_by_username(username)
        if user is None:
            new_user = cls(username=username, password=password)
            new_user.save_to_mongo()
            session['username'] = username
            return True
        else:
            # username already exists in database
            return False



    # login and logout methods
    @staticmethod
    def login(username):
        session['username'] = username
    @staticmethod
    def logout():
        session['username'] = None



    # get methods
    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get__id(self):
        return self._id

    # set methods
    def set_username(self, new_username):
        self.username = new_username

    def set_password(self, new_password):
        self.password = new_password

    def set__id(self, new__id):
        self._id = new__id
