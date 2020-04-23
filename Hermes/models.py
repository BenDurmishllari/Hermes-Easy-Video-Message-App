from Hermes import route, login_manager, auth, db
from flask_login import UserMixin
from flask import session



class User(UserMixin):

    def __init__(self, username, email, role, id, profile_image):

        
        self.__username = username
        self.__email = email
        self.__role = role
        self.__id = id
        self.__profile_image = profile_image
    
    
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__id)

    def get_username(self):
        return self.__username
    
    def set_username(self, username):
        self.__username = username
    
    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email
    
    def get_role(self):
        return self.__role
    
    def set_role(self, role):
        self.__role = role
    
    def set_Id(self, id):
        self.__id = id
    
    def get_profile_image(self):
        return str(self.__profile_image)
    
    def set_profile_image(self, profile_image):
        self.__profile_image = profile_image
    
    
     
    def __repr__(self):
        return f"User('{self.__id}','{self.__username}', '{self.__email}','{self.__role}', '{self.__profile_image}'')"
