from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from core.models.CSales_pageModel import SalesPageModel
from database import Database
from datetime import datetime

class SalesPageController:
    def __init__(self, sales_ui, sales_controller):
        self.ui = sales_ui
        self.sales_controller = sales_controller
        self.model = SalesPageModel(Database)

        self._setup_salestab_states()
        self._connect_sales_buttons()

        self.ui.stackedWidget_Sales.setCurrentIndex(0)
        self.set_active_button(self.ui.pushButton_summaryView)

        self._initialize_tables()
        self.ui.comboBox_filterSales.currentTextChanged.connect(self.update_sales_data)
        self.update_sales_data(self.ui.comboBox_filterSales.currentText())

    def _initialize_tables(self):
        """Initialize table settings and adjust column widths"""
        # Sales Summary Table
        self.ui.tableWidget_salesSummary.setColumnCount(5)
        self.ui.tableWidget_salesSummary.setHorizontalHeaderLabels([
            "Report ID", "Shop Branch", "Total Quantity Sold",
            "Total Revenue (₱)", "Date Generated"
        ])
        
        self.ui.tableWidget_salesSummary.setColumnWidth(0, 200)
        self.ui.tableWidget_salesSummary.setColumnWidth(1, 350)
        self.ui.tableWidget_salesSummary.setColumnWidth(2, 250)
        self.ui.tableWidget_salesSummary.setColumnWidth(3, 300)
        self.ui.tableWidget_salesSummary.setColumnWidth(4, 400)
        self.ui.tableWidget_salesSummary.horizontalHeader().setStretchLastSection(True)

        # Order Details Table
        self.ui.tableWidget_orderDetails.setColumnCount(5)
        self.ui.tableWidget_orderDetails.setHorizontalHeaderLabels([
            "Detail ID", "Product Name", "Quantity Sold",
            "Total Sales Amount (₱)", "Date Recorded"
        ])

        self.ui.tableWidget_orderDetails.setColumnWidth(0, 200)
        self.ui.tableWidget_orderDetails.setColumnWidth(1, 350)
        self.ui.tableWidget_orderDetails.setColumnWidth(2, 250)
        self.ui.tableWidget_orderDetails.setColumnWidth(3, 300)
        self.ui.tableWidget_orderDetails.setColumnWidth(4, 400)
        self.ui.tableWidget_orderDetails.horizontalHeader().setStretchLastSection(True)

    def update_sales_data(self, filter_text):
        """Update both tables based on filter selection"""
        self.update_sales_report_label(filter_text)
        self._load_sales_summary(filter_text)
        self._load_order_details(filter_text)

    def _load_sales_summary(self, filter_type):
        """Load data into sales summary table"""
        data = self.model.get_sales_summary_data(filter_type)
        self.ui.tableWidget_salesSummary.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))

                if col_idx == 2:
                    item.setText(f"{int(col_data)}")
                elif col_idx == 3:
                    item.setText(f"₱{float(col_data):,.2f}")
                elif col_idx == 4:
                    if isinstance(col_data, datetime):
                        item.setText(col_data.strftime("%Y-%m-%d %H:%M"))
                    else:
                        item.setText(str(col_data))

                self.ui.tableWidget_salesSummary.setItem(row_idx, col_idx, item)

    def _load_order_details(self, filter_type):
        """Load data into order details table"""
        data = self.model.get_order_details_data(filter_type)
        self.ui.tableWidget_orderDetails.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))

                if col_idx == 2:
                    item.setText(f"{col_data}")
                elif col_idx == 3:
                    item.setText(f"₱{float(col_data):,.2f}")
                elif col_idx == 4:
                    if isinstance(col_data, datetime):
                        item.setText(col_data.strftime("%Y-%m-%d %H:%M"))
                    else:
                        item.setText(str(col_data))

                self.ui.tableWidget_orderDetails.setItem(row_idx, col_idx, item)

    def update_sales_report_label(self, filter_text):
        """Update the sales report label based on the selected filter"""
        filter_text = filter_text.upper()

        if filter_text == "DAILY":
            self.ui.SALES_label.setText("Daily Sales Report")
        elif filter_text == "WEEKLY":
            self.ui.SALES_label.setText("Weekly Sales Report")
        elif filter_text == "MONTHLY":
            self.ui.SALES_label.setText("Monthly Sales Report")
        else:
            self.ui.SALES_label.setText("Sales Report")

    def _setup_salestab_states(self):
        self.sales_tab_buttons = [
            self.ui.pushButton_summaryView,
            self.ui.pushButton_salesDetail
        ]
        self.reset_button_styles()

    def reset_button_styles(self):
        """Reset all sales tab buttons to inactive state"""
        for button in self.sales_tab_buttons:
            button.setProperty('class', '')
            button.style().unpolish(button)
            button.style().polish(button)

    def _connect_sales_buttons(self):
        """Connect the sales tab buttons to their respective functions"""
        self.ui.pushButton_summaryView.clicked.connect(lambda: self.view_sales_tab(0))
        self.ui.pushButton_salesDetail.clicked.connect(lambda: self.view_sales_tab(1))

    def set_active_button(self, button):
        """Set a single button as active"""
        self.reset_button_styles()
        button.setProperty('class', 'activeButton')
        button.style().unpolish(button)
        button.style().polish(button)

    def view_sales_tab(self, index):
        """Switch to the specified sales tab and update button states"""
        self.ui.stackedWidget_Sales.setCurrentIndex(index)
        if index == 0:
            self.set_active_button(self.ui.pushButton_summaryView)
        elif index == 1:
            self.set_active_button(self.ui.pushButton_salesDetail)