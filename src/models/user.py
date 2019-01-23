from flask import session

from src.common.database import Database


class User(object):

    def __init__(self, username, password, email=None):
        self.username = username
        self.password = password
        self.email = email
        # note that username and email are unique, hence we do not set a uuid
        # username will be referenced as user_id in other places
        # username and passwrod will always exist but email is optional for a user account


    # methods to save User into database
    def json(self):
        return {
            'username':self.get_username(),
            'password':self.get_password(),
            'email':self.get_email()
        }
    def save_to_mongo(self):
        Database.insert(collection='users',
                        data=self.json())


    # methods to get user from database
    @classmethod
    def get_user_by_username(cls, username):
        user = Database.find_one(collection='user',
                                 query={'username': username})
        return cls(**user)
    @classmethod
    def get_user_by_email(cls, email):
        user = Database.find_one(collection='user',
                                 query={'email': email})
        return cls(**user)


    # checking valid login
    @staticmethod
    def isvalid_login_username(username, password):
        user = Database.find_one(collection='user',
                                 query={'username': username,
                                        'password': password})
        if user is not None:
            return True
        return False
    @staticmethod
    def isvalid_login_email(email, password):
        user = Database.find_one(collection='user',
                                 query={'email': email,
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
    @classmethod
    def signup_with_email(cls, email, password):
        """Signs up with email and password, returns boolean on whether successful signup"""
        user = cls.get_user_by_email(email)
        if user is None:
            username = input()  # to be changed later to prompt_for_enter_username
            new_user = cls(username=username, password=password, email=email)
            new_user.save_to_mongo()
            session['username'] = username
            # ensure that user has a username
            return True
        else:
            return False
    @staticmethod
    def prompt_for_enter_username():
        pass



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

    def get_email(self):
        return self.email

    # set methods
    def set_username(self, new_username):
        self.username = new_username

    def set_password(self, new_password):
        self.password = new_password

    def set_email(self, new_email):
        self.email = new_email
