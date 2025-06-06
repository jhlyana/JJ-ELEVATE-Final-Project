# core/models/OInventoryModel.py
import psycopg2

class InventoryModel:
    def __init__(self, db_conn):
        self.conn = db_conn

    def get_all_products(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products ORDER BY product_id ASC")
        return cur.fetchall()

    def add_product(self, name, category, quantity, price):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO products (product_name, category, quantity, price) VALUES (%s, %s, %s, %s)",
            (name, category, quantity, price)
        )
        self.conn.commit()

    def update_product(self, product_id, quantity, price):
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE products SET quantity = %s, price = %s WHERE product_id = %s",
            (quantity, price, product_id)
        )
        self.conn.commit()

    def delete_product(self, product_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        self.conn.commit()