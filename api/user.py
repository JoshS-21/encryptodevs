from flask_login import UserMixin
from bson import ObjectId

class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.is_online = False  # Default to False when user is created

    def set_online(self, is_online):
        self.is_online = is_online

    def is_authenticated(self):
        return super().is_authenticated() and self.is_online

    @classmethod
    def get_user(cls, user_id, db):
        user_data = db['users'].find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(
                user_id=str(user_data['_id']),
                username=user_data['username'],
            )
        return None

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.id}, {self.username})"
