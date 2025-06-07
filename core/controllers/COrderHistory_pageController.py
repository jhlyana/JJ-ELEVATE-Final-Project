class OrderHistoryPageController:
    def __init__(self, orderHistory_ui, cashier_controller):
        self.ui = orderHistory_ui
        self.cashier_controller = cashier_controller
        
        # Connect the filter combo box to update the label
        self.ui.comboBox_filterOrders.currentTextChanged.connect(self.update_order_history_label)
        
        # Initialize label text based on the default combo box selection
        self.update_order_history_label(self.ui.comboBox_filterOrders.currentText())

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
            self.ui.orderReportText.setText("All Order History")  # Default/fallback