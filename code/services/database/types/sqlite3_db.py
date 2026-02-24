import sqlite3
from typing import Any, Iterable
from ..db import Database
from logger.logger import Logger


logger = Logger().get()

class SQLiteDatabase(Database):

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        
        logger.debug("SQLiteDatabase initialized")

    def connect(self) -> None:
        logger.debug("Connecting to SQLite db")
        
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # allows dict-like access

    def close(self) -> None:
        logger.debug("Closing connection to SQLite db")
        
        if self.connection:
            self.connection.close()

    def execute(self, query: str, params: Iterable[Any] = ()) -> None:
        logger.debug("Executing SQL Query: " + query)
        
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        
    def fetch(self, query: str, params: Iterable[Any] = ()):
        logger.debug("Executing SQL Query: " + query)

        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
