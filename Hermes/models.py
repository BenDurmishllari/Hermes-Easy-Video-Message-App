from Hermes import route


class User():

    def __init__(self, username, email, role, userId):

        self.__username = username
        self.__email = email
        self.__role = role
        self.__userId = userId
        # self.__tokenId = tokenId
        
        #self.profile_image = profile_image
    
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

    def get_userId(self):
        return self.__userId
    
    def set_userId(self, userId):
        self.__userId = userId
     
    def __repr__(self):
        return f"User('{self.__username}','{self.__email}', '{self.__userId}','{self.__role}'')"
