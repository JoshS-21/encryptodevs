from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, name, email, password, login_status):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.login_status = login_status

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.email}, {self.password}, {self.login_status})"
