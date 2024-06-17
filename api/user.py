from datetime import datetime, timezone
from bson import ObjectId


#--------------------------------------------------------------- Currently not used but possible will be used in future
# def get_user(user_id, db):
#     user_data = db['users'].find_one({"_id": ObjectId(user_id)})
#     if user_data:
#         user = User(
#             user_id=str(user_data['_id']),
#             username=user_data['username'],
#             is_online=user_data.get('is_online', False),  # Set is_online based on database value
#             last_seen=user_data.get('last_seen')  # Set last_seen from database
#         )
#         return user
#     return None
#---------------------------------------------------------------

class User:
    def __init__(self, user_id, username, is_online=False, last_seen=None):
        self.id = user_id
        self.username = username
        self.is_online = is_online
        self.last_seen = last_seen  # Default to None when user is created

    def set_online(self, is_online):
        self.is_online = is_online

    def update_last_seen(self, db):
        self.last_seen = datetime.now(timezone.utc)  # Get the current time in UTC (UK)
        db['users'].update_one(
            {'_id': ObjectId(self.id)},
            {'$set': {'last_seen': self.last_seen}})

#--------------------------------------------------------------- Currently not used
# def get_id(self):
#     return str(self.id)
#
# def __eq__(self, other):
#     return self.__dict__ == other.__dict__
#
# def __repr__(self):
#     return f"User({self.id}, {self.username})"
