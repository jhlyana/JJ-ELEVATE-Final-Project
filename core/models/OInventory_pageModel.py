from datetime import datetime
# Assuming 'database' module is accessible for connection
from database import Database
from core.models.OStk_Hstry_model import StockHistoryModel

class InventoryModel:
    def __init__(self, database, current_user_shop_id=None, current_user_id=None):
        self.database = database
        self.current_user_shop_id = current_user_shop_id 
        self.current_user_id = current_user_id           
        if not self.database.connection:
            self.database.connect()
        # Initialize StockHistoryModel here, passing the shared database connection
        self.stock_history_model = StockHistoryModel(database)

    def get_all_products(self, shop_id=None):
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
            WHERE p.shop_id = %s
            ORDER BY p.product_name;
        """
        try:
            # Use fetch_all from the Database class directly
            results = self.database.fetch_all(query, (shop_id,))
            
            # Map column names for consistency with controller's expectations
            mapped_results = []
            for row in results:
                mapped_row = {
                    "product_id": row['product_id'],
                    "prod_type_name": row['prod_type_name'],
                    "product_name": row['product_name'],
                    "product_price": row['product_price'],
                    "stock_qty": row['prod_spec_stock_qty'], # Map to 'stock_qty' for controller
                    "color": row['prod_spec_color'],
                    "length_mm": row['prod_spec_length_mm'],
                    "thickness_mm": row['prod_spec_thickness_mm'],
                    "width_mm": row['prod_spec_width_mm'],
                    "other": row['prod_spec_other'],
                    "product_source": row['product_source'],
                    "created_at": row['product_created_at'],
                    "updated_at": row['product_updated_at']
                }
                mapped_results.append(mapped_row)
            return mapped_results
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    def get_products_by_type(self, prod_type_name, shop_id):
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
            WHERE t.prod_type_name = %s AND p.shop_id = %s
            ORDER BY p.product_name;
        """
        try:
            results = self.database.fetch_all(query, (prod_type_name, shop_id))
            mapped_results = []
            for row in results:
                mapped_row = {
                    "product_id": row['product_id'],
                    "prod_type_name": row['prod_type_name'],
                    "product_name": row['product_name'],
                    "product_price": row['product_price'],
                    "stock_qty": row['prod_spec_stock_qty'], # Map to 'stock_qty'
                    "color": row['prod_spec_color'],
                    "length_mm": row['prod_spec_length_mm'],
                    "thickness_mm": row['prod_spec_thickness_mm'],
                    "width_mm": row['prod_spec_width_mm'],
                    "other": row['prod_spec_other'],
                    "product_source": row['product_source'],
                    "created_at": row['product_created_at'],
                    "updated_at": row['product_updated_at']
                }
                mapped_results.append(mapped_row)
            return mapped_results
        except Exception as e:
            print(f"Error getting products by type: {e}")
            return []

    def get_product_type_id(self, prod_type_name):
        query = "SELECT prod_type_id FROM PRODUCT_TYPE WHERE prod_type_name = %s"
        try:
            result = self.database.fetch_one(query, (prod_type_name,))
            return result['prod_type_id'] if result else None
        except Exception as e:
            print(f"Error getting product type ID for {prod_type_name}: {e}")
            return None

    def get_product_by_id(self, product_id):
        query = """
            SELECT
                p.product_id,
                t.prod_type_name,
                p.product_name,
                p.product_price,
                s.prod_spec_id,
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
            WHERE p.product_id = %s
        """
        try:
            result = self.database.fetch_one(query, (product_id,))
            if result:
                # Map the database keys to the more user-friendly keys expected by the controller
                product_dict = {
                    "product_id": result.get('product_id'),
                    "prod_type_name": result.get('prod_type_name'),
                    "product_name": result.get('product_name'),
                    "product_price": result.get('product_price'),
                    "prod_spec_id": result.get('prod_spec_id'),
                    "stock_qty": result.get('prod_spec_stock_qty'), # Renamed for controller usage
                    "color": result.get('prod_spec_color'),
                    "length_mm": result.get('prod_spec_length_mm'),
                    "thickness_mm": result.get('prod_spec_thickness_mm'),
                    "width_mm": result.get('prod_spec_width_mm'),
                    "other": result.get('prod_spec_other'),
                    "product_source": result.get('product_source'),
                    "created_at": result.get('product_created_at'),
                    "updated_at": result.get('product_updated_at')
                }
                # Ensure correct types for numeric values (they might be returned as Decimal from psycopg2)
                product_dict['stock_qty'] = int(product_dict['stock_qty']) if product_dict['stock_qty'] is not None else 0
                product_dict['product_price'] = float(product_dict['product_price']) if product_dict['product_price'] is not None else 0.0
                product_dict['length_mm'] = float(product_dict['length_mm']) if product_dict['length_mm'] is not None else None
                product_dict['thickness_mm'] = float(product_dict['thickness_mm']) if product_dict['thickness_mm'] is not None else None
                product_dict['width_mm'] = float(product_dict['width_mm']) if product_dict['width_mm'] is not None else None
                return product_dict
            return None
        except Exception as e:
            print(f"Error getting product by ID: {e}")
            return None

    def get_product_name_by_id(self, product_id):
        """Fetches the product name from the product table given a product_id."""
        query = "SELECT product_name FROM product WHERE product_id = %s"
        try:
            result = self.database.fetch_one(query, (product_id,))
            return result['product_name'] if result else None
        except Exception as e:
            print(f"Error fetching product name for ID {product_id}: {e}")
            return None

    def validate_price(self, price_str):
        """Helper method to validate and convert price strings"""
        try:
            # Remove peso symbol and commas
            clean_price = str(price_str).strip().replace("₱", "").replace(",", "")
            return float(clean_price)
        except ValueError:
            raise ValueError("Please enter a valid price (e.g. ₱1,250.50).")

    def get_product_source_by_type(self, prod_type_name):
        """
        Retrieves the 'source' information for a given product type.
        As per previous discussion, assuming 'source' is a fixed value.
        """
        # This function name might be misleading if it always returns a fixed string.
        # It seems the intention is to provide a default source.
        return "J&J FACTORY-MOALBOAL"

    def insert_product(self, shop_id, product_type_id, name, price, source):
        # This method assumes the transaction is managed externally if it's part of a larger unit of work.
        # Otherwise, self.database.execute handles commit/rollback for single operations.
        try:
            validated_price = self.validate_price(price)
            if validated_price <= 0:
                raise ValueError("Price must be greater than zero.")

            query = """
                INSERT INTO PRODUCT (
                    product_id, shop_id, product_type_id, product_name,
                    product_price, product_source, product_created_at, product_updated_at
                ) VALUES (
                    CONCAT(LEFT(%s, 1), LPAD(NEXTVAL('product_seq')::text, 3, '0')),
                    %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING product_id
            """
            now = datetime.now()
            prefix = name[0].upper() if name else 'X' # Default prefix if name is empty
            
            # Using cursor directly for RETURNING clause
            cursor = self.database.connection.cursor()
            cursor.execute(query, (
                prefix, shop_id, product_type_id, name, validated_price, source, now, now
            ))
            product_id = cursor.fetchone()[0]
            # No commit here if it's part of a larger transaction in the controller
            # The calling context (controller) should initiate/commit/rollback the transaction.
            cursor.close()
            return product_id
        except Exception as e:
            print(f"Error inserting product: {e}")
            # If this is called within a larger transaction, rollback is handled externally.
            # If called stand-alone, the Database.execute handles it.
            return None

    def insert_specification(self, shop_id, product_id, stock_qty, length=None, thickness=None,
                            width=None, color=None, other=None):
        try:
            query = """
                INSERT INTO PRODUCT_SPECIFICATION (
                    shop_id, product_id, prod_spec_stock_qty,
                    prod_spec_length_mm, prod_spec_thickness_mm, prod_spec_width_mm,
                    prod_spec_color, prod_spec_other,
                    prod_spec_created_at, prod_spec_updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING prod_spec_id
            """
            now = datetime.now()
            # Ensure proper type conversion, especially for potentially empty strings from UI
            stock_qty = int(stock_qty) if stock_qty is not None and str(stock_qty).isdigit() else 0
            length = float(length) if length is not None and str(length).replace('.','').isdigit() else None
            thickness = float(thickness) if thickness is not None and str(thickness).replace('.','').isdigit() else None
            width = float(width) if width is not None and str(width).replace('.','').isdigit() else None
            color = str(color).strip() if color is not None else None
            other = str(other).strip() if other is not None else None
            
            cursor = self.database.connection.cursor()
            cursor.execute(query, (
                shop_id, product_id, stock_qty,
                length, thickness, width,
                color, other,
                now, now
            ))
            
            spec_id = cursor.fetchone()[0]
            # No commit here if it's part of a larger transaction
            cursor.close()
            return spec_id
        except Exception as e:
            print(f"Error inserting specification: {e}")
            return None

    def update_product(self, product_id, name, price, source):
        """Update product information in the database"""
        try:
            validated_price = self.validate_price(price)
            if validated_price <= 0:
                raise ValueError("Price must be greater than zero.")
            query = """
                UPDATE product
                SET product_name = %s,
                    product_price = %s,
                    product_source = %s,
                    product_updated_at = %s
                WHERE product_id = %s
            """
            now = datetime.now()
            # Using cursor directly for precise control within a larger transaction
            cursor = self.database.connection.cursor()
            cursor.execute(query, (name, validated_price, source, now, product_id))
            # No commit here. The transaction should be committed by the controller or higher level.
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def update_specification(self, product_id, stock_qty=None, length=None, thickness=None,
                             width=None, color=None, other=None):
        """Update product specification in the database"""
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
            
            # Convert values to appropriate types, handling None/empty strings
            stock_qty_val = int(stock_qty) if stock_qty is not None and str(stock_qty).isdigit() else 0
            length_val = float(length) if length is not None and str(length).replace('.','').isdigit() else None
            thickness_val = float(thickness) if thickness is not None and str(thickness).replace('.','').isdigit() else None
            width_val = float(width) if width is not None and str(width).replace('.','').isdigit() else None
            color_val = str(color).strip() if color is not None else None
            other_val = str(other).strip() if other is not None else None
            
            cursor = self.database.connection.cursor()
            cursor.execute(query, (
                stock_qty_val,
                length_val,
                thickness_val,
                width_val,
                color_val,
                other_val,
                now,
                product_id
            ))
            # No commit here. The transaction should be committed by the controller or higher level.
            cursor.close()
            return True
        except Exception as e:
            print(f"Error updating specification: {e}")
            return False
    
    def search_products_by_name(self, search_query, shop_id):
        """
        Searches for products by name using a LIKE query (case-insensitive) for a specific shop.
        """
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
            WHERE p.product_name ILIKE %s AND p.shop_id = %s
            ORDER BY p.product_name;
            """
            # Use fetch_all from the Database class directly
            results = self.database.fetch_all(query, ('%' + search_query + '%', shop_id))
            
            # Map column names for consistency with controller's expectations
            mapped_results = []
            for row in results:
                mapped_row = {
                    "product_id": row['product_id'],
                    "prod_type_name": row['prod_type_name'],
                    "product_name": row['product_name'],
                    "product_price": row['product_price'],
                    "stock_qty": row['prod_spec_stock_qty'], # Map to 'stock_qty' for controller
                    "color": row['prod_spec_color'],
                    "length_mm": row['prod_spec_length_mm'],
                    "thickness_mm": row['prod_spec_thickness_mm'],
                    "width_mm": row['prod_spec_width_mm'],
                    "other": row['prod_spec_other'],
                    "product_source": row['product_source'],
                    "created_at": row['product_created_at'],
                    "updated_at": row['product_updated_at']
                }
                mapped_results.append(mapped_row)
            return mapped_results
        except Exception as e:
            print(f"Error searching products by name: {e}")
            return []

    def delete_product_by_id(self, product_id, shop_id, user_id):
        """Proper deletion that maintains history"""
        cursor = None
        try:
            original_autocommit = self.database.connection.autocommit
            self.database.connection.autocommit = False 

            cursor = self.database.connection.cursor()

            # Step 1: Get product_specification details BEFORE deleting
            product_full_data = self.get_product_by_id(product_id)
            if not product_full_data:
                raise ValueError(f"Product {product_id} not found for deletion.")

            old_qty = product_full_data.get('stock_qty', 0)
            product_name = product_full_data.get('product_name', 'Unknown Product')

            # Step 2: Delete from specification only if it exists
            cursor.execute("DELETE FROM product_specification WHERE product_id = %s AND shop_id = %s", (product_id, shop_id))

            # Step 3: Delete from product table
            cursor.execute("DELETE FROM product WHERE product_id = %s AND shop_id = %s", (product_id, shop_id))

            # Step 4: Record stock history
            history_recorded = self.stock_history_model.add_history_entry(
                product_id=product_id,
                old_stock_qty=old_qty,
                new_stock_qty=0,
                action_type='PRODUCT_DELETED',
                user_acc_id=user_id,
                shop_id=shop_id
            )

            if not history_recorded:
                raise Exception("Failed to record stock history during product deletion.")

            self.database.connection.commit()
            return True, f"Product {product_name} (ID: {product_id}) successfully deleted and logged."

        except Exception as e:
            self.database.connection.rollback()
            return False, f"Delete failed for {product_id}: {e}"
        finally:
            if cursor:
                cursor.close()
            self.database.connection.autocommit = original_autocommit

    def delete_product_only(self, product_id):
        """Helper to delete only product entry if specification insertion fails."""
        try:
            original_autocommit = self.database.connection.autocommit
            self.database.connection.autocommit = False # Ensure transactional behavior
            cursor = self.database.connection.cursor()
            cursor.execute("DELETE FROM product WHERE product_id = %s AND shop_id = %s", (product_id, self.current_user_shop_id))
            self.database.connection.commit()
            return True
        except Exception as e:
            self.database.connection.rollback()
            print(f"Error deleting product only for ID {product_id}: {e}")
            return False
        finally:
            self.database.connection.autocommit = original_autocommit # Reset autocommit

    def get_low_stock_products(self, shop_id):
        query = """
            SELECT
                p.product_name,        -- This will be index 0 in the tuple
                ps.prod_spec_stock_qty  -- This will be index 1 in the tuple
            FROM
                product_specification ps
            JOIN
                product p ON ps.product_id = p.product_id AND ps.shop_id = p.shop_id
            WHERE
                ps.prod_spec_stock_qty < 20 AND ps.shop_id = %s;
        """
        try:
            # fetch_all will return a list of dictionaries (e.g., [{'product_name': 'Product A', 'prod_spec_stock_qty': 5}])
            low_stock_items = self.database.fetch_all(query, (shop_id,))
            
            # Map 'prod_spec_stock_qty' to 'stock_qty' if the controller expects it
            mapped_items = []
            for item in low_stock_items:
                mapped_items.append({
                    'product_name': item['product_name'],
                    'stock_qty': item['prod_spec_stock_qty']
                })
            return mapped_items
        except Exception as e:
            print(f"Error fetching low stock items: {e}")
            return []
        
    def _convert_product_data(self, product_data):
        """Convert raw product data to proper types - This function might be redundant if fetch_one/all handle types well"""
        if isinstance(product_data, dict):
            # Convert dict values
            converted = {}
            for key, value in product_data.items():
                if key.endswith('_qty') or key == 'stock_qty':
                    converted[key] = int(value) if value is not None else 0
                elif key.endswith(('_mm', '_price')):
                    converted[key] = float(value) if value is not None else None
                elif key == 'color':
                    converted[key] = str(value) if value is not None else ""
                else:
                    converted[key] = value
            return converted
        return product_data