from Hermes import route

class User:

    def __init__(self, username, email, role, userId):

        self.__username = username
        self.__email = email
        self.__userId = userId
        self.__role = role
        #self.profile_image = profile_image
    
    def get_username(self):
        return self.__username
    
    def set_username(self, username):
        self.__username = username
    
    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email

    def get_userId(self):
        return self.__userId
    
    def set_userId(self, userId):
        self.__userId = userId
    
    def get_role(self):
        return self.__role
    
    def set_role(self, role):
        self.__role = role

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}','{self.userId}')"
