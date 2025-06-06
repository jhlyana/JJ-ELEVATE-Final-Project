from database import Database
import psycopg2.extras

database = Database()
database.connect()

class InventoryModel:
    """Model class for inventory database operations"""

    @staticmethod # CHANGED JUST NOW
    def get_all_products():
        """Retrieve all products with their specifications and type names"""
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
                p.product_created_at,
                p.product_updated_at
            FROM product p
            LEFT JOIN product_type t ON p.product_type_id = t.prod_type_id
            LEFT JOIN product_specification s ON p.product_id = s.product_id
            ORDER BY p.product_name;
        """
        return Database.fetch_all(query)
    
    @staticmethod
    def get_products_by_type(category):
        """Retrieve products filtered by category/type name"""
        query = """
            SELECT p.product_id, p.product_name, p.product_price, p.prod_spec_stock_qty,
                   p.prod_spec_color, p.prod_spec_other,
                   d.prod_dimension_length_mm, d.prod_dimension_width_mm, d.prod_dimension_thickness_mm,
                   t.prod_type_name
            FROM products p
            LEFT JOIN product_dimensions d ON p.product_id = d.product_id
            LEFT JOIN product_types t ON p.prod_type_id = t.prod_type_id
            WHERE t.prod_type_name = :category
            ORDER BY p.product_name;
        """
        values = {"category": category}
        return Database.fetch_all(query, values=values)

    @staticmethod
    def search_products(search_text):
        """Search products by name or description matching search_text"""
        query = """
            SELECT p.product_id, p.product_name, p.product_price, p.prod_spec_stock_qty,
                   p.prod_spec_color, p.prod_spec_other,
                   d.prod_dimension_length_mm, d.prod_dimension_width_mm, d.prod_dimension_thickness_mm,
                   t.prod_type_name
            FROM products p
            LEFT JOIN product_dimensions d ON p.product_id = d.product_id
            LEFT JOIN product_types t ON p.prod_type_id = t.prod_type_id
            WHERE p.product_name ILIKE :search OR p.prod_spec_other ILIKE :search
            ORDER BY p.product_name;
        """
        values = {"search": f"%{search_text}%"}
        return Database.fetch_all(query, values=values)

    @staticmethod
    def add_product(shop_id, category, name, price, stock_qty, color,
                    length, width, thickness, description):
        """
        Add a new product to the database.
        Returns the new product_id or None if failed.
        """
        try:
            # Insert product
            insert_product = """
                INSERT INTO products (product_name, product_price, prod_spec_stock_qty,
                    prod_spec_color, prod_spec_other, prod_type_id)
                VALUES (:name, :price, :stock_qty, :color, :description,
                    (SELECT prod_type_id FROM product_types WHERE prod_type_name = :category))
                RETURNING product_id;
            """
            values = {
                "name": name,
                "price": price,
                "stock_qty": stock_qty,
                "color": color,
                "description": description,
                "category": category,
            }
            product_id_row = Database.fetch_one(insert_product, values=values)
            if not product_id_row:
                return None
            product_id = product_id_row["product_id"]

            # Insert product dimensions
            insert_dimensions = """
                INSERT INTO product_dimensions (product_id, prod_dimension_length_mm,
                    prod_dimension_width_mm, prod_dimension_thickness_mm)
                VALUES (:product_id, :length, :width, :thickness);
            """
            dim_values = {
                "product_id": product_id,
                "length": length,
                "width": width,
                "thickness": thickness,
            }
            Database.execute(insert_dimensions, values=dim_values)

            return product_id

        except Exception as e:
            print(f"Error adding product: {e}")
            return None

    @staticmethod
    def update_product(product_id, name=None, price=None, stock_qty=None, color=None,
                       length=None, width=None, thickness=None, description=None):
        """
        Update product information. Only updates fields provided (not None).
        Returns True if successful, False otherwise.
        """
        try:
            # Update products table fields if provided
            update_parts = []
            values = {"product_id": product_id}

            if name is not None:
                update_parts.append("product_name = :name")
                values["name"] = name
            if price is not None:
                update_parts.append("product_price = :price")
                values["price"] = price
            if stock_qty is not None:
                update_parts.append("prod_spec_stock_qty = :stock_qty")
                values["stock_qty"] = stock_qty
            if color is not None:
                update_parts.append("prod_spec_color = :color")
                values["color"] = color
            if description is not None:
                update_parts.append("prod_spec_other = :description")
                values["description"] = description

            if update_parts:
                update_query = f"""
                    UPDATE products SET {', '.join(update_parts)} WHERE product_id = :product_id;
                """
                Database.execute(update_query, values=values)

            # Update product_dimensions table if needed
            dim_update_parts = []
            dim_values = {"product_id": product_id}

            if length is not None:
                dim_update_parts.append("prod_dimension_length_mm = :length")
                dim_values["length"] = length
            if width is not None:
                dim_update_parts.append("prod_dimension_width_mm = :width")
                dim_values["width"] = width
            if thickness is not None:
                dim_update_parts.append("prod_dimension_thickness_mm = :thickness")
                dim_values["thickness"] = thickness

            if dim_update_parts:
                dim_update_query = f"""
                    UPDATE product_dimensions SET {', '.join(dim_update_parts)} WHERE product_id = :product_id;
                """
                Database.execute(dim_update_query, values=dim_values)

            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    @staticmethod
    def delete_product(product_id):
        """
        Delete product and related dimensions from database.
        Returns True if successful, False otherwise.
        """
        try:
            delete_dimensions = "DELETE FROM product_dimensions WHERE product_id = :product_id;"
            Database.execute(delete_dimensions, values={"product_id": product_id})

            delete_product = "DELETE FROM products WHERE product_id = :product_id;"
            Database.execute(delete_product, values={"product_id": product_id})

            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    @staticmethod
    def get_low_stock_products(threshold=10):
        """
        Get products with stock quantity less than or equal to threshold.
        Returns list of low stock products.
        """
        query = """
            SELECT p.product_id, p.product_name, p.product_price, p.prod_spec_stock_qty,
                   p.prod_spec_color, p.prod_spec_other,
                   d.prod_dimension_length_mm, d.prod_dimension_width_mm, d.prod_dimension_thickness_mm,
                   t.prod_type_name
            FROM products p
            LEFT JOIN product_dimensions d ON p.product_id = d.product_id
            LEFT JOIN product_types t ON p.prod_type_id = t.prod_type_id
            WHERE p.prod_spec_stock_qty <= :threshold
            ORDER BY p.prod_spec_stock_qty ASC;
        """
        values = {"threshold": threshold}
        return Database.fetch_all(query, values=values)