from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from core.models.COrders_pageModel import OrdersModel

class OrdersPageController:
    def __init__(self, orders_ui, cashier_controller):
        self.ui = orders_ui
        self.cashier_controller = cashier_controller
        self.database = cashier_controller.database
        self.orders_model = OrdersModel(self.database)
        self.current_order_items = []
        
        self.setup_connections()
        self.load_product_list()
    
    def setup_connections(self):
        """Setup all signal-slot connections"""
        self.ui.comboBox_filterProduct_List.currentTextChanged.connect(self.filter_product_list)
        self.ui.Add_Order_2.clicked.connect(self.add_to_order)
        self.ui.View_OrderSummary.clicked.connect(self.show_order_summary)
        self.ui.Back.clicked.connect(self.show_take_orders)
        self.ui.ConfirmandPrint.clicked.connect(self.confirm_and_print)
        self.ui.Remove.clicked.connect(self.remove_from_order)
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def filter_product_list(self, filter_text):
        """Filter product list based on selected type"""
        self.update_list_label(filter_text)
        
        if filter_text == "All Products":
            products = self.orders_model.get_all_products()
        else:
            type_mapping = {
                "Roof": "ROOF",
                "Spandrel": "SPANDREL", 
                "Gutter": "GUTTER",
                "Others": "OTHER"
            }
            db_type = type_mapping.get(filter_text, "ROOF")
            products = self.orders_model.get_products_by_type(db_type)
        
        self.display_products(products)
    
    def update_list_label(self, filter_text):
        """Update the label above the product list"""
        labels = {
            "Roof": "Roof Product List",
            "Spandrel": "Spandrel Product List",
            "Gutter": "Gutter Product List",
            "Others": "Other Product List",
            "All Products": "All Product List"
        }
        self.ui.orderReportText.setText(labels.get(filter_text, "Product List"))
    
    def load_product_list(self):
        """Load all products initially"""
        products = self.orders_model.get_all_products()
        self.display_products(products)
    
    def display_products(self, products):
        """Display products in the tableWidget_ProdList"""
        table = self.ui.tableWidget_ProdList
        table.setRowCount(0)
        
        if not products:
            return
        
        headers = [
            "Product ID", "Product Type", "Name", "Price", 
            "Stock Qty", "Updated At", "Color", "Length (mm)", 
            "Thickness (mm)", "Width (mm)", "Other Specs"
        ]
        
        if table.columnCount() == 0:
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
        
        for product in products:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            
            def format_value(value):
                if value is None:
                    return 'N/A'
                if isinstance(value, (int, float)) and value == 0:
                    return 'N/A'
                return str(value)
            
            updated_at = product.get('product_updated_at', '')
            updated_at = updated_at.strftime('%Y-%m-%d %H:%M:%S') if updated_at else 'N/A'
            
            values = [
                product['product_id'],
                product['prod_type_name'],
                product['product_name'],
                f"₱{float(product['product_price']):,.2f}",
                format_value(product.get('prod_spec_stock_qty')),
                updated_at,
                format_value(product.get('prod_spec_color')),
                format_value(product.get('prod_spec_length_mm')),
                format_value(product.get('prod_spec_thickness_mm')),
                format_value(product.get('prod_spec_width_mm')),
                format_value(product.get('prod_spec_other'))
            ]
            
            for col, value in enumerate(values):
                table.setItem(row_pos, col, QTableWidgetItem(value))
    
    def add_to_order(self):
        """Add selected product to current order"""
        selected_row = self.ui.tableWidget_ProdList.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Selection", "Please select a product first!")
            return
        
        product_id = self.ui.tableWidget_ProdList.item(selected_row, 0).text()
        quantity = self.ui.spinBox_quantity.value()
        
        if quantity <= 0:
            QMessageBox.warning(None, "Invalid Quantity", "Quantity must be at least 1!")
            return
        
        product = self.orders_model.get_product_details(product_id)
        if not product:
            QMessageBox.warning(None, "Error", "Could not retrieve product details!")
            return
        
        existing_item = next((item for item in self.current_order_items 
                            if item['product_id'] == product_id), None)
        
        if existing_item:
            existing_item['quantity'] += quantity
        else:
            self.current_order_items.append({
                'product_id': product_id,
                'name': product['product_name'],
                'type': product['prod_type_name'],
                'price': float(product['product_price']),
                'quantity': quantity,
                'color': product.get('prod_spec_color', 'N/A')
            })
        
        QMessageBox.information(None, "Added to Order", 
                              f"{quantity} {product['product_name']} added to order!")
    
    def show_order_summary(self):
        """Show the order summary with current items"""
        if not self.current_order_items:
            QMessageBox.warning(None, "Empty Order", "Your order is empty!")
            return
        
        self.update_order_summary()
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def update_order_summary(self):
        """Update the order summary table with current items"""
        table = self.ui.tableWidget_OrderSummary
        table.setRowCount(0)
        
        if not self.current_order_items:
            return
        
        if table.columnCount() == 0:
            headers = ["Product", "Price", "Qty", "Subtotal"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
        
        for item in self.current_order_items:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            
            table.setItem(row_pos, 0, QTableWidgetItem(item['name']))
            table.setItem(row_pos, 1, QTableWidgetItem(f"₱{item['price']:,.2f}"))
            table.setItem(row_pos, 2, QTableWidgetItem(str(item['quantity'])))
            table.setItem(row_pos, 3, QTableWidgetItem(f"₱{item['price'] * item['quantity']:,.2f}"))
        
        total = sum(item['price'] * item['quantity'] for item in self.current_order_items)
        self.ui.label_Total.setText(f"Total: ₱{total:,.2f}")
    
    def show_take_orders(self):
        """Switch back to take orders view"""
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def remove_from_order(self):
        """Remove selected item from order"""
        selected_row = self.ui.tableWidget_OrderSummary.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Selection", "Please select an item to remove!")
            return
        
        reply = QMessageBox.question(
            None, 'Confirm Removal', "Remove this item from order?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            del self.current_order_items[selected_row]
            self.update_order_summary()
            QMessageBox.information(None, "Removed", "Item removed from order!")
    
    def confirm_and_print(self):
        """Confirm order and print receipt"""
        if not self.current_order_items:
            QMessageBox.warning(None, "Empty Order", "Your order is empty!")
            return
        
        reply = QMessageBox.question(
            None, 'Confirm Order', "Confirm and print receipt for this order?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            try:
                order_id = self.save_order_to_database()
                self.print_receipt(order_id)
                self.current_order_items = []
                self.update_order_summary()
                QMessageBox.information(None, 'Success', f"Order #{order_id} confirmed!")
                self.show_take_orders()
            except Exception as e:
                QMessageBox.critical(None, 'Error', f"Failed to process order: {str(e)}")
    
    def save_order_to_database(self):
        """Save the current order to database and return order ID"""
        # TODO: Implement actual database saving
        return 1001  # Dummy ID
    
    def print_receipt(self, order_id):
        """Generate and print receipt for the order"""
        # TODO: Implement actual receipt printing
        print(f"Receipt for order #{order_id}")
        for item in self.current_order_items:
            print(f"{item['quantity']} x {item['name']} @ ₱{item['price']:,.2f}")
        total = sum(item['price'] * item['quantity'] for item in self.current_order_items)
        print(f"Total: ₱{total:,.2f}")