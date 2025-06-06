from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

class OrdersPageController:
    def __init__(self, orders_ui, cashier_controller):
        self.ui = orders_ui
        self.cashier_controller = cashier_controller
        
        # Set initial view to Take Orders page (index 0)
        self.ui.stackedWidget.setCurrentIndex(0)
        
        # Connect button signals for Take Orders page
        self.ui.Add_Order_2.clicked.connect(self.add_order)
        self.ui.View_OrderSummary.clicked.connect(self.show_OrderSummary_page)
        
        # Connect button signals for Order Summary page
        self.ui.Back.clicked.connect(self.show_Take_Orders_page)
        self.ui.ConfirmandPrint.clicked.connect(self.confirm_and_print)
        self.ui.Remove.clicked.connect(self.remove_product)
    
    def add_order(self):
        """Handle Add Order button click"""
        QMessageBox.information(
            None, 
            'Order Added', 
            "Order added to Order Summary!", 
            QMessageBox.Ok
        )
        # Here you would add the actual order to your data structure
        # For example: self.cashier_controller.add_to_order(...)
    
    def show_OrderSummary_page(self):
        """Show the Order Summary page (index 1"""
        self.ui.stackedWidget.setCurrentIndex(1)
        # Here you would update the order summary display with current items
    
    def show_Take_Orders_page(self):
        """Show the Take Orders page (index 0)"""
        self.ui.stackedWidget.setCurrentIndex(0)
    
    def confirm_and_print(self):
        """Handle Confirm and Print button click"""
        reply = QMessageBox.question(
            None, 
            'Confirm Order', 
            "Order Confirmed! Print Receipt?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            # Here you would call your receipt printing function
            self.print_receipt()
            QMessageBox.information(
                None, 
                'Receipt Printed', 
                "Receipt has been printed!", 
                QMessageBox.Ok
            )
    
    def print_receipt(self):
        """Generate and print the receipt using fpdf2"""
        # This is where you would implement your actual receipt printing
        # Example:
        # from fpdf import FPDF
        # pdf = FPDF()
        # pdf.add_page()
        # pdf.set_font("Arial", size=12)
        # pdf.cell(200, 10, txt="Your Receipt", ln=1, align="C")
        # ... add more receipt content ...
        # pdf.output("receipt.pdf")
        pass
    
    def remove_product(self):
        """Handle Remove button click"""
        reply = QMessageBox.question(
            None, 
            'Remove Product', 
            "Are you sure you want to remove this product from Order Summary?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Here you would remove the selected product from your order
            # For example: self.cashier_controller.remove_from_order(...)
            QMessageBox.information(
                None, 
                'Product Removed', 
                "Product has been removed from order summary!", 
                QMessageBox.Ok
            )