from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import QTimer
from database import Database
from core.models.OStk_Hstry_model import StockHistoryModel

class StockHistoryPageController:
    # Column constants for stock history table
    COL_HISTORY_ID = 0
    COL_USER_ID = 1
    COL_USERNAME = 2
    COL_ACTION = 3
    COL_PRODUCT_NAME = 4
    COL_OLD_QTY = 5
    COL_NEW_QTY = 6
    COL_UPDATED_AT = 7

    def __init__(self, history_ui, history_widget, database, current_user_shop_id=None, # Added database parameter
                 current_user_id=None, current_username=None, parent=None):
        self.ui = history_ui
        self.history_widget = history_widget
        self.parent = parent
        self.database = database # Store the passed database instance
        
        # User/Shop ID initialization
        self.current_user_shop_id = current_user_shop_id if current_user_shop_id is not None else 1
        self.current_user_id = current_user_id if current_user_id is not None else 1
        self.current_username = current_username if current_username is not None else "admin_user"
        
        print(f"DEBUG: StockHistoryPageController initialized with Shop ID: {self.current_user_shop_id}, User ID: {self.current_user_id}, Username: {self.current_username}")
        
        # Initialize StockHistoryModel with the passed database
        try:
            # Pass the already connected database instance
            self.history_model = StockHistoryModel(self.database)
        except Exception as e:
            print(f"Error initializing StockHistoryModel in controller: {e}")
            self.history_model = None
        
        # Initialize search timer for debouncing
        self.search_timer = QTimer()
        self.search_timer.timeout.connect(self.filter_stock_history)
        self.search_timer.setSingleShot(True)
        
        self.current_selected_history = None
        self._setup_stock_history_connections()
        self.initialize_stock_history_table()
        self.load_stock_history()

    def _setup_stock_history_connections(self):
        """Setup stock history UI connections with error handling"""
        try:
            # Connect filter dropdown
            if hasattr(self.ui, 'comboBox_filterStockHistory'):
                self.ui.comboBox_filterStockHistory.currentTextChanged.connect(
                    lambda text: self.update_stock_history_label(text)
                )
                self.ui.comboBox_filterStockHistory.currentTextChanged.connect(self.load_stock_history)
            
            # Connect search functionality with debouncing
            if hasattr(self.ui, 'lineEdit_OWNER_QuickSearch_StockHistory'):
                self.ui.lineEdit_OWNER_QuickSearch_StockHistory.textChanged.connect(self._on_search_text_changed)
            
            # Connect action buttons
            if hasattr(self.ui, 'pushButton_SEARCHStockHistory'):
                self.ui.pushButton_SEARCHStockHistory.clicked.connect(self.filter_stock_history)
            
            if hasattr(self.ui, 'pushButton_DeleteSelectedStockHistory'):
                self.ui.pushButton_DeleteSelectedStockHistory.clicked.connect(self.delete_selected_history)
            
            if hasattr(self.ui, 'pushButton_DeleteAllStockHistory'):
                self.ui.pushButton_DeleteAllStockHistory.clicked.connect(self.delete_all_stock_history)
            
        except AttributeError as e:
            self._show_error_message(f"Critical UI element missing for Stock History: {e}\nPlease check your UI design file.", title="UI Connection Error")
        except Exception as e:
            self._show_error_message(f"An unexpected error occurred during Stock History connection setup: {e}", title="Connection Setup Error")

    def initialize_stock_history_table(self):
        """Initialize the stock history table with columns, with robustness checks"""
        try:
            self.ui.tableWidget_StockHistory.setColumnCount(8)  # Increased to 8 for the hidden ID
            self.ui.tableWidget_StockHistory.setHorizontalHeaderLabels([
                "History ID",  # Hidden
                "User ID",
                "Username", 
                "Action",
                "Product Name",
                "Old Qty",
                "New Qty",
                "Updated At"
            ])
            self.ui.tableWidget_StockHistory.setColumnHidden(self.COL_HISTORY_ID, True)  # Hide the ID column
            
            # Set table properties
            self.ui.tableWidget_StockHistory.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.ui.tableWidget_StockHistory.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.ui.tableWidget_StockHistory.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            self.ui.tableWidget_StockHistory.setSortingEnabled(True)  # Enable sorting by columns
            
            # Set initial column widths
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_USER_ID, 160)
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_USERNAME, 170)
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_ACTION, 180)
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_PRODUCT_NAME, 260)
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_OLD_QTY, 180)
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_NEW_QTY, 180)
            self.ui.tableWidget_StockHistory.setColumnWidth(self.COL_UPDATED_AT, 290)
            
            # Set resize modes
            header = self.ui.tableWidget_StockHistory.horizontalHeader()
            header.setSectionResizeMode(self.COL_USER_ID, QHeaderView.Fixed)
            header.setSectionResizeMode(self.COL_USERNAME, QHeaderView.Fixed)
            header.setSectionResizeMode(self.COL_ACTION, QHeaderView.Fixed)
            header.setSectionResizeMode(self.COL_PRODUCT_NAME, QHeaderView.Fixed)
            header.setSectionResizeMode(self.COL_OLD_QTY, QHeaderView.Fixed)
            header.setSectionResizeMode(self.COL_NEW_QTY, QHeaderView.Fixed)
            header.setSectionResizeMode(self.COL_UPDATED_AT, QHeaderView.Fixed)
            
        except AttributeError as e:
            self._show_error_message(f"Critical table widget or UI element missing: {e}\nPlease check your UI design file (tableWidget_StockHistory).", title="Table Init Error")
        except Exception as e:
            self._show_error_message(f"An unexpected error occurred during Stock History table initialization: {e}", title="Table Init Error")

    def update_stock_history_label(self, filter_text: str):
        """Update the stock history label based on the selected filter"""
        try:
            # Using a dictionary for cleaner mapping
            label_map = {
                "roof": "Roof Stock History",
                "spandrel": "Spandrel Stock History", 
                "gutter": "Gutter Stock History",
                "others": "Other Stock History",
                "filter history": "All Stock History" # Default for "Filter History"
            }
            # Remove leading/trailing spaces and convert to lowercase for robust comparison
            normalized_filter = filter_text.strip().lower()
            self.ui.stockHistoryText.setText(label_map.get(normalized_filter, "All Stock History"))
        except AttributeError as e:
            self._show_error_message(f"Missing 'stockHistoryText' label in UI: {e}. Check your UI file.", title="UI Label Error")
        except Exception as e:
            self._show_error_message(f"An unexpected error occurred updating history label: {e}", title="Label Update Error")

    def load_stock_history(self):
        """Load stock history data based on current filter"""
        if self.history_model is None:
            self._show_error_message("Cannot load stock history: History model not initialized.", title="Initialization Error")
            self.ui.tableWidget_StockHistory.setRowCount(0)
            return

        try:
            # Store current column widths before reloading
            column_widths = {}
            for col in range(self.ui.tableWidget_StockHistory.columnCount()):
                column_widths[col] = self.ui.tableWidget_StockHistory.columnWidth(col)
            
            filter_text = self.ui.comboBox_filterStockHistory.currentText().strip()
            print(f"DEBUG: Selected filter text: '{filter_text}'")
            
            # Map UI filter text to database values
            type_mapping = {
                "Filter History": None,  # Assuming "Filter History" means no specific type filter
                "Roof": "ROOF",
                "Spandrel": "SPANDREL",
                "Gutter": "GUTTER",
                "Others": "OTHER"
            }
            # Get the database product type (None means no filtering)
            db_product_type = type_mapping.get(filter_text, None)

            # Get history data
            history_data = self.history_model.get_stock_history(
                product_type=db_product_type,
                shop_id=self.current_user_shop_id
            )

            # Populate table
            self._populate_history_table(history_data)  # Pass the list directly
            for col, width in column_widths.items():
                if col < self.ui.tableWidget_StockHistory.columnCount():  # Ensure column exists
                    self.ui.tableWidget_StockHistory.setColumnWidth(col, width)
        except AttributeError as e:
            self._show_error_message(f"UI element for filter combo box missing: {e}. Check your UI file.", title="UI Element Error")
        except Exception as e:
            self._show_error_message(f"Failed to load stock history: {str(e)}", title="Load History Error")

    def _populate_history_table(self, history_data: list):
        """Populate the table with history data"""
        try:
            # Store current column widths
            column_widths = {}
            for col in range(self.ui.tableWidget_StockHistory.columnCount()):
                column_widths[col] = self.ui.tableWidget_StockHistory.columnWidth(col)
                
            self.ui.tableWidget_StockHistory.setRowCount(0)  # Clear existing rows
            if not history_data:
                print("No stock history data to display.")
                return

            # Ensure column count is correct if headers were reset or changed
            if self.ui.tableWidget_StockHistory.columnCount() != 8:
                self.initialize_stock_history_table()  # Re-initialize if column count is off

            for row_idx, record in enumerate(history_data):
                self.ui.tableWidget_StockHistory.insertRow(row_idx)
                
                # Fetch data using .get() for safety against missing keys
                history_id = str(record.get('stk_hstry_id', 'N/A'))
                user_id = str(record.get('user_id', 'N/A'))
                username = record.get('user_acc_username', 'N/A')
                action_raw = record.get('action_type', 'N/A')
                product_name = record.get('product_name', 'N/A')
                old_qty = str(record.get('old_quantity', 'N/A'))
                new_qty = str(record.get('new_quantity', 'N/A'))
                updated_at = record.get('timestamp')
                formatted_updated_at = updated_at.strftime('%Y-%m-%d %H:%M:%S') if updated_at else "N/A"

                # Populate items and set alignment using COL_ constants
                items_to_set = [
                    (self.COL_HISTORY_ID, history_id, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft),  # Hidden
                    (self.COL_USER_ID, user_id, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter),
                    (self.COL_USERNAME, username, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft),
                    (self.COL_ACTION, action_raw, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft),
                    (self.COL_PRODUCT_NAME, product_name, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter),
                    (self.COL_OLD_QTY, old_qty, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter),
                    (self.COL_NEW_QTY, new_qty, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter),
                    (self.COL_UPDATED_AT, formatted_updated_at, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignCenter)
                ]
                for col, text, alignment in items_to_set:
                    item = QTableWidgetItem(text)
                    item.setTextAlignment(alignment)
                    self.ui.tableWidget_StockHistory.setItem(row_idx, col, item)

            self.ui.tableWidget_StockHistory.resizeColumnsToContents()
            for col, width in column_widths.items():
                if col < self.ui.tableWidget_StockHistory.columnCount():  # Ensure column exists
                    self.ui.tableWidget_StockHistory.setColumnWidth(col, width)
        except Exception as e:
            self._show_error_message(f"An error occurred while populating the table: {e}", title="Table Population Error")

    def _on_search_text_changed(self):
        """Handler for text changes that starts the debounce timer"""
        self.search_timer.start(400)  # 400ms delay after typing stops

    def filter_stock_history(self):
        """Filter the table ONLY when button/Enter is pressed"""
        try:
            search_text = self.ui.lineEdit_OWNER_QuickSearch_StockHistory.text().lower()
            for row in range(self.ui.tableWidget_StockHistory.rowCount()):
                match = False
                # Search only in visible columns (skip hidden history_id column)
                for col in range(self.COL_USER_ID, self.ui.tableWidget_StockHistory.columnCount()):
                    item = self.ui.tableWidget_StockHistory.item(row, col)
                    if item and search_text in item.text().lower():
                        match = True
                        break
                self.ui.tableWidget_StockHistory.setRowHidden(row, not match)
        except Exception as e:
            self._show_error_message(f"Search error: {str(e)}", title="Search Error")

    def log_stock_action(self, product_spec_id: int, product_id: int, old_quantity: int,
                         new_quantity: int, action_type: str, product_name: str, user_acc_id: int) -> bool:
        """
        Logs a stock action into the history.
        Args:
            product_spec_id: The ID of the product specification.
            product_id: The ID of the product.
            old_quantity: The stock quantity before the action.
            new_quantity: The stock quantity after the action.
            action_type: The type of action (e.g., "ADD", "SALE", "ADJUSTMENT", "DELETE").
            product_name: The name of the product.
            user_acc_id: The ID of the user performing the action.
        Returns:
            True if the action was logged successfully, False otherwise.
        """
        if self.history_model is None:
            print("WARNING: Cannot log stock action - history model not initialized.")
            return False
        try:
            # Convert quantities to integers safely
            old_qty = int(old_quantity) if isinstance(old_quantity, (int, str)) and str(old_quantity).isdigit() else 0
            new_qty = int(new_quantity) if isinstance(new_quantity, (int, str)) and str(new_quantity).isdigit() else 0
            
            success = self.history_model.add_history_entry(
                product_id=product_id, # Ensure this is the actual product_id
                shop_id=self.current_user_shop_id,  # Use the controller's shop ID
                user_acc_id=user_acc_id,  # Pass the user_acc_id received by the function
                product_spec_id=product_spec_id, # Pass the product_spec_id
                product_name=product_name, # Pass the actual product name
                stk_hstry_old_stock_qty=old_qty,
                stk_hstry_new_stock_qty=new_qty,
                stk_hstry_action=action_type.upper(),  # Ensure action type is uppercase for consistency
            )
            if success:
                print(f"Successfully logged {action_type} action for product {product_id} ({product_name}).")
                # Reload history to show the new entry immediately
                self.load_stock_history()
                return success
        except Exception as e:
            print(f"Error logging action: {str(e)}")
            self._show_error_message(f"Failed to log stock action: {e}", title="Log Action Error")
        return False # Return False in case of any exception

    def delete_selected_history(self):
        """Handle deletion of selected stock history record"""
        try:
            selected_items = self.ui.tableWidget_StockHistory.selectedItems()
            if not selected_items:
                QMessageBox.warning(
                    self.history_widget,
                    "No Selection",
                    "Please select a history record to delete first by clicking on a row."
                )
                return
            selected_row = self.ui.tableWidget_StockHistory.currentRow()
            # Get the history ID from the HIDDEN first column (COL_HISTORY_ID)
            history_id_item = self.ui.tableWidget_StockHistory.item(selected_row, self.COL_HISTORY_ID)
            if not history_id_item:
                self._show_error_message("Could not retrieve the ID of the selected history record. Table data might be inconsistent.", title="Deletion Error")
                return
            history_id = int(history_id_item.text())
            # Confirm deletion
            reply = QMessageBox.question(
                self.history_widget,
                "Confirm Deletion",
                "Are you sure you want to delete this history record? This action cannot be undone.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if self.history_model.delete_history_entry(history_id):
                    QMessageBox.information(self.history_widget, "Success", "History record deleted successfully.")
                    self.load_stock_history()  # Refresh the table
                else:
                    self._show_error_message("Failed to delete history record due to a database error.", title="Deletion Error")
        except ValueError:
            self._show_error_message("Invalid history ID found for deletion. Please select a valid row.", title="Deletion Error")
        except Exception as e:
            self._show_error_message(f"An unexpected error occurred during deletion: {e}", title="Deletion Error")

    def delete_all_stock_history(self):
        """Simple version without processing dialog"""
        # Check if table is empty
        if self.ui.tableWidget_StockHistory.rowCount() == 0:
            QMessageBox.information(
                self.history_widget,
                "No Records",
                "The stock history table is already empty."
            )
            return
        # Confirm with user
        reply = QMessageBox.question(
            self.history_widget,
            "Confirm Delete All",
            "Are you sure you want to delete ALL stock history records?\nThis action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                # Perform deletion
                success = self.history_model.delete_all_history_entries(
                    shop_id=self.current_user_shop_id
                )
                if success:
                    QMessageBox.information(
                        self.history_widget,
                        "Success",
                        "All stock history records have been deleted successfully."
                    )
                    self.load_stock_history()  # Refresh table
                else:
                    self._show_error_message("Failed to delete all history records.")
            except Exception as e:
                self._show_error_message(f"Error during deletion: {str(e)}")
        else:
            # User canceled - just refresh
            self.load_stock_history()

    def _show_error_message(self, message: str, title: str = "Error"):
        """Helper to show error messages using QMessageBox"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        # Determine the parent for the QMessageBox to ensure it's displayed correctly
        if self.history_widget and self.history_widget.isVisible():
            msg.setParent(self.history_widget)
        elif self.parent:
            msg.setParent(self.parent)
        # If no suitable parent, it will be displayed as a top-level window by default
        msg.exec_()

    # Additional methods for stock history functionality
    def _setup_stock_history_ui(self):
        """Setup stock history UI components"""
        try:
            self._setup_stock_history_filters()
            self._setup_stock_history_search()
            self._setup_stock_history_date_range()
        except Exception as e:
            self._show_error_message(f"Error setting up stock history UI: {e}")

    def _setup_stock_history_filters(self):
        """Setup filter controls for stock history"""
        try:
            # Setup filter dropdowns and controls
            if hasattr(self.ui, 'comboBox_StockHistory_Filter_Type'):
                self.ui.comboBox_StockHistory_Filter_Type.addItems([
                    'All Changes', 'Stock In', 'Stock Out', 'Adjustment', 'Sale', 'Return'
                ])
            
            if hasattr(self.ui, 'comboBox_StockHistory_Filter_Product'):
                self._populate_product_filter()
                
        except Exception as e:
            print(f"Error setting up stock history filters: {e}")

    def _setup_stock_history_search(self):
        """Setup search functionality for stock history"""
        try:
            # Connect search functionality
            if hasattr(self.ui, 'lineEdit_StockHistory_Search'):
                self.ui.lineEdit_StockHistory_Search.textChanged.connect(self.filter_stock_history)
                
        except Exception as e:
            print(f"Error setting up stock history search: {e}")

    def _setup_stock_history_date_range(self):
        """Setup date range picker for stock history"""
        try:
            # Setup date range controls
            if hasattr(self.ui, 'dateEdit_StockHistory_From'):
                self.ui.dateEdit_StockHistory_From.setDate(QtCore.QDate.currentDate().addDays(-30))
            
            if hasattr(self.ui, 'dateEdit_StockHistory_To'):
                self.ui.dateEdit_StockHistory_To.setDate(QtCore.QDate.currentDate())
                
        except Exception as e:
            print(f"Error setting up stock history date range: {e}")

    def _setup_stock_history_tables(self):
        """Setup stock history tables"""
        try:
            # Main stock history table
            if hasattr(self.ui, 'tableWidget_StockHistory'):
                table = self.ui.tableWidget_StockHistory
                table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                table.itemSelectionChanged.connect(self._handle_stock_history_selection)
            
            # Stock movement summary table
            if hasattr(self.ui, 'tableWidget_StockMovement_Summary'):
                table = self.ui.tableWidget_StockMovement_Summary
                table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
                table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
                table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
                
        except Exception as e:
            self._show_error_message(f"Error setting up stock history tables: {e}")

    def _handle_stock_history_selection(self):
        """Handle stock history table selection"""
        try:
            if hasattr(self.ui, 'tableWidget_StockHistory'):
                table = self.ui.tableWidget_StockHistory
                selected_items = table.selectedItems()
                
                if selected_items:
                    # Assuming History ID is in COL_HISTORY_ID
                    history_id_item = table.item(selected_items[0].row(), self.COL_HISTORY_ID)
                    if history_id_item:
                        history_id = int(history_id_item.text())
                        self.current_selected_history = self.history_model.get_stock_history_by_id(history_id)
                        
                        if self.current_selected_history:
                            self._display_stock_history_details(self.current_selected_history)
                        
        except Exception as e:
            print(f"Error handling stock history selection: {e}")
            self.current_selected_history = None

    def _display_stock_history_details(self, history_data):
        """Display detailed information about selected stock history entry"""
        try:
            # Update detail display widgets with history information
            # Note: The keys might need to be adjusted based on the actual dictionary returned by your model's get_stock_history_by_id
            if hasattr(self.ui, 'label_StockHistory_Detail_Product'):
                self.ui.label_StockHistory_Detail_Product.setText(history_data.get('product_name', ''))
            
            if hasattr(self.ui, 'label_StockHistory_Detail_ChangeType'):
                self.ui.label_StockHistory_Detail_ChangeType.setText(history_data.get('action_type', '')) # Using 'action_type' from model
            
            if hasattr(self.ui, 'label_StockHistory_Detail_Quantity'):
                # Display difference or new quantity, depending on what you want to show
                old_qty = history_data.get('old_quantity', 0)
                new_qty = history_data.get('new_quantity', 0)
                change = new_qty - old_qty
                self.ui.label_StockHistory_Detail_Quantity.setText(str(change))
            
            if hasattr(self.ui, 'label_StockHistory_Detail_Reason'):
                # Assuming 'other' or a similar field might contain a reason. Adjust if your model has a specific reason field.
                self.ui.label_StockHistory_Detail_Reason.setText(history_data.get('other', ''))
            
            if hasattr(self.ui, 'label_StockHistory_Detail_User'):
                self.ui.label_StockHistory_Detail_User.setText(history_data.get('user_acc_username', ''))
            
            if hasattr(self.ui, 'label_StockHistory_Detail_Timestamp'):
                timestamp = history_data.get('timestamp')
                formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"
                self.ui.label_StockHistory_Detail_Timestamp.setText(formatted_timestamp)
                
        except Exception as e:
            print(f"Error displaying stock history details: {e}")

    def connect_stock_history_buttons(self):
        """Connect stock history related buttons"""
        try:
            # Refresh button
            if hasattr(self.ui, 'pushButton_StockHistory_Refresh'):
                self.ui.pushButton_StockHistory_Refresh.clicked.connect(self.refresh_stock_history)
            
            # Export button
            if hasattr(self.ui, 'pushButton_StockHistory_Export'):
                self.ui.pushButton_StockHistory_Export.clicked.connect(self.export_stock_history)
            
            # Filter apply button
            if hasattr(self.ui, 'pushButton_StockHistory_Apply_Filter'):
                self.ui.pushButton_StockHistory_Apply_Filter.clicked.connect(self.apply_stock_history_filters)
            
            # Clear filter button
            if hasattr(self.ui, 'pushButton_StockHistory_Clear_Filter'):
                self.ui.pushButton_StockHistory_Clear_Filter.clicked.connect(self.clear_stock_history_filters)
            
            # Add stock adjustment button
            if hasattr(self.ui, 'pushButton_StockHistory_Add_Adjustment'):
                self.ui.pushButton_StockHistory_Add_Adjustment.clicked.connect(self.add_stock_adjustment)
                
        except Exception as e:
            self._show_error_message(f"Error connecting stock history buttons: {e}")

    def load_stock_history_data(self):
        """Load stock history data into tables"""
        try:
            # Load main stock history
            history_data = self.history_model.get_stock_history(shop_id=self.current_user_shop_id)
            self._populate_history_table(history_data) # Re-using existing populate method
            
            # Load stock movement summary
            self._load_stock_movement_summary()
            
        except Exception as e:
            self._show_error_message(f"Error loading stock history data: {e}")

    # No need for a separate _load_stock_history_table; _populate_history_table is sufficient
    # def _load_stock_history_table(self, history_data):
    #     """Load stock history data into the main table"""
    #     ... (already handled by _populate_history_table)

    def _load_stock_movement_summary(self):
        """Load stock movement summary data"""
        try:
            if not hasattr(self.ui, 'tableWidget_StockMovement_Summary'):
                return
                
            # Get summary data from model
            summary_data = self.history_model.get_stock_movement_summary(self.current_user_shop_id)
            
            table = self.ui.tableWidget_StockMovement_Summary
            table.setRowCount(0)
            
            if not summary_data:
                return
            
            # Set up summary table headers
            headers = ["Product Name", "Total In", "Total Out", "Net Change", "Current Stock"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            
            # Populate summary table
            table.setRowCount(len(summary_data))
            for row, summary in enumerate(summary_data):
                table.setItem(row, 0, QTableWidgetItem(str(summary.get('product_name', ''))))
                table.setItem(row, 1, QTableWidgetItem(str(summary.get('total_in', 0))))
                table.setItem(row, 2, QTableWidgetItem(str(summary.get('total_out', 0))))
                table.setItem(row, 3, QTableWidgetItem(str(summary.get('net_change', 0))))
                table.setItem(row, 4, QTableWidgetItem(str(summary.get('current_stock', 0))))
            
            table.resizeColumnsToContents()
            
        except Exception as e:
            print(f"Error loading stock movement summary: {e}")

    def _populate_product_filter(self):
        """Populate product filter dropdown"""
        try:
            if not hasattr(self.ui, 'comboBox_StockHistory_Filter_Product'):
                return
                
            # Get all products for filter from history model (which might use inventory model)
            products = self.history_model.get_all_products_for_filter(self.current_user_shop_id)
            
            combo = self.ui.comboBox_StockHistory_Filter_Product
            combo.clear()
            combo.addItem("All Products", None)
            
            for product in products:
                combo.addItem(product['product_name'], product['product_id'])
                
        except Exception as e:
            print(f"Error populating product filter: {e}")

    def apply_stock_history_filters(self):
        """Apply selected filters to stock history data"""
        try:
            # Get filter values
            change_type_filter = None
            product_filter_id = None
            date_from = None
            date_to = None
            
            if hasattr(self.ui, 'comboBox_StockHistory_Filter_Type'):
                type_text = self.ui.comboBox_StockHistory_Filter_Type.currentText()
                if type_text != "All Changes":
                    change_type_filter = type_text
            
            if hasattr(self.ui, 'comboBox_StockHistory_Filter_Product'):
                product_filter_id = self.ui.comboBox_StockHistory_Filter_Product.currentData()
            
            if hasattr(self.ui, 'dateEdit_StockHistory_From'):
                date_from = self.ui.dateEdit_StockHistory_From.date().toPyDate()
            
            if hasattr(self.ui, 'dateEdit_StockHistory_To'):
                date_to = self.ui.dateEdit_StockHistory_To.date().toPyDate()
            
            # Apply filters
            filtered_data = self.history_model.get_filtered_stock_history(
                shop_id=self.current_user_shop_id,
                action_type=change_type_filter, # Changed from change_type to action_type for consistency with model
                product_id=product_filter_id,
                start_date=date_from, # Changed to start_date for consistency with model
                end_date=date_to # Changed to end_date for consistency with model
            )
            
            self._populate_history_table(filtered_data)
            
        except Exception as e:
            self._show_error_message(f"Error applying filters: {e}")

    def clear_stock_history_filters(self):
        """Clear all filters and reload full stock history"""
        try:
            # Reset filter controls
            if hasattr(self.ui, 'comboBox_StockHistory_Filter_Type'):
                self.ui.comboBox_StockHistory_Filter_Type.setCurrentIndex(0)
            
            if hasattr(self.ui, 'comboBox_StockHistory_Filter_Product'):
                self.ui.comboBox_StockHistory_Filter_Product.setCurrentIndex(0)
            
            if hasattr(self.ui, 'lineEdit_OWNER_QuickSearch_StockHistory'):
                self.ui.lineEdit_OWNER_QuickSearch_StockHistory.clear()
            
            # Reload full data
            self.load_stock_history()
            
        except Exception as e:
            self._show_error_message(f"Error clearing filters: {e}")

    def refresh_stock_history(self):
        """Refresh stock history data"""
        try:
            self.load_stock_history()
            QMessageBox.information(self.history_widget, "Success", "Stock history refreshed successfully!")
        except Exception as e:
            self._show_error_message(f"Error refreshing stock history: {e}")

    def export_stock_history(self):
        """Export stock history data to file"""
        try:
            # Get all history data
            history_data = self.history_model.get_stock_history(shop_id=self.current_user_shop_id)
            
            # Export logic would go here (CSV, Excel, etc.)
            # This is a placeholder implementation
            
            QMessageBox.information(self.history_widget, "Success", "Stock history exported successfully!")
        except Exception as e:
            self._show_error_message(f"Error exporting stock history: {e}")

    def add_stock_adjustment(self):
        """Add a manual stock adjustment"""
        try:
            # This would open a dialog for manual stock adjustments
            # Placeholder implementation
            QMessageBox.information(self.history_widget, "Info", "Stock adjustment feature coming soon!")
        except Exception as e:
            self._show_error_message(f"Error adding stock adjustment: {e}")

    def record_stock_change(self, product_id, change_type, quantity_change, old_quantity, new_quantity, reason=""):
        """Record a stock change in the history"""
        try:
            # You would need to get product_spec_id and product_name here
            # For simplicity, assuming product_id is enough to get spec_id and name for history model
            # This logic needs to be robust if product_id alone isn't enough to get product_spec_id
            product_info = self.database.fetch_one("SELECT prod_spec_id, product_name FROM product_specification ps JOIN product p ON ps.product_id = p.product_id WHERE p.product_id = %s", (product_id,))
            
            if product_info:
                product_spec_id = product_info['prod_spec_id']
                product_name = product_info['product_name']
            else:
                product_spec_id = None # Handle case where product_spec_id cannot be found
                product_name = "Unknown Product"
                print(f"WARNING: Could not find product_spec_id or product_name for product_id: {product_id}")

            return self.log_stock_action(
                product_spec_id=product_spec_id,
                product_id=product_id,
                old_quantity=old_quantity,
                new_quantity=new_quantity,
                action_type=change_type,
                product_name=product_name,
                user_acc_id=self.current_user_id
            )
        except Exception as e:
            print(f"Error recording stock change: {e}")
            return False

    def get_product_stock_history(self, product_id):
        """Get stock history for a specific product"""
        try:
            return self.history_model.get_stock_history(product_id=product_id, shop_id=self.current_user_shop_id)
        except Exception as e:
            print(f"Error getting product stock history: {e}")
            return []

    def get_low_stock_warning(self):
        """Get low stock warning information for display"""
        try:
            return self.history_model.get_low_stock_products(self.current_user_shop_id)
        except Exception as e:
            print(f"Error getting low stock warning: {e}")
            return []

    def update_low_stock_warning(self):
        """Update low stock warning display"""
        try:
            low_stock_items = self.get_low_stock_warning()
            
            # Update UI elements with low stock information
            if hasattr(self.ui, 'label_LowStockWarning'):
                if low_stock_items:
                    warning_text = f"Warning: {len(low_stock_items)} items are low in stock!"
                    self.ui.label_LowStockWarning.setText(warning_text)
                    self.ui.label_LowStockWarning.setStyleSheet("color: red; font-weight: bold;")
                else:
                    self.ui.label_LowStockWarning.setText("All items are well stocked")
                    self.ui.label_LowStockWarning.setStyleSheet("color: green; font-weight: bold;")
                    
        except Exception as e:
            print(f"Error updating low stock warning: {e}")