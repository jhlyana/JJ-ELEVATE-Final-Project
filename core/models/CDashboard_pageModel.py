from datetime import datetime, timedelta
from database import Database

class DashboardPageModel:
    def __init__(self, database_class):
        self.database = database_class

    def get_today_sales(self):
        """Get total sales amount for today"""
        query = """
        SELECT COALESCE(SUM(od.od_total_amt), 0) as total_sales
        FROM order_detail od
        JOIN order_header oh ON od.oh_id = oh.oh_id
        WHERE DATE(oh.oh_created_at) = CURRENT_DATE
        """
        result = self.database.fetch_one(query)
        return float(result['total_sales']) if result else 0.0

    def get_today_orders(self):
        """Get total number of orders for today"""
        query = """
        SELECT COUNT(DISTINCT oh_id) as total_orders
        FROM order_header
        WHERE DATE(oh_created_at) = CURRENT_DATE
        """
        result = self.database.fetch_one(query)
        return result['total_orders'] if result else 0

    def get_today_revenue(self):
        """Get total revenue for today (same as sales in this implementation)"""
        return self.get_today_sales()

    def get_best_sellers(self, limit=5):
        """Get top selling products of all time"""
        query = f"""
        SELECT 
            p.product_name,
            SUM(od.od_quantity) as total_quantity,
            SUM(od.od_total_amt) as total_sales
        FROM order_detail od
        JOIN product p ON od.product_id = p.product_id
        JOIN order_header oh ON od.oh_id = oh.oh_id
        GROUP BY p.product_name
        ORDER BY total_quantity DESC
        LIMIT {limit}
        """
        return self.database.fetch_all(query)