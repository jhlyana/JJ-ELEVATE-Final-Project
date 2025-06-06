# database.py
import psycopg2
import psycopg2.extras

class Database:
    def __init__(self, dbname="inventory_sales_system", user="postgres", password="", host="localhost", port="5432"):
        self.connection = None
        self.db_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.db_params)
            print("✅ Database connected!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def execute(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                self.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Query failed: {e}")
            self.connection.rollback()
            return False

    def fetch_all(self, query, values=None):
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, values)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all: {e}")
            return []

    def fetch_one(self, query, values=None):
        try:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, values)
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching one: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("🔌 Database disconnected.")

    @staticmethod
    def fetch_all(query, values=None):
        db = Database()
        db.connect()
        try:
            with db.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, values)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error in static fetch_all: {e}")
            return []
        finally:
            db.close()

    @staticmethod
    def fetch_one(query, values=None):
        db = Database()
        db.connect()
        try:
            with db.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, values)
                return cursor.fetchone()
        except Exception as e:
            print(f"Error in static fetch_one: {e}")
            return None
        finally:
            db.close()

    @staticmethod
    def execute(query, values=None):
        db = Database()
        db.connect()
        try:
            with db.connection.cursor() as cursor:
                cursor.execute(query, values)
                db.connection.commit()
                return True
        except Exception as e:
            print(f"Error in static execute: {e}")
            db.connection.rollback()
            return False
        finally:
            db.close()