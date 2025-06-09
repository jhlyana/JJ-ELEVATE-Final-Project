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
            if self.connection is None or self.connection.closed:
                self.connection = psycopg2.connect(**self.db_params)
                # Set autocommit to False by default if you want to manage transactions manually
                # Otherwise, leave it as is, and psycopg2 will implicitly commit
                # self.connection.autocommit = False 
                print(" ✅  Database connected!")
            return True
        except Exception as e:
            print(f" ❌  Connection failed: {e}")
            return False

    def execute(self, query, params=None):
        try:
            # Check if connection is active, try to reconnect if not
            if self.connection is None or self.connection.closed:
                self.connect()
                if self.connection is None or self.connection.closed:
                    raise Exception("Database connection not available.")

            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if not self.connection.autocommit: # Only commit if not in autocommit mode
                    self.connection.commit()
            return True
        except Exception as e:
            print(f" ❌  Query failed: {e}")
            if not self.connection.autocommit: # Only rollback if not in autocommit mode
                self.connection.rollback()
            return False

    def fetch_all(self, query, values=None):
        try:
            # Check if connection is active, try to reconnect if not
            if self.connection is None or self.connection.closed:
                self.connect()
                if self.connection is None or self.connection.closed:
                    raise Exception("Database connection not available.")

            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, values)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching all: {e}")
            return []

    def fetch_one(self, query, values=None):
        try:
            # Check if connection is active, try to reconnect if not
            if self.connection is None or self.connection.closed:
                self.connect()
                if self.connection is None or self.connection.closed:
                    raise Exception("Database connection not available.")

            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute(query, values)
                return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching one: {e}")
            return None

    def close(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
            print(" 🔌  Database disconnected.")

    # Remove static methods if they are not intended to be used,
    # or ensure they use the *instance* of the Database class.
    # The current static methods create new connections every time,
    # which is inefficient and can lead to connection exhaustion.
    # It's better to pass the instantiated Database object around.
    # If you MUST keep them, they should be updated to manage connections properly.
    # For now, I'll assume they should be removed or refactored if they are truly static helpers.
    # Given the `MainController` now passes `self.database` to other controllers,
    # these static methods might become unnecessary.
    
    # @staticmethod
    # def fetch_all(query, values=None):
    #     db = Database()
    #     db.connect()
    #     try:
    #         with db.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    #             cursor.execute(query, values)
    #             return cursor.fetchall()
    #     except Exception as e:
    #         print(f"Error in static fetch_all: {e}")
    #         return []
    #     finally:
    #         db.close()
    
    # @staticmethod
    # def fetch_one(query, values=None):
    #     db = Database()
    #     db.connect()
    #     try:
    #         with db.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    #             cursor.execute(query, values)
    #             return cursor.fetchone()
    #     except Exception as e:
    #         print(f"Error in static fetch_one: {e}")
    #         return None
    #     finally:
    #         db.close()
    
    # @staticmethod
    # def execute(query, values=None):
    #     db = Database()
    #     db.connect()
    #     try:
    #         with db.connection.cursor() as cursor:
    #             cursor.execute(query, values)
    #             db.connection.commit()
    #             return True
    #     except Exception as e:
    #         print(f"Error in static execute: {e}")
    #         db.connection.rollback()
    #         return False
    #     finally:
    #         db.close()