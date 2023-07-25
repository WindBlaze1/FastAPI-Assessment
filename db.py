""" Connecting to mongodb Atlas"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from starlette.config import Config

class ConnectDB:
    """ A Wrapper class for pymongo and Atlas """
    def __init__(self) -> None:
        self.conn = None

    def get_collection(self):
        """ Get the pymongo collection connection to db """
        try:
            config = Config('.env')
            DBName = config('DBNAME')
            collectionName = config('COLLECTION_NAME')
            USER = config('USER')
            PASS = config('PASS')
            CLUSTER_URL = config('CLUSTER_URL')
            self.conn = MongoClient(f'mongodb+srv://{USER}:{PASS}@{CLUSTER_URL}/')
            self.db = self.conn[DBName]
            collection = self.db[collectionName]
            return collection
        except ConnectionFailure as err:
            print("Could not connect to the MongoDB database:", err)

    def close(self):
        """ To close the connection to db. """
        self.conn.close()