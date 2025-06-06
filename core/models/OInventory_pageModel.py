from datetime import datetime

class InventoryModel:
    def __init__(self, database):
        self.database = database
        if not self.database.connection:
            self.database.connect()

    def get_all_products(self):
        query = """
            SELECT 
                p.product_id, 
                t.prod_type_name,
                p.product_name, 
                p.product_price,
                s.prod_spec_stock_qty,
                s.prod_spec_color,
                s.prod_spec_length_mm,
                s.prod_spec_thickness_mm,
                s.prod_spec_width_mm,
                s.prod_spec_other,
                p.product_source,
                p.product_created_at,
                p.product_updated_at
            FROM product p
            LEFT JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification s ON p.product_id = s.product_id
            ORDER BY p.product_name;
        """
        try:
            cursor = self.database.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    def get_products_by_type(self, prod_type_name):
        query = """
            SELECT 
                p.product_id, 
                t.prod_type_name,
                p.product_name, 
                p.product_price,
                s.prod_spec_stock_qty,
                s.prod_spec_color,
                s.prod_spec_length_mm,
                s.prod_spec_thickness_mm,
                s.prod_spec_width_mm,
                s.prod_spec_other,
                p.product_source,
                p.product_created_at,
                p.product_updated_at
            FROM product p
            LEFT JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification s ON p.product_id = s.product_id
            WHERE t.prod_type_name = %s
            ORDER BY p.product_name;
        """
        try:
            cursor = self.database.connection.cursor()
            cursor.execute(query, (prod_type_name,))
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(f"Error getting products by type: {e}")
            return []
    
    def get_product_type_id(self, prod_type_name):
        query = "SELECT prod_type_id FROM product_type WHERE prod_type_name = %s"
        cursor = self.database.connection.cursor()
        cursor.execute(query, (prod_type_name,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None
    
    def get_product_by_id(self, product_id):
        query = """
            SELECT 
                p.product_id, 
                t.prod_type_name,
                p.product_name, 
                p.product_price,
                s.prod_spec_stock_qty,
                s.prod_spec_color,
                s.prod_spec_length_mm,
                s.prod_spec_thickness_mm,
                s.prod_spec_width_mm,
                s.prod_spec_other,
                p.product_source
            FROM product p
            LEFT JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification s ON p.product_id = s.product_id
            WHERE p.product_id = %s
        """
        try:
            cursor = self.database.connection.cursor()
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                columns = [
                    "product_id", "prod_type_name", "product_name", "product_price",
                    "stock_qty", "color", "length_mm", "thickness_mm", "width_mm", "other",
                    "source"
                ]
                return dict(zip(columns, result))
            return None
        except Exception as e:
            print(f"Error getting product by ID: {e}")
            return None

    def validate_price(self, price_str):
        try:
            clean_price = price_str.strip().replace("₱", "").replace(",", "")
            return float(clean_price)
        except ValueError:
            raise ValueError("Please enter a valid price (e.g. ₱1,250.50)")

    def insert_product(self, shop_id, product_type_id, name, price, source):
        try:
            validated_price = self.validate_price(price) if isinstance(price, str) else price
            if validated_price <= 0:
                raise ValueError("Price must be greater than zero")
            
            query = """
                INSERT INTO product (
                    product_id, shop_id, product_type_id, product_name, 
                    product_price, product_source, product_created_at, product_updated_at
                ) VALUES (
                    CONCAT(LEFT(%s, 1), LPAD(NEXTVAL('product_seq')::text, 3, '0')),
                    %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING product_id
            """
            now = datetime.now()
            prefix = name[0].upper()
            cursor = self.database.connection.cursor()
            cursor.execute(query, (
                prefix, shop_id, product_type_id, name, price, source, now, now
            ))
            product_id = cursor.fetchone()[0]
            self.database.connection.commit()
            cursor.close()
            return product_id
        except Exception as e:
            self.database.connection.rollback()
            print(f"Error inserting product: {e}")
            return None
    
    def get_product_source_by_type(self, prod_type_name):
        return "J&J FACTORY-MOALBOAL"

    def insert_specification(self, shop_id, product_id, stock_qty, length, thickness, width, color, other):
        try:
            query = """
                INSERT INTO product_specification (
                    shop_id, product_id, prod_spec_stock_qty, prod_spec_length_mm, 
                    prod_spec_thickness_mm, prod_spec_width_mm, prod_spec_color, 
                    prod_spec_other, prod_spec_created_at, prod_spec_updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            now = datetime.now()
            cursor = self.database.connection.cursor()
            cursor.execute(query, (
                shop_id,
                product_id,
                stock_qty,
                float(length) if length else None,
                float(thickness) if thickness else None,
                float(width) if width else None,
                color.strip() if color else None,
                other.strip() if other else None,
                now,
                now
            ))
            self.database.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error inserting specification: {e}")
            self.database.connection.rollback()
            return False

    def update_product(self, product_id, name, price, source):
        try:
            validated_price = self.validate_price(price) if isinstance(price, str) else price
            if validated_price <= 0:
                raise ValueError("Price must be greater than zero")
            query = """
                UPDATE product 
                SET product_name = %s,
                    product_price = %s,
                    product_source = %s,
                    product_updated_at = %s
                WHERE product_id = %s
            """
            now = datetime.now()
            cursor = self.database.connection.cursor()
            cursor.execute(query, (name, price, source, now, product_id))
            self.database.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            self.database.connection.rollback()
            return False

    def update_specification(self, product_id, stock_qty, length=None, thickness=None, 
                            width=None, color=None, other=None):
        try:
            query = """
                UPDATE product_specification
                SET prod_spec_stock_qty = %s,
                    prod_spec_length_mm = %s,
                    prod_spec_thickness_mm = %s,
                    prod_spec_width_mm = %s,
                    prod_spec_color = %s,
                    prod_spec_other = %s,
                    prod_spec_updated_at = %s
                WHERE product_id = %s
            """
            now = datetime.now()
            cursor = self.database.connection.cursor()
            cursor.execute(query, (
                stock_qty,
                float(length) if length else None,
                float(thickness) if thickness else None,
                float(width) if width else None,
                color.strip() if color else None,
                other.strip() if other else None,
                now,
                product_id
            ))
            self.database.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating specification: {e}")
            self.database.connection.rollback()
            return False
    
    def search_products_by_name(self, search_query):
        try:
            query = """
            SELECT
                p.product_id,
                t.prod_type_name,
                p.product_name,
                p.product_price,
                s.prod_spec_stock_qty,
                s.prod_spec_color,
                s.prod_spec_length_mm,
                s.prod_spec_thickness_mm,
                s.prod_spec_width_mm,
                s.prod_spec_other,
                p.product_source,
                p.product_created_at,
                p.product_updated_at
            FROM product p
            LEFT JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification s ON p.product_id = s.product_id
            WHERE p.product_name ILIKE %s
            ORDER BY p.product_name;
            """
            cursor = self.database.connection.cursor()
            cursor.execute(query, ('%' + search_query + '%',))
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(f"Error searching products by name: {e}")
            return []

    def delete_product_by_id(self, product_id):
        try:
            cursor = self.database.connection.cursor()
            cursor.execute("BEGIN;")
            query_spec = "DELETE FROM product_specification WHERE product_id = %s;"
            cursor.execute(query_spec, (product_id,))
            query_product = "DELETE FROM product WHERE product_id = %s;"
            cursor.execute(query_product, (product_id,))
            cursor.execute("COMMIT;")
            return True
        except Exception as e:
            if cursor:
                cursor.execute("ROLLBACK;")
            print(f"Error deleting product with ID {product_id}: {e}")
            return False
        finally:
            if cursor:
                cursor.close()