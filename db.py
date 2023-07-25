""" Connecting to mongodb Atlas"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from starlette.config import Config

class ConnectDB:
    def __init__(self) -> None:
        self.conn = None

    def get_collection(self):
        try:
            config = Config('.env')
            DBName = config('DBNAME')
            collectionName = config('COLLECTION_NAME')
            USER = config('USER')
            PASS = config('PASS')
            self.conn = MongoClient(f'mongodb+srv://{USER}:{PASS}@cluster0.l6yrrcu.mongodb.net/')
            self.db = self.conn[DBName]
            collection = self.db[collectionName]
            return collection
        except ConnectionFailure as err:
            print("Could not connect to the MongoDB database:", err)

    def close(self):
        self.conn.close()