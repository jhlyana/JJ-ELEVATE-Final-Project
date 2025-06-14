from datetime import datetime, timedelta
# from database import Database # We will receive an instance, so no need to import the class directly here

class DashboardPageModel:
    # FIX: Accept database_instance, user_id, and shop_id
    def __init__(self, database_instance, user_id, shop_id):
        self.database = database_instance # Store the provided database instance
        self.user_id = user_id # Store user ID for potential future use in queries
        self.shop_id = shop_id # Store shop ID for potential future use in queries
        
    def get_today_sales(self):
        """Get total sales amount for today for the current shop."""
        query = """
        SELECT COALESCE(SUM(od.od_total_amt), 0) as total_sales
        FROM order_detail od
        JOIN order_header oh ON od.oh_id = oh.oh_id
        WHERE DATE(oh.oh_created_at) = CURRENT_DATE
        AND oh.shop_id = %s -- Add shop_id to filter sales by the current shop
        """
        # Pass the query and its parameters (shop_id) to fetch_one
        result = self.database.fetch_one(query, (self.shop_id,))
        return float(result['total_sales']) if result and result['total_sales'] is not None else 0.0

    def get_today_orders(self):
        """Get total number of orders for today for the current shop."""
        query = """
        SELECT COUNT(DISTINCT oh_id) as total_orders
        FROM order_header
        WHERE DATE(oh_created_at) = CURRENT_DATE
        AND shop_id = %s -- Add shop_id to filter orders by the current shop
        """
        # Pass the query and its parameters (shop_id) to fetch_one
        result = self.database.fetch_one(query, (self.shop_id,))
        return result['total_orders'] if result and result['total_orders'] is not None else 0

    def get_today_revenue(self):
        """Get total revenue for today (same as sales in this implementation)"""
        return self.get_today_sales()

    def get_best_sellers(self, limit=5):
        """Get top selling products of all time for the current shop."""
        query = f"""
        SELECT 
            p.product_name,
            SUM(od.od_quantity) as total_quantity,
            SUM(od.od_total_amt) as total_sales
        FROM order_detail od
        JOIN product p ON od.product_id = p.product_id
        JOIN order_header oh ON od.oh_id = oh.oh_id
        WHERE oh.shop_id = %s -- Add shop_id to filter best sellers by the current shop
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT {limit}
        """
        # Pass the query and its parameters (shop_id) to fetch_all
        return self.database.fetch_all(query, (self.shop_id,))