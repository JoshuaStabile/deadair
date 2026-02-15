import sqlite3
from typing import Any, Iterable
from ..db import Database


class SQLiteDatabase(Database):

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def connect(self) -> None:
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # allows dict-like access

    def close(self) -> None:
        if self.connection:
            self.connection.close()

    def execute(self, query: str, params: Iterable[Any] = ()) -> None:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()

    def fetch_all(self, query: str, params: Iterable[Any] = ()) -> list:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query: str, params: Iterable[Any] = ()) -> Any:
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
