import sqlite3
import threading
from typing import Any, Iterable
from ..db import Database, ConnectionMode
from logger.logger import Logger

logger = Logger().get()


class SQLiteDatabase(Database):

    def __init__(self, db_path: str, mode=ConnectionMode.SINGLE):
        self.db_path = db_path
        self.mode = mode
        self.local = threading.local()

        self._shared_connection = None

        logger.debug(f"SQLiteDatabase initialized in {mode}")

    # --------------------------
    # Connection Factory
    # --------------------------
    def _create_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row

        # Performance tuning for small SBCs
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")

        return conn

    def _get_connection(self):
        # -------- Thread Local Mode --------
        if self.mode == ConnectionMode.THREAD_LOCAL:
            if not hasattr(self.local, "connection"):
                logger.debug("Creating thread-local SQLite connection")
                self.local.connection = self._create_connection()

            return self.local.connection

        # -------- Single Connection Mode --------
        else:
            if self._shared_connection is None:
                logger.debug("Creating shared SQLite connection")
                self._shared_connection = self._create_connection()

            return self._shared_connection

    # --------------------------
    # Public API
    # --------------------------
    def execute(self, query: str, params: Iterable[Any] = ()):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        conn.commit()

    def fetch(self, query: str, params: Iterable[Any] = ()):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        logger.debug("Closing database connections")

        if self._shared_connection:
            self._shared_connection.close()

        if hasattr(self.local, "connection"):
            self.local.connection.close()