import pymongo
from pymongo import MongoClient

class DataClient:
    def __init__(self):
        super().__init__()

    def connect_to_client(self, connect_string):
        try:
            # connect to MongoDB Database
            client = MongoClient(connect_string)
            db = client["ImageLocator_AI"]

            # creates collections if they don't already exist in database
            self.collectionExists("User", db)
            self.collectionExists("Image", db)
            self.collectionExists("Location", db)
            return client
     
        except ConnectionError as cerr:
            print(f"Error in MongoDB connection: {cerr}")

        except RuntimeError as rerr:
            print(f"Runtime error: {rerr}")

        except TypeError as terr:
            print(f"Invlaid type detected: {terr}")

        except pymongo.errors.OperationFailure as operr:
            print(f"Error in MongoDB authentication: {operr}")

        except pymongo.errors.ServerSelectionTimeoutError as sserr:
            print(f"Connection/socket timeout error: {sserr}")  

    # checks if collection already exists, if so --> exception is thrown. If not, collection is instantiated
    def collectionExists(self, collection_name, database):
        try:
            database.create_collection(collection_name)

        except pymongo.errors.CollectionInvalid:
            print("This collection already exists")