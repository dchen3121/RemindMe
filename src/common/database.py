import pymongo


class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    DATABASE = None

    @staticmethod
    def initialize():
        """Initializes the database"""
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['RemindMe']

    @staticmethod
    def insert(collection, data):
        """Inserts an item data into the collection"""
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        """Finds an item based on query given in the desired collection"""
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        """Finds one item based on query given in the desired collection"""
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        """Removes all items based on query given in the desired collection"""
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def update(collection, query, update):
        """Updates all items based on query given in the desired collection"""
        Database.DATABASE[collection].update(query, update)
