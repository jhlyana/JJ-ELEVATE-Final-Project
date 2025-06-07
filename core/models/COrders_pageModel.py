from database import Database
from datetime import datetime

class OrdersModel:
    def __init__(self, database):
        self.database = database
        if not self.database.connection:
            self.database.connect()

    def get_all_products(self):
        """Get all products with their specifications from database"""
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                t.prod_type_name,
                p.product_price,
                p.product_source as stock_city,
                p.product_updated_at,
                ps.prod_spec_stock_qty,
                ps.prod_spec_color,
                ps.prod_spec_length_mm,
                ps.prod_spec_thickness_mm,
                ps.prod_spec_width_mm,
                ps.prod_spec_other
            FROM product p
            JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification ps ON p.product_id = ps.product_id AND p.shop_id = ps.shop_id
            ORDER BY t.prod_type_name, p.product_name
        """
        try:
            cursor = self.database.connection.cursor()
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Database error getting all products: {e}")
            return []

    def get_products_by_type(self, product_type):
        """Get products filtered by type from database"""
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                t.prod_type_name,
                p.product_price,
                p.product_source as stock_city,
                p.product_updated_at,
                ps.prod_spec_stock_qty,
                ps.prod_spec_color,
                ps.prod_spec_length_mm,
                ps.prod_spec_thickness_mm,
                ps.prod_spec_width_mm,
                ps.prod_spec_other
            FROM product p
            JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification ps ON p.product_id = ps.product_id AND p.shop_id = ps.shop_id
            WHERE t.prod_type_name = %s
            ORDER BY p.product_name
        """
        try:
            cursor = self.database.connection.cursor()
            cursor.execute(query, (product_type,))
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"Database error getting products by type: {e}")
            return []

    def get_product_details(self, product_id):
        """Get detailed information for a specific product from database"""
        query = """
            SELECT 
                p.product_id,
                p.product_name,
                t.prod_type_name,
                p.product_price,
                p.product_source as stock_city,
                p.product_updated_at,
                ps.prod_spec_stock_qty,
                ps.prod_spec_color,
                ps.prod_spec_length_mm,
                ps.prod_spec_thickness_mm,
                ps.prod_spec_width_mm,
                ps.prod_spec_other
            FROM product p
            JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification ps ON p.product_id = ps.product_id AND p.shop_id = ps.shop_id
            WHERE p.product_id = %s
        """
        try:
            cursor = self.database.connection.cursor()
            cursor.execute(query, (product_id,))
            columns = [desc[0] for desc in cursor.description]
            row = cursor.fetchone()
            cursor.close()
            
            return dict(zip(columns, row)) if row else None
        except Exception as e:
            print(f"Database error getting product details: {e}")
            return None