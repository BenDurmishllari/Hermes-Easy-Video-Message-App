from Hermes import route, login_manager, auth, db
from flask_login import UserMixin
from flask import session

# @login_manager.user_loader
# def load_user(user_id):
    
#     # cUserID = "ayHjTbjQOncuWUClEv99nAitN2n1"
#     # cUserDB = db.child("Users").order_by_key().equal_to(cUserID).limit_to_first(1).get()
   
#     user = User(username = "op",
#                 email = "op@gmail.com", 
#                 role = "Admin", 
#                 id = "ayHjTbjQOncuWUClEv99nAitN2n1",
#                 profile_image = "https://firebasestorage.googleapis.com/v0/b/hermes-d58c7.appspot.com/o/profile_pic%2Fop%40gmail.com%2FayHjTbjQOncuWUClEv99nAitN2n1?alt=media&token=ayHjTbjQOncuWUClEv99nAitN2n1")
    
#     return user
#     # return User(username = cUserDB.val().get("username"),
#     #             email = cUserDB.val().get("email"), 
#     #             role = cUserDB.val().get("role"), 
#     #             userId = cUserDB.val().get("userId"),
#     #             profile_image = cUserDB.val().get("profile_image"))
#     # return cUserDB[0].val()

# @login_manager.user_loader
# def load_user(user_id):
    
#     cUser = "ayHjTbjQOncuWUClEv99nAitN2n1"
   
#     cUserDB = db.child("Users").order_by_key().equal_to(cUser).limit_to_first(1).get()
#     user = User(username = cUserDB.val().get("username"),
#                 email = cUserDB.val().get("email"), 
#                 role = cUserDB.val().get("role"), 
#                 id = cUserDB.val().get("id"),
#                 profile_image = cUserDB.val().get("profile_image"))
#     return cUserDB.val()

# @login_manager.user_loader
# def load_user(user_id):
#     #s = session['_user_id']
#     user_id = "ayHjTbjQOncuWUClEv99nAitN2n1"
#     cUserDB = db.child("Users").order_by_key().equal_to(user_id).limit_to_first(1).get()
	
#     #print(session['_user_id'])
 
#     return User (username = cUserDB.val().get("username"),
#                  email = cUserDB.val().get("email"), 
#                  role = cUserDB.val().get("role"), 
#                  id = cUserDB.val().get("id"),
#                  profile_image = cUserDB.val().get("profile_image"))

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

    # def get_userId(self):
    #     return self.__userId
    
    def set_Id(self, id):
        self.__id = id
    
    def get_profile_image(self):
        return str(self.__profile_image)
    
    def set_profile_image(self, profile_image):
        self.__profile_image = profile_image
    
    
     
    def __repr__(self):
        return f"User('{self.__id}','{self.__username}', '{self.__email}','{self.__role}', '{self.__profile_image}'')"
