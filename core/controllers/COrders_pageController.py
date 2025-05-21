from PyQt5.QtWidgets import QMessageBox

class OrdersPageController:
    def __init__(self, orders_ui, cashier_controller):
        self.ui = orders_ui
        self.cashier_controller = cashier_controller
        
        # Set initial view to index 0
        self.ui.stackedWidget_Orders.setCurrentIndex(0)
        
        # Connect button signals
        self.ui.Add_Order.clicked.connect(self.show_add_order_page)
        self.ui.OrderSummary_submitOrder.clicked.connect(self.show_receipt_page)
        self.ui.OrderSummary_cancelOrder.clicked.connect(self.cancel_order)
        self.ui.Save_Receipt.clicked.connect(self.save_receipt)
        self.ui.Close.clicked.connect(self.close_receipt)
    
    def show_add_order_page(self):
        """Show the add order page (index 1)"""
        self.ui.stackedWidget_Orders.setCurrentIndex(1)
    
    def show_receipt_page(self):
        """Show the receipt page (index 2)"""
        self.ui.stackedWidget_Orders.setCurrentIndex(2)
    
    def cancel_order(self):
        """Handle cancel order confirmation"""
        reply = QMessageBox.question(
            None, 'Cancel Order',
            "Are you sure you want to Cancel and Reset current Order?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            # Reset form and stay on current index (1)
            self.reset_order_form()
        else:
            # Go back to index 0
            self.ui.stackedWidget_Orders.setCurrentIndex(0)
    
    def reset_order_form(self):
        """Reset the order form fields"""
        # Add your form reset logic here
        pass
    
    def save_receipt(self):
        """Handle save receipt confirmation"""
        QMessageBox.information(
            None, 'Order Completed',
            "Order Completed! Save Receipt?",
            QMessageBox.Ok
        )
        # Add your receipt saving logic here
    
    def close_receipt(self):
        """Handle close receipt confirmation"""
        reply = QMessageBox.question(
            None, 'Next Order',
            "Proceed to next order?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Go back to index 0 for new order
            self.ui.stackedWidget_Orders.setCurrentIndex(0)
            self.reset_order_form()
        # Else stay on current index (2)