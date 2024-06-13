
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
