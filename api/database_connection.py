import os
from flask import g
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    DEV_DATABASE_NAME = os.getenv('MONGODB_DATABASE')
    TEST_DATABASE_NAME = "encryptodevs_test"

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(os.getenv('MONGODB_URL'))
            self.db = self.client[self._database_name()]
        except Exception as e:
            raise Exception(f"Couldn't connect to the database {self._database_name()}! Error: {str(e)}")

    def seed(self, collection_name, documents):
        self._check_connection()
        collection = self.db[collection_name]
        collection.insert_many(documents)

    def execute(self, collection_name, query, projection=None):
        self._check_connection()
        collection = self.db[collection_name]
        return list(collection.find(query, projection))

    CONNECTION_MESSAGE = (
        'DatabaseConnection.exec_params: Cannot run a query as '
        'the connection to the database was never opened. Did you '
        'make sure to call first the method DatabaseConnection.connect` '
        'in your app.py file (or in your tests)?'
    )

    def _check_connection(self):
        if self.client is None or self.db is None:
            raise Exception(self.CONNECTION_MESSAGE)

    def _database_name(self):
        return self.TEST_DATABASE_NAME if self.test_mode else self.DEV_DATABASE_NAME

# This function integrates with Flask to create one database connection that
# each Flask request can use. To see how to use it, look at example_routes.py
def get_flask_database_connection():
    if not hasattr(g, 'flask_database_connection'):
        g.flask_database_connection = DatabaseConnection(
            test_mode=os.getenv('APP_ENV') == 'test'
        )
        g.flask_database_connection.connect()
    return g.flask_database_connection