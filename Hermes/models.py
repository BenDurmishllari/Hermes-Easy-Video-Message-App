from Hermes import route, login_manager, auth, db
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    
    cUser = auth.current_user['localId']
    cUserDB = db.child("Users").order_by_key().equal_to(cUser).limit_to_first(1).get()
    
    return User(username = cUserDB.val().get("username"),
                email = cUserDB.val().get("email"), 
                role = cUserDB.val().get("role"), 
                userId = cUserDB.val().get("userId"),
                profile_image = cUserDB.val().get("profile_image"))

class User(UserMixin):

    def __init__(self, username, email, role, userId, profile_image):

        
        self.__username = username
        self.__email = email
        self.__role = role
        self.__userId = userId
        self.__profile_image = profile_image
    
    
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__userId)

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

    # def get_userId(self):
    #     return self.__userId
    
    def set_userId(self, userId):
        self.__userId = userId
    
    def get_profile_image(self):
        return str(self.__profile_image)
    
    def set_profile_image(self, profile_image):
        self.__profile_image = profile_image
    
    
     
    def __repr__(self):
        return f"User('{self.__userId}','{self.__username}', '{self.__email}','{self.__role}', '{self.__profile_image}'')"
