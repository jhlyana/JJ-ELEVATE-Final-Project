from datetime import datetime, timedelta
import logging

class DashboardPageModel:
    def __init__(self, database_instance, user_id, shop_id):
        self.database = database_instance 
        self.user_id = user_id 
        self.shop_id = shop_id 
        logging.debug(f"DashboardPageModel initialized with User ID: {self.user_id}, Shop ID: {self.shop_id}")
        
    def get_today_sales(self):
        """Get total sales amount for today for the current shop."""
        query = """
        SELECT COALESCE(SUM(od.od_total_amt), 0) as total_sales
        FROM order_detail od
        JOIN order_header oh ON od.oh_id = oh.oh_id
        WHERE DATE(oh.oh_created_at) = CURRENT_DATE
        AND oh.shop_id = %s
        """
        result = self.database.fetch_one(query, (self.shop_id,))
        sales = float(result['total_sales']) if result and result['total_sales'] is not None else 0.0
        logging.debug(f"Retrieved today's sales: {sales}")
        return sales

    def get_today_orders(self):
        """Get total number of orders for today for the current shop."""
        query = """
        SELECT COUNT(DISTINCT oh_id) as total_orders
        FROM order_header
        WHERE DATE(oh_created_at) = CURRENT_DATE
        AND shop_id = %s
        """
        result = self.database.fetch_one(query, (self.shop_id,))
        orders = result['total_orders'] if result and result['total_orders'] is not None else 0
        logging.debug(f"Retrieved today's orders: {orders}")
        return orders

    def get_today_revenue(self):
        """Get total revenue for today (same as sales in this implementation)"""
        revenue = self.get_today_sales()
        logging.debug(f"Retrieved today's revenue: {revenue}")
        return revenue

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
        WHERE oh.shop_id = %s
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT {limit}
        """
        best_sellers = self.database.fetch_all(query, (self.shop_id,))
        logging.debug(f"Retrieved best sellers: {best_sellers}")
        return best_sellers