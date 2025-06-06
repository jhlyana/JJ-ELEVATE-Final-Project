from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings
from database import Database
from controllers.OInv_pageController import InventoryPageController
from core.models.inventory_model import InventoryModel
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class InventoryController:
    """Controller for inventory operations"""

    def __init__(self):
        """Initialize the inventory controller"""
        self.shop_id = 1  # Default shop ID

    def load_all_inventory_products(self):
        try:
            products = InventoryModel.get_all_products()

            self.tableWidget.setRowCount(0)  # Clear table first

            for row_num, product in enumerate(products):
                self.tableWidget.insertRow(row_num)
                
                # Set items in the correct column order
                self.tableWidget.setItem(row_num, 0, QTableWidgetItem(str(product["product_id"])))
                self.tableWidget.setItem(row_num, 1, QTableWidgetItem(str(product["prod_type_name"])))
                self.tableWidget.setItem(row_num, 2, QTableWidgetItem(str(product["product_name"])))
                
                # Format price with peso sign
                price_item = QTableWidgetItem(f"₱{float(product['product_price']):,.2f}")
                price_item.setData(QtCore.Qt.UserRole, float(product['product_price']))  # For sorting
                self.tableWidget.setItem(row_num, 3, price_item)
                
                # Stock quantity
                self.tableWidget.setItem(row_num, 4, QTableWidgetItem(str(product["prod_spec_stock_qty"])))
                
                # Updated at (format date if needed)
                updated_at = product["product_updated_at"]
                if isinstance(updated_at, datetime):
                    updated_at = updated_at.strftime("%Y-%m-%d %H:%M")
                self.tableWidget.setItem(row_num, 5, QTableWidgetItem(str(updated_at)))
                
                # Color
                self.tableWidget.setItem(row_num, 6, QTableWidgetItem(str(product["prod_spec_color"] or "")))
                
                # Dimensions
                self.tableWidget.setItem(row_num, 7, QTableWidgetItem(str(product["prod_spec_length_mm"] or "")))
                self.tableWidget.setItem(row_num, 8, QTableWidgetItem(str(product["prod_spec_thickness_mm"] or "")))
                self.tableWidget.setItem(row_num, 9, QTableWidgetItem(str(product["prod_spec_width_mm"] or "")))
                
                # Other specifications
                self.tableWidget.setItem(row_num, 10, QTableWidgetItem(str(product["prod_spec_other"] or "")))

        except Exception as e:
            print(f"Error loading inventory: {e}")

    def search_inventory(self, search_text, category="ALL"):
        """
        Search inventory items by text
        
        Args:
            search_text (str): Text to search for
            category (str): Product category to filter
            
        Returns:
            list: Filtered inventory items (dict)
        """
        if not search_text:
            return self.get_inventory_by_category(category)

        try:
            products = InventoryModel.search_products(search_text)
            if category != "ALL":
                products = [p for p in products if p['prod_type_name'] == category]

            result = []
            for product in products:
                item = {
                    "prod_code": str(product['product_id']),
                    "name": product['product_name'],
                    "description": product.get('prod_spec_other', "") or "",
                    "price": float(product['product_price']),
                    "stock_qty": int(product['prod_spec_stock_qty']),
                    "type": product['prod_type_name'],
                    "length": int(product['prod_dimension_length_mm'] or 0),
                    "width": int(product['prod_dimension_width_mm'] or 0),
                    "color": product.get('prod_spec_color', "") or "",
                    "thickness": int(product['prod_dimension_thickness_mm'] or 0),
                }
                result.append(item)
            return result

        except Exception as e:
            print(f"Error searching inventory: {str(e)}")
            return []

    def populate_inventory_table(self, table_widget, items):
        """
        Populate a QTableWidget with inventory items
        
        Args:
            table_widget (QTableWidget): Table widget to populate
            items (list): List of inventory item dicts
            
        Returns:
            None
        """
        try:
            table_widget.setRowCount(0)
            if table_widget.columnCount() == 0:
                table_widget.setColumnCount(6)
                headers = ["ID", "Name", "Type", "Price", "Stock", "Color"]
                table_widget.setHorizontalHeaderLabels(headers)

            for row, item in enumerate(items):
                table_widget.insertRow(row)
                table_widget.setItem(row, 0, QTableWidgetItem(item['prod_code']))
                table_widget.setItem(row, 1, QTableWidgetItem(item['name']))
                table_widget.setItem(row, 2, QTableWidgetItem(item['type']))
                table_widget.setItem(row, 3, QTableWidgetItem(f"{item['price']:.2f}"))
                table_widget.setItem(row, 4, QTableWidgetItem(str(item['stock_qty'])))
                table_widget.setItem(row, 5, QTableWidgetItem(item['color']))
        except Exception as e:
            print(f"Error populating inventory table: {str(e)}")

    def add_stock(self, category, item_data):
        """
        Add new inventory item
        
        Args:
            category (str): Product category (ROOF, SPANDREL, GUTTER, OTHER)
            item_data (dict): Inventory item data
            
        Returns:
            bool: Success status
        """
        try:
            name = item_data.get("name", "").strip()
            price = float(item_data.get("price", 0))
            stock_qty = int(item_data.get("stock_qty", 0))
            color = item_data.get("color", "").strip()
            description = item_data.get("description", "").strip()
            length = int(item_data.get("length", 0) or 0)
            width = int(item_data.get("width", 0) or 0)
            thickness = int(item_data.get("thickness", 0) or 0)

            if not name:
                raise ValueError("Product name is required")
            if price <= 0:
                raise ValueError("Price must be greater than zero")
            if stock_qty < 0:
                raise ValueError("Stock quantity cannot be negative")

            product_id = InventoryModel.add_product(
                self.shop_id, category, name, price, stock_qty,
                color, length, width, thickness, description
            )
            if product_id is None:
                raise Exception("Failed to add product")

            return True

        except ValueError as ve:
            QMessageBox.warning(None, "Input Error", str(ve))
            return False
        except Exception as e:
            QMessageBox.critical(None, "System Error", f"Error adding inventory item: {str(e)}")
            return False

    def update_stock(self, category, product_id, item_data):
        """
        Update an existing inventory item
        
        Args:
            category (str): Product category
            product_id (str or int): Product ID
            item_data (dict): Updated inventory data
            
        Returns:
            bool: Success status
        """
        try:
            name = item_data.get("name")
            price = float(item_data["price"]) if item_data.get("price") is not None else None
            stock_qty = int(item_data["stock_qty"]) if item_data.get("stock_qty") is not None else None
            color = item_data.get("color")
            description = item_data.get("description")
            length = int(item_data["length"]) if item_data.get("length") is not None else None
            width = int(item_data["width"]) if item_data.get("width") is not None else None
            thickness = int(item_data["thickness"]) if item_data.get("thickness") is not None else None

            if price is not None and price <= 0:
                raise ValueError("Price must be greater than zero")
            if stock_qty is not None and stock_qty < 0:
                raise ValueError("Stock quantity cannot be negative")

            success = InventoryModel.update_product(
                int(product_id), name, price, stock_qty, color,
                length, width, thickness, description
            )
            if not success:
                raise Exception(f"Failed to update product {product_id}")

            return True

        except ValueError as ve:
            QMessageBox.warning(None, "Input Error", str(ve))
            return False
        except Exception as e:
            QMessageBox.critical(None, "System Error", f"Error updating inventory item: {str(e)}")
            return False

    def delete_stock(self, product_id):
        """
        Delete an inventory item
        
        Args:
            product_id (str or int): Product ID
            
        Returns:
            bool: Success status
        """
        try:
            pid = int(product_id)
            success = InventoryModel.delete_product(pid)
            if not success:
                raise Exception(f"Failed to delete product {product_id}")
            return True

        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error deleting inventory item: {str(e)}")
            return False

    def get_low_stock_products(self, threshold=10):
        """
        Get list of products with stock below threshold
        
        Args:
            threshold (int): Low stock threshold
            
        Returns:
            list: List of low stock products (dict)
        """
        try:
            return InventoryModel.get_low_stock_products(threshold)
        except Exception as e:
            print(f"Error getting low stock products: {str(e)}")
            return []