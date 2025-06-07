from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView
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
        
        # Quick Search functionality
        self.ui.lineEdit__QuicksearchProduct.textChanged.connect(self.quick_search_live)
        self.ui.pushButton_searchProduct.clicked.connect(self.quick_search_exact)
        
        # Set table selection behavior and style for PRODUCT LIST and ORDER SUMMARY
        self.ui.tableWidget_ProdList.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget_ProdList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tableWidget_OrderSummary.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget_OrderSummary.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # selection highlight and style sheet that keeps headers dark blue always
        style = """
            /* Base table styling */
            QTableWidget {
                background-color: white;
                gridline-color: lightgray;
            }
            
            /* Header styling - keeps dark blue always */
            QHeaderView::section {
                background-color: #003366;
                color: white;
                font-weight: bold;
                padding: 3px;
                border: none;
            }
            
            /* Header styling when hovered/pressed */
            QHeaderView::section:hover,
            QHeaderView::section:pressed {
                background-color: #003366;
            }
            
            /* Row selection styling */
            QTableView::item:selected {
                background-color: #0078d7;
                color: white;
            }
            
            /* Ensure header doesn't change during selection */
            QHeaderView {
                background-color: #003366;
            }
        """
        
        self.ui.tableWidget_ProdList.setStyleSheet(style)
        self.ui.tableWidget_OrderSummary.setStyleSheet(style)
        
        # Connect selection change signal
        self.ui.tableWidget_ProdList.itemSelectionChanged.connect(self.update_selected_product_display)
        
        self.ui.stackedWidget.setCurrentIndex(0)

    def quick_search_live(self, search_text):
        """Live search as user types"""
        if not search_text.strip():  # If search field is empty
            self.filter_product_list(self.ui.comboBox_filterProduct_List.currentText())
            return
        
        # Get all products first (or use current filtered list)
        if self.ui.comboBox_filterProduct_List.currentText() == "All Products":
            products = self.orders_model.get_all_products()
        else:
            type_mapping = {
                "Roof": "ROOF",
                "Spandrel": "SPANDREL", 
                "Gutter": "GUTTER",
                "Others": "OTHER"
            }
            db_type = type_mapping.get(self.ui.comboBox_filterProduct_List.currentText(), "ROOF")
            products = self.orders_model.get_products_by_type(db_type)
        
        # Filter products based on search text (case insensitive)
        search_text = search_text.lower()
        filtered_products = []
        
        for p in products:
            # Convert all values to lowercase strings for comparison
            values_to_check = [
                p['product_id'].lower(),
                p['prod_type_name'].lower(),
                p['product_name'].lower(),
                str(p['product_price']).lower(),
                str(p.get('prod_spec_stock_qty', '')).lower(),
                str(p.get('product_updated_at', '')).lower(),
                str(p.get('prod_spec_color', '')).lower(),
                str(p.get('prod_spec_length_mm', '')).lower(),
                str(p.get('prod_spec_thickness_mm', '')).lower(),
                str(p.get('prod_spec_width_mm', '')).lower(),
                str(p.get('prod_spec_other', '')).lower()
            ]
            
            if any(search_text in value for value in values_to_check):
                filtered_products.append(p)
        
        self.display_products(filtered_products)

    def quick_search_exact(self):
        """Exact search when search button is clicked"""
        search_text = self.ui.lineEdit__QuicksearchProduct.text().strip()
        if not search_text:
            self.filter_product_list(self.ui.comboBox_filterProduct_List.currentText())
            return
        
        # Get all products from database for exact search
        products = self.orders_model.search_products_all_fields(search_text)
        self.display_products(products)
    
    def update_selected_product_display(self):
        """Update product name display when selection changes"""
        selected = self.ui.tableWidget_ProdList.selectedItems()
        if selected:
            row = selected[0].row()
            product_name = self.ui.tableWidget_ProdList.item(row, 2).text()
            self.ui.OrderInput_prodnameDisplay_2.setText(product_name)
            self.ui.OrderInput_Qty_2.setFocus()

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
            "All Products": "All Products List"
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
        selected_items = self.ui.tableWidget_ProdList.selectedItems()
        if not selected_items:
            QMessageBox.warning(None, "No Selection", "Please select a product first!")
            return

        selected_row = selected_items[0].row()
        product_id = self.ui.tableWidget_ProdList.item(selected_row, 0).text()
        
        try:
            quantity = int(self.ui.OrderInput_Qty_2.text())
            discount = float(self.ui.OrderInput_Discount_2.text()) if self.ui.OrderInput_Discount_2.text() else 0.0
        except ValueError:
            QMessageBox.warning(None, "Invalid Input", "Please enter valid numbers for quantity and discount!")
            return

        product = self.orders_model.get_product_details(product_id)
        if not product:
            QMessageBox.warning(None, "Error", "Could not retrieve product details!")
            return

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

        existing_item = next((item for item in self.current_order_items 
                            if item['product_id'] == product_id), None)

        if existing_item:
            new_total = existing_item['quantity'] + quantity
            if new_total > available_stock:
                QMessageBox.warning(None, "Stock Exceeded",
                                f"Cannot add {quantity} more. Max available: {available_stock - existing_item['quantity']}")
                return
            existing_item['quantity'] = new_total
            existing_item['discount'] = discount
        else:
            self.current_order_items.append({
                'product_id': product_id,
                'name': product['product_name'],
                'price': float(product['product_price']),
                'quantity': quantity,
                'discount': discount,
                'max_stock': available_stock
            })

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
        
        self.update_order_summary()
        self.ui.stackedWidget.setCurrentIndex(1)
        
    def update_order_summary(self):
        """Update the order summary table with current items"""
        table = self.ui.tableWidget_OrderSummary
        table.setRowCount(0)
        
        if not self.current_order_items:
            return
        
        if table.columnCount() == 0:
            headers = ["Name", "Qty", "Price", "Discount %", "Total"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
        
        for item in self.current_order_items:
            row_pos = table.rowCount()
            table.insertRow(row_pos)
            
            discounted_price = item['price'] * (1 - item['discount']/100)
            total = discounted_price * item['quantity']
            
            table.setItem(row_pos, 0, QTableWidgetItem(item['name']))
            table.setItem(row_pos, 1, QTableWidgetItem(str(item['quantity'])))
            table.setItem(row_pos, 2, QTableWidgetItem(f"₱{item['price']:,.2f}"))
            table.setItem(row_pos, 3, QTableWidgetItem(f"{item['discount']}%"))
            table.setItem(row_pos, 4, QTableWidgetItem(f"₱{total:,.2f}"))
    
    def show_take_orders(self):
        """Switch back to take orders view"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def remove_from_order(self):
        """Remove selected item from order"""
        # Get the currently selected row
        selected_row = self.ui.tableWidget_OrderSummary.currentRow()
        
        # Validate selection
        if selected_row < 0 or selected_row >= len(self.current_order_items):
            QMessageBox.warning(
                None, 
                "No Selection", 
                "Please select an item to remove by clicking on a row first"
            )
            return
        
        # Get product name for confirmation message
        product_name = self.current_order_items[selected_row]['name']
        
        # Confirm removal
        reply = QMessageBox.question(
            None, 
            'Confirm Removal', 
            f"Remove {product_name} from the current order?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        # Process removal if confirmed
        if reply == QMessageBox.Yes:
            del self.current_order_items[selected_row]
            self.update_order_summary()
            QMessageBox.information(
                None, 
                "Removed", 
                f"{product_name} has been removed from the order"
            )

    def validate_order_details(self):
        """Validate all required order details before confirmation"""
        # Check if all required fields are filled
        customer_name = self.ui.OrderSummary_CusName.text().strip()
        address = self.ui.OrderSummary_CusAddress.text().strip()
        service = self.ui.OrderSummary_CusService.text().strip()
        contact = self.ui.OrderSummary_CusContactNumber.text().strip()
        cash = self.ui.OrderSummary_CusCash.text().strip()
        
        # Validate required fields
        if not all([customer_name, address, service, contact, cash]):
            QMessageBox.warning(None, "Missing Information", 
                            "Please fill in all customer details before confirming the order!")
            return False
        
        # Validate service options (case-sensitive to match DB)
        valid_services = {'Install', 'Supply', 'Repair', 'Deliver'}  # Note title case
        input_services = {s.strip().capitalize() for s in service.split('&')}
        
        if not input_services.issubset(valid_services):
            QMessageBox.warning(None, "Invalid Service", 
                            "Service must be one or more of: Install, Supply, Repair, Deliver (separated by &)")
            return False
        
        # Format services properly for display
        formatted_services = ' & '.join(input_services)
        self.ui.OrderSummary_CusService.setText(formatted_services)
        
        # Validate cash amount
        try:
            cash_amount = float(cash)
            if cash_amount <= 0:
                QMessageBox.warning(None, "Invalid Amount", 
                                "Amount paid must be greater than 0!")
                return False
        except ValueError:
            QMessageBox.warning(None, "Invalid Amount", 
                            "Please enter a valid number for amount paid!")
            return False
        
        # Check if there are items in the order
        if not self.current_order_items:
            QMessageBox.warning(None, "Empty Order", 
                            "Please add items to the order before confirming!")
            return False
        
        return True

    def confirm_and_print(self):
        """Confirm order and print receipt"""
        if not self.validate_order_details():
            return
        
        reply = QMessageBox.question(
            None, 'Confirm Order', 
            "Confirm and print receipt for this order?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if reply == QMessageBox.Yes:
            try:
                # Save order to database
                order_id = self.save_order_to_database()
                
                # Ask if ready to print receipt
                print_reply = QMessageBox.question(
                    None, 'Print Receipt', 
                    "Order confirmed and saved! Ready to print receipt?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                
                if print_reply == QMessageBox.Yes:
                    self.print_receipt(order_id)
                
                # Reset for new order
                self.current_order_items = []
                self.update_order_summary()
                self.clear_order_fields()
                self.show_take_orders()
                
            except Exception as e:
                QMessageBox.critical(None, 'Error', f"Failed to process order: {str(e)}")

    def clear_order_fields(self):
        """Clear all order input fields"""
        self.ui.OrderSummary_CusName.clear()
        self.ui.OrderSummary_CusAddress.clear()
        self.ui.OrderSummary_CusService.clear()
        self.ui.OrderSummary_CusContactNumber.clear()
        self.ui.OrderSummary_CusCash.clear()

    def save_order_to_database(self):
        """Save the current order to database and return order ID"""
        try:
            cursor = self.database.connection.cursor()
            
            # Get all required values from UI
            customer_name = self.ui.OrderSummary_CusName.text().strip()
            address = self.ui.OrderSummary_CusAddress.text().strip()
            service = self.ui.OrderSummary_CusService.text().strip()
            contact = self.ui.OrderSummary_CusContactNumber.text().strip()
            cash = float(self.ui.OrderSummary_CusCash.text().strip())
            
            # Calculate order totals
            subtotal = sum(
                item['price'] * item['quantity'] 
                for item in self.current_order_items
            )
            
            total_discount = sum(
                (item['price'] * item['quantity']) * (item['discount'] / 100)
                for item in self.current_order_items
            )
            
            total_amount = subtotal - total_discount
            change = cash - total_amount
            
            if change < 0:
                raise ValueError("Cash amount is less than total amount to pay!")
            
            # 1. Get service ID(s) - use exact case matching
            service_parts = [s.strip() for s in service.split('&')]  # Remove .lower()
            primary_service = service_parts[0]
            
            cursor.execute(
                "SELECT service_id FROM service WHERE service_name = %s",  # Removed LOWER()
                (primary_service,)
            )
            service_id = cursor.fetchone()
            if not service_id:
                raise ValueError(f"Invalid service: {primary_service}")
            service_id = service_id[0]
            
            # 2. Save to order_header
            cursor.execute("""
                INSERT INTO order_header (
                    shop_id, user_acc_id, service_id,
                    oh_by_customer_name, oh_by_customer_contact_num, oh_by_customer_address
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                ) RETURNING oh_id
            """, (
                1,  # shop_id (adjust as needed)
                self.cashier_controller.user_id,
                service_id,
                customer_name,
                contact,
                address
            ))
            oh_id = cursor.fetchone()[0]
            
            # 3. Save each item to order_detail
            for item in self.current_order_items:
                item_total = item['price'] * (1 - item['discount']/100) * item['quantity']
                
                cursor.execute("""
                    INSERT INTO order_detail (
                        product_id, shop_id, oh_id, od_quantity,
                        od_product_price, od_bulk_discount_pct, od_total_amt
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    item['product_id'],
                    1,  # shop_id
                    oh_id,
                    item['quantity'],
                    item['price'],
                    item['discount'],
                    item_total
                ))
                
                # 4. Update product stock
                cursor.execute("""
                    UPDATE product_specification
                    SET prod_spec_stock_qty = prod_spec_stock_qty - %s
                    WHERE product_id = %s AND shop_id = %s
                """, (item['quantity'], item['product_id'], 1))
            
            # 5. Save to receipt table
            cursor.execute("""
                INSERT INTO receipt (
                    shop_id, oh_id, user_acc_id, service_id,
                    receipt_discount_applied, receipt_subtotal, receipt_final_amt,
                    receipt_customer_name, receipt_customer_contact_num, receipt_customer_address,
                    receipt_cash, receipt_change
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                1,  # shop_id
                oh_id,
                self.cashier_controller.user_id,
                service_id,
                total_discount,
                subtotal,
                total_amount,
                customer_name,
                contact,
                address,
                cash,
                change
            ))
            
            self.database.connection.commit()
            cursor.close()
            return oh_id
            
        except Exception as e:
            self.database.connection.rollback()
            raise Exception(f"Database error: {str(e)}")

    def print_receipt(self, order_id):
        """Generate and print receipt for the order"""
        try:
            cursor = self.database.connection.cursor()
            
            # 1. Get order header and receipt information
            cursor.execute("""
                SELECT 
                    oh.oh_id, oh.oh_created_at, oh.user_acc_id,
                    r.receipt_subtotal, r.receipt_discount_applied, 
                    r.receipt_final_amt, r.receipt_cash, r.receipt_change,
                    oh.oh_by_customer_name, oh.oh_by_customer_contact_num, oh.oh_by_customer_address,
                    s.service_name,
                    sh.shop_branch_name, sh.shop_location,
                    ua.user_acc_username
                FROM order_header oh
                JOIN receipt r ON oh.oh_id = r.oh_id
                JOIN service s ON oh.service_id = s.service_id
                JOIN shop sh ON oh.shop_id = sh.shop_id
                JOIN user_account ua ON oh.user_acc_id = ua.user_acc_id
                WHERE oh.oh_id = %s
            """, (order_id,))
            
            order_info = cursor.fetchone()
            if not order_info:
                raise ValueError("Order not found in database!")
            
            # 2. Get order details
            cursor.execute("""
                SELECT 
                    p.product_name, od.od_quantity, 
                    od.od_product_price, od.od_bulk_discount_pct,
                    od.od_total_amt
                FROM order_detail od
                JOIN product p ON od.product_id = p.product_id
                WHERE od.oh_id = %s
            """, (order_id,))
            
            order_items = cursor.fetchall()
            
            cursor.close()
            
            # 3. Prepare receipt data
            receipt_data = {
                'order_id': order_info[0],
                'date_time': order_info[1].strftime('%Y-%m-%d %H:%M:%S'),
                'cashier_id': order_info[2],
                'cashier_name': order_info[13],
                'subtotal': float(order_info[3]),
                'discount': float(order_info[4]),
                'total': float(order_info[5]),
                'cash': float(order_info[6]),
                'change': float(order_info[7]),
                'customer_name': order_info[8],
                'customer_contact': order_info[9],
                'customer_address': order_info[10],
                'service': order_info[11],
                'shop_name': order_info[12],
                'shop_location': order_info[13],
                'items': [{
                    'name': item[0],
                    'quantity': item[1],
                    'price': float(item[2]),
                    'discount': float(item[3]),
                    'total': float(item[4])
                } for item in order_items]
            }
            
            # 4. Generate PDF receipt (you'll need to implement this)
            self.generate_pdf_receipt(receipt_data)
            
            QMessageBox.information(None, "Success", "Receipt generated successfully!")
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to generate receipt: {str(e)}")

    def generate_pdf_receipt(self, receipt_data):
        """Generate PDF receipt using fpdf"""
        from fpdf import FPDF
        
        try:
            # Create PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Use built-in Arial font (available on Windows)
            pdf.set_font("Arial", 'B', 16)
            
            # Header
            pdf.cell(0, 10, "J&J Elevate", ln=1, align='C')
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"{receipt_data['shop_name']} - {receipt_data['shop_location']}", ln=1, align='C')
            
            # Title
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, "RECEIPT", ln=1, align='C')
            pdf.ln(5)
            
            # Order info
            pdf.set_font("Arial", '', 10)
            pdf.cell(0, 10, f"Order ID: {receipt_data['order_id']}", ln=1)
            pdf.cell(0, 10, f"Date and Time: {receipt_data['date_time']}", ln=1)
            pdf.cell(0, 10, f"Cashier ID: {receipt_data['cashier_id']}", ln=1)
            pdf.ln(5)
            
            # Customer info
            pdf.cell(0, 10, f"Customer: {receipt_data['customer_name']}", ln=1)
            pdf.cell(0, 10, f"Contact: {receipt_data['customer_contact']}", ln=1)
            pdf.cell(0, 10, f"Address: {receipt_data['customer_address']}", ln=1)
            pdf.ln(10)
            
            # Items table header
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(80, 10, "Item", border=1)
            pdf.cell(30, 10, "Qty", border=1)
            pdf.cell(30, 10, "Price", border=1)
            pdf.cell(30, 10, "Total", border=1, ln=1)
            
            # Items - replace peso sign with PHP if needed
            pdf.set_font("Arial", '', 10)
            for item in receipt_data['items']:
                pdf.cell(80, 10, item['name'], border=1)
                pdf.cell(30, 10, str(item['quantity']), border=1)
                try:
                    pdf.cell(30, 10, f"₱{item['price']:,.2f}", border=1)
                    pdf.cell(30, 10, f"₱{item['total']:,.2f}", border=1, ln=1)
                except:
                    # Fallback if peso sign doesn't work
                    pdf.cell(30, 10, f"PHP{item['price']:,.2f}", border=1)
                    pdf.cell(30, 10, f"PHP{item['total']:,.2f}", border=1, ln=1)
            
            # Totals
            pdf.ln(5)
            try:
                pdf.cell(0, 10, f"Subtotal: ₱{receipt_data['subtotal']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Discount: ₱{receipt_data['discount']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Total Amount: ₱{receipt_data['total']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Cash: ₱{receipt_data['cash']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Change: ₱{receipt_data['change']:,.2f}", ln=1)
            except:
                # Fallback if peso sign doesn't work
                pdf.cell(0, 10, f"Subtotal: PHP{receipt_data['subtotal']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Discount: PHP{receipt_data['discount']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Total Amount: PHP{receipt_data['total']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Cash: PHP{receipt_data['cash']:,.2f}", ln=1)
                pdf.cell(0, 10, f"Change: PHP{receipt_data['change']:,.2f}", ln=1)
            
            pdf.ln(10)
            
            # Service
            pdf.cell(0, 10, f"Service Availed: {receipt_data['service']}", ln=1)
            pdf.ln(10)
            
            # Footer
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 10, "Thank You for your purchase!", ln=1, align='C')
            
            # Save PDF
            filename = f"receipt_{receipt_data['order_id']}.pdf"
            pdf.output(filename)
            
            # Open the PDF (optional)
            import os
            os.startfile(filename)
            
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")