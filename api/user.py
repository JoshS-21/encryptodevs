from bson import ObjectId


def get_user(user_id, db):
    user_data = db['users'].find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(
            user_id=str(user_data['_id']),
            username=user_data['username'],
            is_online=user_data.get('is_online', False)  # Set is_online based on database value
        )
    return None


class User:
    def __init__(self, user_id, username, is_online=False):
        self.id = user_id
        self.username = username
        self.is_online = is_online

    def set_online(self, is_online):
        self.is_online = is_online

    def is_authenticated(self):
        return self.is_online

    def get_id(self):
        return str(self.id)


def __eq__(self, other):
    return self.__dict__ == other.__dict__


def __repr__(self):
    return f"User({self.id}, {self.username})"
