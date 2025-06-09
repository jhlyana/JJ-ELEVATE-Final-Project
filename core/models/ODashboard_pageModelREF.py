# from models.database import Database
# import logging

# class DashboardModel:
#     LOW_STOCK_THRESHOLD = 20

#     def __init__(self, database: Database):
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(logging.DEBUG)
#         self.database = database
#         self.db = database

#         if not self.db.connection:
#             self.logger.debug("No active database connection, attempting to connect")
#             try:
#                 self.db.connect()
#             except Exception as e:
#                 self.logger.error(f"Failed to connect to database: {e}")
#                 raise

#     def get_low_stock_products(self, shop_id: int, limit: int = 4):
#         if not isinstance(shop_id, int) or shop_id <= 0:
#             raise ValueError("shop_id must be a positive integer")
#         if not isinstance(limit, int) or limit <= 0:
#             raise ValueError("limit must be a positive integer")
#         query = """
#         SELECT
#             p.product_name,
#             ps.prod_spec_stock_qty
#         FROM
#             product_specification ps
#         JOIN
#             product p ON ps.product_id = p.product_id AND ps.shop_id = p.shop_id
#         WHERE
#             ps.shop_id = %s AND ps.prod_spec_stock_qty < %s
#         ORDER BY
#             ps.prod_spec_stock_qty ASC
#         LIMIT %s;
#         """
#         return self._execute_query(query, (shop_id, self.LOW_STOCK_THRESHOLD, limit), "low stock products")

#     def get_low_stock_count(self, shop_id: int) -> int:
#         if not isinstance(shop_id, int) or shop_id <= 0:
#             raise ValueError("shop_id must be a positive integer")
#         query = """
#         SELECT COUNT(*)
#         FROM product_specification ps
#         JOIN product p ON ps.product_id = p.product_id AND ps.shop_id = p.shop_id
#         WHERE ps.shop_id = %s AND ps.prod_spec_stock_qty < %s;
#         """
#         return self._execute_single_value_query(query, "total low stock count", (shop_id, self.LOW_STOCK_THRESHOLD))

#     def _execute_single_value_query(self, query: str, description: str, params: tuple = None):
#         self.logger.debug(f"Fetching {description} with params: {params}")
#         try:
#             raw_result = self.db.fetch_one(query, params) if params else self.db.fetch_one(query)
#             value = 0
#             if raw_result is not None:
#                 if isinstance(raw_result, (tuple, list)):
#                     if raw_result and raw_result[0] is not None:
#                         value = int(raw_result[0])
#                 elif isinstance(raw_result, dict):
#                     if 'count' in raw_result and raw_result['count'] is not None:
#                         value = int(raw_result['count'])
#                     else:
#                         self.logger.warning(f"Dictionary result for {description} did not contain a 'count' key or its value was None: {raw_result}. Defaulting to 0.")
#                 else:
#                     try:
#                         value = int(raw_result)
#                     except (ValueError, TypeError):
#                         self.logger.warning(f"Could not convert raw_result '{raw_result}' to int for {description}. Defaulting to 0.")
#                         value = 0
#             self.logger.debug(f"Fetched {description}: {value}")
#             return value
#         except Exception as e:
#             self.logger.error(f"Error fetching {description}: {e}", exc_info=True)
#             return 0

#     def _execute_query(self, query: str, params: tuple, description: str):
#         self.logger.debug(f"Fetching {description} with params: {params}")
#         try:
#             return self.db.fetch_all(query, params) or []
#         except Exception as e:
#             self.logger.error(f"Error fetching {description}: {e}")
#             return []