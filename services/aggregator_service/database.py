from pymongo import MongoClient
import psycopg2
from config import Config, logger
from typing import List, Dict
from contextlib import contextmanager

class DatabaseConnection:
    @contextmanager
    def get_redshift_cursor(self):
        conn = None
        try:
            conn = psycopg2.connect(**Config.REDSHIFT_CONFIG)
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Redshift operation failed: {str(e)}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_mongo_client(self):
        try:
            client = MongoClient(Config.MONGO_URL)
            return client[Config.MONGO_DB_NAME]
        except Exception as e:
            logger.error(f"MongoDB connection failed: {str(e)}")
            raise