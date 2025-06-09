from datetime import datetime
from database import Database 

class StockHistoryModel:
    def __init__(self, database):
        self.database = database
        # self.database.connect() is handled by the MainController and passed down
        # So, no need to connect here again.
        if not self.database.connection:
            print("WARNING: Database connection not active in StockHistoryModel init. Attempting to connect.")
            self.database.connect() # Fallback, though ideally already connected

    def add_history_entry(self, product_id, old_stock_qty, new_stock_qty, action_type, user_acc_id, shop_id, product_spec_id=None):
        """
        Records a stock action in the stock_history table.
        This method does NOT commit the transaction; it expects the calling method (e.g., in InventoryModel)
        to handle the commit/rollback for the overall transaction.
        """
        # Fetch product name if not provided (especially for DELETE actions)
        product_name = None
        if product_id:
            try:
                # Use current cursor for this fetch, if available in a transaction
                # Otherwise, use the database's fetch_one
                with self.database.connection.cursor() as cursor:
                    cursor.execute("SELECT product_name FROM product WHERE product_id = %s", (product_id,))
                    result = cursor.fetchone()
                    if result:
                        product_name = result[0]
            except Exception as e:
                print(f"Warning: Could not fetch product name for history entry (product_id: {product_id}): {e}")
                product_name = "Unknown Product" # Fallback if name cannot be fetched

        # Ensure product_spec_id is retrieved if not provided and product_id is available
        if product_spec_id is None and product_id:
            try:
                with self.database.connection.cursor() as cursor:
                    cursor.execute("SELECT prod_spec_id FROM product_specification WHERE product_id = %s", (product_id,))
                    result = cursor.fetchone()
                    if result:
                        product_spec_id = result[0]
            except Exception as e:
                print(f"Warning: Could not fetch product_spec_id for history entry (product_id: {product_id}): {e}")
                # It's crucial to have a prod_spec_id if the table requires it.
                # If it's optional, then None is fine. Check your schema for `stock_history`.
                # Based on your \d+ stock_history, prod_spec_id is NOT NULL.
                # So if it's None, this insert will fail. This means for 'PRODUCT_DELETED', 
                # you need to pass it from the product_full_data.
                pass # Let the database insert fail if prod_spec_id is truly missing and required

        query = """
            INSERT INTO stock_history (
                product_id, 
                shop_id, 
                user_acc_id, 
                product_spec_id, -- Added product_spec_id based on table schema
                stk_hstry_old_stock_qty, 
                stk_hstry_new_stock_qty, 
                stk_hstry_action, -- Changed from stk_hstry_action_type based on your schema
                product_name,    -- Added product_name based on table schema
                stk_hstry_updated_at -- Renamed from stk_hstry_created_at to match schema
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        now = datetime.now()
        try:
            with self.database.connection.cursor() as cursor:
                cursor.execute(query, (
                    product_id,
                    shop_id, 
                    user_acc_id, 
                    product_spec_id, # Value for product_spec_id
                    old_stock_qty,
                    new_stock_qty,
                    action_type,
                    product_name, # Value for product_name
                    now # Value for stk_hstry_updated_at
                ))
            # IMPORTANT: Do NOT commit here. The calling function (e.g., delete_product_by_id)
            # is responsible for committing or rolling back the entire transaction.
            return True
        except Exception as e:
            print(f"Error recording stock history for product {product_id} (Spec ID: {product_spec_id}): {e}")
            return False

    def get_stock_history(self, product_type: str = None, shop_id: int = None, search_query: str = None,
                          start_date: datetime = None, end_date: datetime = None, limit: int = 500) -> list:
        """
        Get stock history with optional product type, shop_id, search query, and date range filtering.
        """
        base_query = """
            SELECT
                sh.stk_hstry_id,
                sh.user_acc_id AS user_id,
                u.user_acc_username,
                sh.stk_hstry_action AS action_type,
                sh.product_name,
                sh.stk_hstry_old_stock_qty AS old_quantity,
                sh.stk_hstry_new_stock_qty AS new_quantity,
                sh.stk_hstry_updated_at AS timestamp
            FROM
                stock_history sh
            LEFT JOIN
                user_account u ON sh.user_acc_id = u.user_acc_id
            LEFT JOIN
                product p ON sh.product_id = p.product_id
            LEFT JOIN
                product_type pt ON p.product_type_id = pt.prod_type_id
            {where_clause}
            ORDER BY
                sh.stk_hstry_updated_at DESC
            LIMIT %s;
        """
        where_conditions = []
        params = []

        if product_type:
            where_conditions.append("pt.prod_type_name = %s")
            params.append(product_type)
        if shop_id is not None:
            where_conditions.append("sh.shop_id = %s")
            params.append(shop_id)
        if search_query:
            where_conditions.append("(sh.product_name ILIKE %s OR u.user_acc_username ILIKE %s OR sh.stk_hstry_action ILIKE %s)")
            params.extend([f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'])
        if start_date:
            where_conditions.append("sh.stk_hstry_updated_at >= %s")
            params.append(start_date)
        if end_date:
            where_conditions.append("sh.stk_hstry_updated_at <= %s")
            params.append(end_date + datetime.timedelta(days=1)) # Include end of day

        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        params.append(limit)
        query = base_query.format(where_clause=where_clause)

        print(f"DEBUG: FINAL SQL QUERY BEING EXECUTED:\n{query}")
        print(f"DEBUG: FINAL QUERY PARAMETERS: {params}")
        print(f"DEBUG: Number of parameters: {len(params)}")

        try:
            # Use self.database.fetch_all since it uses DictCursor and handles connection
            results = self.database.fetch_all(query, params)
            return results
        except Exception as e:
            print(f"Error fetching stock history: {e}")
            return []
            
    def get_filtered_stock_history(self, shop_id: int, action_type: str = None, product_id: str = None,
                                   start_date: datetime = None, end_date: datetime = None, limit: int = 500) -> list:
        """
        Retrieves filtered stock history entries.
        """
        base_query = """
            SELECT
                sh.stk_hstry_id,
                sh.user_acc_id AS user_id,
                u.user_acc_username,
                sh.stk_hstry_action AS action_type,
                sh.product_name,
                sh.stk_hstry_old_stock_qty AS old_quantity,
                sh.stk_hstry_new_stock_qty AS new_quantity,
                sh.stk_hstry_updated_at AS timestamp
            FROM
                stock_history sh
            LEFT JOIN
                user_account u ON sh.user_acc_id = u.user_acc_id
            LEFT JOIN
                product p ON sh.product_id = p.product_id
            {where_clause}
            ORDER BY
                sh.stk_hstry_updated_at DESC
            LIMIT %s;
        """
        where_conditions = []
        params = []

        where_conditions.append("sh.shop_id = %s")
        params.append(shop_id)

        if action_type and action_type.lower() != 'all changes':
            where_conditions.append("sh.stk_hstry_action = %s")
            params.append(action_type.upper()) # Ensure action type is uppercase for DB consistency
        
        if product_id:
            where_conditions.append("sh.product_id = %s")
            params.append(product_id)

        if start_date:
            where_conditions.append("sh.stk_hstry_updated_at >= %s")
            params.append(start_date)
        
        if end_date:
            # Add one day to end_date to include the full day
            end_date_inclusive = end_date + datetime.timedelta(days=1)
            where_conditions.append("sh.stk_hstry_updated_at < %s")
            params.append(end_date_inclusive)

        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        params.append(limit) # Limit is always the last parameter

        query = base_query.format(where_clause=where_clause)

        try:
            results = self.database.fetch_all(query, params)
            return results
        except Exception as e:
            print(f"Error fetching filtered stock history: {e}")
            return []

    def get_stock_history_by_id(self, history_id: int):
        """Fetches a single stock history record by its ID."""
        query = """
            SELECT
                sh.stk_hstry_id,
                sh.user_acc_id AS user_id,
                u.user_acc_username,
                sh.stk_hstry_action AS action_type,
                sh.product_name,
                sh.stk_hstry_old_stock_qty AS old_quantity,
                sh.stk_hstry_new_stock_qty AS new_quantity,
                sh.stk_hstry_updated_at AS timestamp,
                ps.prod_spec_id, -- Include prod_spec_id
                sh.product_id    -- Ensure product_id is selected
            FROM
                stock_history sh
            LEFT JOIN
                user_account u ON sh.user_acc_id = u.user_acc_id
            LEFT JOIN
                product p ON sh.product_id = p.product_id
            LEFT JOIN
                product_specification ps ON p.product_id = ps.product_id
            WHERE
                sh.stk_hstry_id = %s
        """
        try:
            result = self.database.fetch_one(query, (history_id,))
            return result
        except Exception as e:
            print(f"Error fetching stock history by ID {history_id}: {e}")
            return None

    def delete_history_entry(self, history_id: int) -> bool:
        """Delete a stock history entry by its ID."""
        try:
            # Using the instance's execute method, which handles commit/rollback
            return self.database.execute("DELETE FROM stock_history WHERE stk_hstry_id = %s", (history_id,))
        except Exception as e:
            print(f"Failed to delete stock history entry with ID {history_id}: {e}")
            return False
    
    def delete_all_history_entries(self, shop_id=None):
        """Delete all records from the stock_history table, optionally for a specific shop.
        
        Args:
            shop_id: Optional shop_id to limit deletion to a specific shop.
            
        Returns:
            bool: True if deletion succeeded, False otherwise.
        """
        try:
            query = "DELETE FROM stock_history"
            params = None
            
            if shop_id is not None:
                query += " WHERE shop_id = %s"
                params = (shop_id,)
                
            # Using the instance's execute method, which handles commit/rollback
            return self.database.execute(query, params)
        except Exception as e:
            print(f"Failed to delete all history entries: {e}")
            return False

    def get_stock_movement_summary(self, shop_id):
        """
        Retrieves a summary of stock movements (total in, total out, net change) for each product.
        """
        query = """
            SELECT
                p.product_name,
                COALESCE(SUM(CASE WHEN sh.stk_hstry_action = 'ADD' THEN sh.stk_hstry_new_stock_qty - sh.stk_hstry_old_stock_qty ELSE 0 END), 0) AS total_in,
                COALESCE(SUM(CASE WHEN sh.stk_hstry_action = 'SALE' OR sh.stk_hstry_action = 'PRODUCT_DELETED' THEN sh.stk_hstry_old_stock_qty - sh.stk_hstry_new_stock_qty ELSE 0 END), 0) AS total_out,
                COALESCE(SUM(sh.stk_hstry_new_stock_qty - sh.stk_hstry_old_stock_qty), 0) AS net_change,
                ps.prod_spec_stock_qty AS current_stock -- Fetch current stock from product_specification
            FROM
                stock_history sh
            JOIN
                product p ON sh.product_id = p.product_id
            JOIN
                product_specification ps ON p.product_id = ps.product_id AND sh.shop_id = ps.shop_id
            WHERE
                sh.shop_id = %s
            GROUP BY
                p.product_id, p.product_name, ps.prod_spec_stock_qty
            ORDER BY
                p.product_name;
        """
        try:
            return self.database.fetch_all(query, (shop_id,))
        except Exception as e:
            print(f"Error getting stock movement summary: {e}")
            return []

    def get_all_products_for_filter(self, shop_id):
        """
        Gets a list of all products (product_id, product_name) for populating filters.
        """
        query = "SELECT product_id, product_name FROM product WHERE shop_id = %s ORDER BY product_name"
        try:
            return self.database.fetch_all(query, (shop_id,))
        except Exception as e:
            print(f"Error fetching all products for filter: {e}")
            return []

    def get_low_stock_products(self, shop_id):
        """
        Retrieves products with stock quantity below a certain threshold (e.g., 20).
        """
        query = """
            SELECT
                p.product_name,
                ps.prod_spec_stock_qty AS stock_qty -- Alias for consistency
            FROM
                product_specification ps
            JOIN
                product p ON ps.product_id = p.product_id AND ps.shop_id = p.shop_id
            WHERE
                ps.prod_spec_stock_qty < 20 AND ps.shop_id = %s
            ORDER BY
                p.product_name;
        """
        try:
            return self.database.fetch_all(query, (shop_id,))
        except Exception as e:
            print(f"Error fetching low stock products: {e}")
            return []