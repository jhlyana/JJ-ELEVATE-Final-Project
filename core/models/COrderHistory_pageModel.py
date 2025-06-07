from datetime import datetime

class OrderHistory:
    def __init__(self, db):
        self.db = db

    def get_all_orders(self, product_type=None, search_term=None):
        print(f"Model getting orders - Product Type: {product_type}, Search Term: {search_term}")  # Debug print
        
        query = """
        SELECT 
            oh.oh_id AS order_id,
            p.product_name AS product,
            od.od_product_price AS price,
            od.od_quantity AS quantity,
            (od.od_product_price * od.od_quantity) AS subtotal,
            od.od_total_amt AS total_amount,
            pt.prod_type_name AS product_type
        FROM order_header oh
        JOIN order_detail od ON oh.oh_id = od.oh_id
        JOIN product p ON od.product_id = p.product_id AND od.shop_id = p.shop_id
        JOIN product_type pt ON p.product_type_id = pt.prod_type_id
        """
        
        conditions = []
        params = []
        
        # Handle product type filtering
        if product_type and product_type != "All Products":
            conditions.append("pt.prod_type_name = %s")
            params.append(product_type)
            print(f"Adding product type filter: {product_type}")  # Debug print
        
        # Handle search term
        if search_term:
            search_conditions = []
            search_params = []
            search_fields = [
                "CAST(oh.oh_id AS TEXT)",
                "p.product_name",
                "CAST(od.od_product_price AS TEXT)",
                "CAST(od.od_quantity AS TEXT)",
                "CAST((od.od_product_price * od.od_quantity) AS TEXT)",
                "CAST(od.od_total_amt AS TEXT)"
            ]
            
            for field in search_fields:
                search_conditions.append(f"{field} ILIKE %s")
                search_params.append(f"%{search_term}%")
            
            conditions.append(f"({' OR '.join(search_conditions)})")
            params.extend(search_params)
            print(f"Adding search term: {search_term}")  # Debug print
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY oh.oh_created_at DESC"
        
        print("Final query:", query)  # Debug print
        print("Query params:", params)  # Debug print
        
        results = self.db.fetch_all(query, params)
        print(f"Found {len(results)} records")  # Debug print
        return results