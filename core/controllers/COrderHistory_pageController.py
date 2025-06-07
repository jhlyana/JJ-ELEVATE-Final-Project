from PyQt5.QtWidgets import QTableWidgetItem
from core.models.COrderHistory_pageModel import OrderHistory

class OrderHistoryPageController:
    def __init__(self, orderHistory_ui, cashier_controller):
        self.ui = orderHistory_ui
        self.cashier_controller = cashier_controller
        self.db = cashier_controller.database
        self.order_history_model = OrderHistory(self.db)
        
        # Initialize UI
        self.initialize_table()
        self.initialize_filter_options()
        self.load_order_history()
        
        # Connect signals
        self.ui.comboBox_filterOrders.currentTextChanged.connect(self.filter_orders)
        self.ui.pushButton_searchOrders.clicked.connect(self.search_orders)
        self.ui.lineEdit__QuickSearch_Orders.textChanged.connect(self.handle_quick_search)
        self.ui.lineEdit__QuickSearch_Orders.returnPressed.connect(self.search_orders)
        
        # Initialize label text
        self.update_order_history_label(self.ui.comboBox_filterOrders.currentText())

    def initialize_table(self):
        """Set up the table columns and headers"""
        headers = ["Order ID", "Product Name", "Price", "Qty", "Subtotal", "Total Amount (₱)"]
        self.ui.tableWidget_order_History.setColumnCount(len(headers))
        self.ui.tableWidget_order_History.setHorizontalHeaderLabels(headers)
        self.ui.tableWidget_order_History.setSortingEnabled(True)
        
        # Adjust column widths
        self.ui.tableWidget_order_History.setColumnWidth(0, 100)   # Order ID
        self.ui.tableWidget_order_History.setColumnWidth(1, 420)  # Product
        self.ui.tableWidget_order_History.setColumnWidth(2, 250)   # Price
        self.ui.tableWidget_order_History.setColumnWidth(3, 100)   # Quantity
        self.ui.tableWidget_order_History.setColumnWidth(4, 250)  # Subtotal
        self.ui.tableWidget_order_History.setColumnWidth(5, 400)  # Total Amount

    def initialize_filter_options(self):
        """Initialize the filter options in the combo box"""
        self.ui.comboBox_filterOrders.clear()
        self.ui.comboBox_filterOrders.addItems([
            "All Products",
            "Roof",
            "Spandrel",
            "Gutter",
            "Others"
        ])
        self.ui.comboBox_filterOrders.setCurrentIndex(0)

    def load_order_history(self, product_type=None, search_term=None):
        """Load order history data into the table"""
        # Convert "All Products" to None for the model
        if product_type == "All Products":
            product_type = None
            
        orders = self.order_history_model.get_all_orders(product_type, search_term)
        self.ui.tableWidget_order_History.setRowCount(len(orders))
        
        for row_idx, order in enumerate(orders):
            # Order ID
            self.ui.tableWidget_order_History.setItem(
                row_idx, 0, QTableWidgetItem(str(order['order_id']))
            )
            
            # Product
            self.ui.tableWidget_order_History.setItem(
                row_idx, 1, QTableWidgetItem(order['product'])
            )
            
            # Price
            self.ui.tableWidget_order_History.setItem(
                row_idx, 2, QTableWidgetItem(f"₱{order['price']:,.2f}")
            )
            
            # Quantity
            self.ui.tableWidget_order_History.setItem(
                row_idx, 3, QTableWidgetItem(str(order['quantity']))
            )
            
            # Subtotal
            self.ui.tableWidget_order_History.setItem(
                row_idx, 4, QTableWidgetItem(f"₱{order['subtotal']:,.2f}")
            )
            
            # Total Amount
            self.ui.tableWidget_order_History.setItem(
                row_idx, 5, QTableWidgetItem(f"₱{order['total_amount']:,.2f}")
            )

    def filter_orders(self):
        """Filter orders strictly based on the selected product type"""
        product_type = self.ui.comboBox_filterOrders.currentText()
        print(f"Filtering by product type: {product_type}")  # Debug print
        
        self.update_order_history_label(product_type)
        
        # Get current search term if any
        search_term = self.ui.lineEdit__QuickSearch_Orders.text().strip()
        if not search_term:
            search_term = None
            
        # Load orders with strict filtering
        self.load_order_history(product_type=product_type, search_term=search_term)

    def search_orders(self):
        """Search orders based on the search term (exact search when button pressed)"""
        search_term = self.ui.lineEdit__QuickSearch_Orders.text().strip()
        product_type = self.ui.comboBox_filterOrders.currentText()
        
        if product_type == "All Products":
            product_type = None
            
        if search_term:
            self.load_order_history(product_type=product_type, search_term=search_term)
        else:
            # If search term is empty, just reload with current filter
            self.load_order_history(product_type=product_type)

    def handle_quick_search(self, text):
        """Handle real-time searching while typing"""
        search_term = text.strip()
        product_type = self.ui.comboBox_filterOrders.currentText()
        
        if product_type == "All Products":
            product_type = None
            
        # Load with current filter and search term (can be empty)
        self.load_order_history(product_type=product_type, search_term=search_term)

    def update_order_history_label(self, filter_text):
        """Update the order history label based on the selected filter"""
        if filter_text == "Roof":
            self.ui.orderReportText.setText("Roof Order History")
        elif filter_text == "Spandrel":
            self.ui.orderReportText.setText("Spandrel Order History")
        elif filter_text == "Gutter":
            self.ui.orderReportText.setText("Gutter Order History")
        elif filter_text == "Others":
            self.ui.orderReportText.setText("Other Orders History")
        else:
            self.ui.orderReportText.setText("All Order History")