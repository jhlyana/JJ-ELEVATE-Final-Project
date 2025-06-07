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
        # self.ui.ConfirmandPrint.clicked.connect(self.confirm_and_print)
        # self.ui.Remove.clicked.connect(self.remove_from_order)
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
        """Add selected product to current order with validations"""
        selected_row = self.ui.tableWidget_ProdList.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Selection", "Please select a product first!")
            return

        # Get input values
        product_id = self.ui.tableWidget_ProdList.item(selected_row, 0).text()
        try:
            quantity = int(self.ui.OrderInput_Qty_2.text())
            discount = float(self.ui.OrderInput_Discount_2.text()) if self.ui.OrderInput_Discount_2.text() else 0.0
        except ValueError:
            QMessageBox.warning(None, "Invalid Input", "Please enter valid numbers for quantity and discount!")
            return

        # Get product details from database
        product = self.orders_model.get_product_details(product_id)
        if not product:
            QMessageBox.warning(None, "Error", "Could not retrieve product details!")
            return

        # Validate inputs
        available_stock = product.get('prod_spec_stock_qty', 0)
        if quantity <= 0:
            QMessageBox.warning(None, "Invalid Quantity", "Quantity must be at least 1!")
            return
        if quantity > available_stock:
            QMessageBox.warning(None, "Insufficient Stock", 
                            f"Only {available_stock} items available in stock!")
            return
        if discount < 0 or discount > 100:
            QMessageBox.warning(None, "Invalid Discount", "Discount must be between 0-100%!")
            return

        # Check for existing item in order
        existing_item = next((item for item in self.current_order_items 
                            if item['product_id'] == product_id), None)

        if existing_item:
            new_total = existing_item['quantity'] + quantity
            if new_total > available_stock:
                QMessageBox.warning(None, "Stock Exceeded",
                                f"Cannot add {quantity} more. Max available: {available_stock - existing_item['quantity']}")
                return
            existing_item['quantity'] = new_total
            existing_item['discount'] = discount  # Update discount if changed
        else:
            self.current_order_items.append({
                'product_id': product_id,
                'name': product['product_name'],
                'price': float(product['product_price']),
                'quantity': quantity,
                'discount': discount,
                'max_stock': available_stock
            })

        # Update UI and reset inputs
        self.update_order_summary()
        self.ui.OrderInput_prodnameDisplay_2.clear()
        self.ui.OrderInput_Qty_2.clear()
        self.ui.OrderInput_Discount_2.clear()
        
        QMessageBox.information(None, "Added to Order", 
                            f"{quantity} {product['product_name']} added to order!")
    
    def show_order_summary(self):
        """Show the order summary with current items"""
        if not self.current_order_items:
            QMessageBox.warning(None, "Empty Order", "Your order is empty!")
            return
        
        # Update product name display if coming from product selection
        selected_row = self.ui.tableWidget_ProdList.currentRow()
        if selected_row >= 0:
            product_name = self.ui.tableWidget_ProdList.item(selected_row, 2).text()
            self.ui.OrderInput_prodnameDisplay_2.setText(product_name)
        
        self.update_order_summary()
        self.ui.stackedWidget.setCurrentIndex(1)
        
    def update_order_summary(self):
        """Update the order summary table with current items"""
        table = self.ui.tableWidget_OrderSummary
        table.setRowCount(0)
        
        if not self.current_order_items:
            return
        
        # Configure table if needed
        if table.columnCount() == 0:
            headers = ["Name", "Qty", "Price", "Discount %", "Total"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
        
        # Add items to table
        for item in self.current_order_items:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            
            # Calculate discounted price
            discounted_price = item['price'] * (1 - item['discount']/100)
            total = discounted_price * item['quantity']
            
            table.setItem(row_pos, 0, QTableWidgetItem(item['name']))
            table.setItem(row_pos, 1, QTableWidgetItem(str(item['quantity'])))
            table.setItem(row_pos, 2, QTableWidgetItem(f"₱{item['price']:,.2f}"))
            table.setItem(row_pos, 3, QTableWidgetItem(f"{item['discount']}%"))
            table.setItem(row_pos, 4, QTableWidgetItem(f"₱{total:,.2f}"))
        
        # # Calculate and display grand total
        # grand_total = sum(
        #     item['price'] * (1 - item['discount']/100) * item['quantity'] 
        #     for item in self.current_order_items
        # )
        # self.ui.label_Total.setText(f"Total: ₱{grand_total:,.2f}")
    
    def show_take_orders(self):
        """Switch back to take orders view"""
        self.ui.stackedWidget.setCurrentIndex(0)
    
    # def remove_from_order(self):
    #     """Remove selected item from order"""
    #     selected_row = self.ui.tableWidget_OrderSummary.currentRow()
    #     if selected_row < 0:
    #         QMessageBox.warning(None, "No Selection", "Please select an item to remove!")
    #         return
        
    #     reply = QMessageBox.question(
    #         None, 'Confirm Removal', "Remove this item from order?",
    #         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
    #     if reply == QMessageBox.Yes:
    #         del self.current_order_items[selected_row]
    #         self.update_order_summary()
    #         QMessageBox.information(None, "Removed", "Item removed from order!")
    
    # def confirm_and_print(self):
    #     """Confirm order and print receipt"""
    #     if not self.current_order_items:
    #         QMessageBox.warning(None, "Empty Order", "Your order is empty!")
    #         return
        
    #     reply = QMessageBox.question(
    #         None, 'Confirm Order', "Confirm and print receipt for this order?",
    #         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
    #     if reply == QMessageBox.Yes:
    #         try:
    #             order_id = self.save_order_to_database()
    #             self.print_receipt(order_id)
    #             self.current_order_items = []
    #             self.update_order_summary()
    #             QMessageBox.information(None, 'Success', f"Order #{order_id} confirmed!")
    #             self.show_take_orders()
    #         except Exception as e:
    #             QMessageBox.critical(None, 'Error', f"Failed to process order: {str(e)}")
    
    def save_order_to_database(self):
        """Save the current order to database and return order ID"""
        try:
            cursor = self.database.connection.cursor()
            
            # 1. Save to order_header
            cursor.execute("""
                INSERT INTO order_header (
                    shop_id, user_acc_id, service_id,
                    oh_by_customer_name, oh_by_customer_contact_num, oh_by_customer_address
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                ) RETURNING oh_id
            """, (
                1,  # shop_id (adjust as needed)
                self.cashier_controller.user_id,  # user_acc_id
                1,  # service_id (adjust as needed)
                'Walk-in Customer',  # Default customer name
                'N/A',  # Default contact
                'N/A'   # Default address
            ))
            oh_id = cursor.fetchone()[0]
            
            # 2. Save each item to order_detail
            for item in self.current_order_items:
                cursor.execute("""
                    INSERT INTO order_detail (
                        product_id, shop_id, oh_id, od_quantity,
                        od_product_price, od_bulk_discount_pct, od_total_amt
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    item['product_id'],
                    1,  # shop_id (adjust as needed)
                    oh_id,
                    item['quantity'],
                    item['price'],
                    item['discount'],
                    item['price'] * (1 - item['discount']/100) * item['quantity']
                ))
                
                # 3. Update product stock
                cursor.execute("""
                    UPDATE product_specification
                    SET prod_spec_stock_qty = prod_spec_stock_qty - %s
                    WHERE product_id = %s AND shop_id = %s
                """, (item['quantity'], item['product_id'], 1))
            
            self.database.connection.commit()
            cursor.close()
            return oh_id
            
        except Exception as e:
            self.database.connection.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    def print_receipt(self, order_id):
        """Generate and print receipt for the order"""
        # TODO: Implement actual receipt printing
        print(f"Receipt for order #{order_id}")
        for item in self.current_order_items:
            print(f"{item['quantity']} x {item['name']} @ ₱{item['price']:,.2f}")
        total = sum(item['price'] * item['quantity'] for item in self.current_order_items)
        print(f"Total: ₱{total:,.2f}")