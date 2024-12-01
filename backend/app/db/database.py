from pymongo import MongoClient, ASCENDING
from pymongo import database
from pymongo.server_api import ServerApi
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Optional


class MongoDB:
    def __init__(self, url, db_name):
        self._client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
        self.url = url
        self.db_name = db_name

    def connect(self):
        print(f"Trying to connect to {self.db_name}")
        self._client = MongoClient(self.url, server_api=ServerApi("1"))

        self.database = self._client[self.db_name]
        print("Connected to MongoDB")

    def get_collection(self, collection_name: str) -> Collection:
        """Retrieve a specific collection from the database."""
        if self.database is None:
            raise Exception(
                "Database connection not established. Call `connect()` first."
            )
        return self.database[collection_name]

    def drop(self):
        """Drop the database"""
        if self.database is None:
            raise Exception(
                "Database connection not established. Call `connect()` first."
            )
        if self._client:
            self._client.drop_database(self.database)

    def close(self):
        """Close the database connection."""
        if self._client:
            self._client.close()
            print("MongoDB connection closed.")
