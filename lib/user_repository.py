from lib.user import User


class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM users')
        users = []
        for row in rows:
            item = User(row["id"], row["name"], row["email"], row["password"])
            users.append(item)
        return users

    def check_email_exists(self, email):
        all_users = self.all()
        for user in all_users:
            if user.email == email:
                return True
        return False

    def create(self, user):
        self._connection.execute('INSERT INTO users(name, email, password) VALUES (%s, %s, %s)',
                                 [user.name, user.email, user.password])
        return None

    def find(self, user_id):
        # try:
        #     user_id = int(user_id)  # Attempt to convert user_id to an integer
        # except ValueError:
        #     return None
        rows = self._connection.execute('SELECT * FROM users WHERE id = %s', [user_id])
        row = rows[0]
        return User(row["id"], row["name"], row["email"], row["password"])

    def delete(self, user_id):
        self._connection.execute('DELETE FROM users WHERE id = %s', [user_id])
        return None