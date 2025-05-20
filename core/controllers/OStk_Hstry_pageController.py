class StockHistoryPageController:
    def __init__(self, stkhistory_ui, stkhistory_controller):
        self.ui = stkhistory_ui
        self.stkhistory_controller = stkhistory_controller
        
        # Connect the filter combo box to update the label
        self.ui.comboBox_filterStockHistory.currentTextChanged.connect(self.update_stock_history_label)
        
        # Initialize label text based on the default combo box selection
        self.update_stock_history_label(self.ui.comboBox_filterStockHistory.currentText())

    def update_stock_history_label(self, filter_text):
        """Update the stock history label based on the selected filter"""
        if filter_text == "Roof":
            self.ui.stockHistoryText.setText("Roof Stock History")
        elif filter_text == "Spandrel":
            self.ui.stockHistoryText.setText("Spandrel Stock History")
        elif filter_text == "Gutter":
            self.ui.stockHistoryText.setText("Gutter Stock History")
        elif filter_text == "Others":
            self.ui.stockHistoryText.setText("Other Stock History")
        else:
            self.ui.stockHistoryText.setText("Stock History")  # Default/fallback