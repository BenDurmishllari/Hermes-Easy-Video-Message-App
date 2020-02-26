from Hermes import route

class User:

    def __init__(self, username, email, role, userId):

        self.username = username
        self.email = email
        self.userId = userId
        self.role = role
        #self.profile_image = profile_image

    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}','{self.userId}')"
