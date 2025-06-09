import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from database import Database  # Assuming 'database' is in the root directory
from core.models.OInventory_pageModel import InventoryModel

class InventoryPageController:
    COL_PRODUCT_ID = 0
    COL_PROD_TYPE_NAME = 1
    COL_PRODUCT_NAME = 2
    COL_PRODUCT_PRICE = 3
    COL_STOCK_QTY = 4
    COL_COLOR = 5
    COL_LENGTH_MM = 6
    COL_THICKNESS_MM = 7
    COL_WIDTH_MM = 8
    COL_OTHER = 9
    COL_PRODUCT_SOURCE = 10
    COL_CREATED_AT = 11
    COL_UPDATED_AT = 12
  
    def __init__(self, inventory_ui, inventory_widget, database, # ADD 'database' parameter here
                 current_user_shop_id=None, current_user_id=None, current_username=None, 
                 inventory_data=None, parent=None):
        self.ui = inventory_ui
        self.inventory_data = inventory_data or {}
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
        self.inventory_widget = inventory_widget
        self.parent = parent
        self.database = database # STORE the passed database instance here
       
        # User/Shop ID initialization
        # Use provided IDs or fallbacks, ensuring they are integers
        self.current_user_shop_id = int(current_user_shop_id) if current_user_shop_id is not None else 1
        self.current_user_id = int(current_user_id) if current_user_id is not None else 1
        self.current_username = current_username if current_username is not None else "admin_user"
        
        # Initialize InventoryModel ONCE with the passed database
        self.inventory_model = InventoryModel(self.database, self.current_user_shop_id, self.current_user_id)
 
        print(f"DEBUG: InventoryPageController initialized with Shop ID: {self.current_user_shop_id}, User ID: {self.current_user_id}, Username: {self.current_username}")
        
        self.current_edit_product = None
        self.current_delete_product = None 
        self._setup_button_groups()
        self._setup_tables()
        self._setup_price_validators()
        self._setup_input_validators() # Call input validators
        self.connect_inventory_buttons()
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
        self.load_all_inventory_products()
        self._setup_color_validators()
        self.update_all_source_labels()

    def perform_quick_search(self):
        """
        Performs a quick search based on the product name entered in the search line edit.
        Displays results in the ALL_ITEMS table.
        """
        search_query = self.ui.lineEdit_OWNER_QuickSearch_Inventory.text().strip()
        if not search_query:
            # If search query is empty, reload all items in the ALL_ITEMS table
            self.load_all_inventory_products()
            self._show_info_message("Displaying all items. Search query was empty.")
            return
        
        try:
            # Call a new method in your InventoryModel to search for products by name
            found_products = self.inventory_model.search_products_by_name(search_query, self.current_user_shop_id)
            if found_products:
                self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)  # Switch to ALL_ITEMS tab
                self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
                self.load_inventory_table(self.ui.tableWidget_ALL_ITEMS, found_products)
                self._show_success_message(f"Found {len(found_products)} matching products for '{search_query}'.")
            else:
                # If no products found, clear the table and show a message
                self.ui.tableWidget_ALL_ITEMS.setRowCount(0)  # Clear existing rows
                self._show_error_message(f"No products found matching '{search_query}'.")
        except Exception as e:
            self._show_error_message(f"An error occurred during search: {e}")

    def _setup_tables(self):
        """Configure all tables to be read-only with proper selection behavior"""
        tables = [
            self.ui.tableWidget_ALL_ITEMS,
            self.ui.tableWidget_ROOF,
            self.ui.tableWidget_SPANDREL,
            self.ui.tableWidget_GUTTER,
            self.ui.tableWidget_OTHER
        ]
        for table in tables:
            # Make tables read-only
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            # Connect selection changed signal
            table.itemSelectionChanged.connect(self._handle_table_selection)

    def _handle_table_selection(self):
        """Store selected product when table row is clicked"""
        try:
            # Get the current table based on which tab is active
            current_table = self._get_current_table()
            if not current_table:
                self.current_edit_product = None
                self.current_delete_product = None
                return
            selected_items = current_table.selectedItems()
            if selected_items:
                # Get product ID from first column
                product_id = selected_items[self.COL_PRODUCT_ID].text()
                product = self.inventory_model.get_product_by_id(product_id)
                self.current_edit_product = product
                self.current_delete_product = product
                current_table.selectRow(selected_items[self.COL_PRODUCT_ID].row())
                # Debug print
                if product:
                    print(f"Selected product: {product.get('product_name', 'N/A')}")
            else:
                self.current_edit_product = None
                self.current_delete_product = None
        except Exception as e:
            print(f"Error handling selection: {e}")
            self.current_edit_product = None
            self.current_delete_product = None

    def _get_current_table(self):
        """Returns the currently visible table widget"""
        index = self.ui.INVENTORY_afterBUTTONSclick.currentIndex()
        tables = [
            self.ui.tableWidget_ALL_ITEMS,
            self.ui.tableWidget_ROOF,
            self.ui.tableWidget_SPANDREL,
            self.ui.tableWidget_GUTTER,
            self.ui.tableWidget_OTHER
        ]
        # Ensure the index is within the valid range before accessing
        return tables[index] if 0 <= index < len(tables) else None

    def _setup_price_validators(self):
        """Set up validators and connections for all price input fields"""
        price_fields = [
            self.ui.lineEdit_AddROOF_Price,
            self.ui.lineEdit_AddSPANDREL_Price,
            self.ui.lineEdit_AddGUTTER_Price,
            self.ui.lineEdit_AddOTHER_Price,
            self.ui.lineEdit_EditROOF_Price,
            self.ui.lineEdit_EditSPANDREL_Price,
            self.ui.lineEdit_EditGUTTER_Price,
            self.ui.lineEdit_EditOTHER_Price
        ]
        for field in price_fields:
            # Set up validator to allow float with 2 decimal places
            validator = QtGui.QDoubleValidator(0.01, 999999.99, 2, field)
            field.setValidator(validator)

    def _setup_input_validators(self):
        """Set up simple validators for price and stock fields"""
        # Price fields (just allow numbers, no fancy formatting)
        price_fields = [
            self.ui.lineEdit_AddROOF_Price,
            self.ui.lineEdit_AddSPANDREL_Price,
            self.ui.lineEdit_AddGUTTER_Price,
            self.ui.lineEdit_AddOTHER_Price,
            self.ui.lineEdit_EditROOF_Price,
            self.ui.lineEdit_EditSPANDREL_Price,
            self.ui.lineEdit_EditGUTTER_Price,
            self.ui.lineEdit_EditOTHER_Price
        ]
        for field in price_fields:
            validator = QtGui.QDoubleValidator(0.01, 999999.99, 2, field) # Allow 2 decimal places
            field.setValidator(validator)
            field.editingFinished.connect(lambda f=field: self._add_peso_symbol(f))

        # Stock fields (minimum 11)
        stock_fields = [
            self.ui.lineEdit_AddROOF_Qty,
            self.ui.lineEdit_AddSPANDREL_Qty,
            self.ui.lineEdit_AddGUTTER_Qty,
            self.ui.lineEdit_AddOTHER_Qty,
            self.ui.lineEdit_EditROOF_Qty,
            self.ui.lineEdit_EditSPANDREL_Qty,
            self.ui.lineEdit_EditGUTTER_Qty,
            self.ui.lineEdit_EditOTHER_Qty
        ]
        for field in stock_fields:
            validator = QtGui.QIntValidator(11, 999999, field)
            field.setValidator(validator)

        # Auto-capitalize first letter for ALL other text fields
        exclude_fields = [f.objectName() for f in price_fields + stock_fields]
        # Connect to all QLineEdit fields
        for widget in self.inventory_widget.findChildren(QtWidgets.QLineEdit): # THIS WAS ALREADY FIXED
            if widget.objectName() not in exclude_fields:
                widget.editingFinished.connect(
                    lambda w=widget: self._auto_capitalize(w)
                )
        # Connect to all QTextEdit fields
        for widget in self.inventory_widget.findChildren(QtWidgets.QTextEdit): # <--- THIS IS THE NEW FIX (Line 199)
            widget.textChanged.connect(
                lambda w=widget: self._auto_capitalize(w)
            )

    def _make_capitalize_connector(self, widget):
        """Helper to create proper connection for capitalization"""
        def connector():
            text = widget.text()
            if text:
                widget.setText(text[0].upper() + text[1:])
        return connector

    def _make_textedit_capitalizer(self, widget):
        """Helper for QTextEdit capitalization"""
        def capitalizer():
            text = widget.toPlainText()
            if text:
                widget.setPlainText(text[0].upper() + text[1:])
        return capitalizer

    def _setup_color_validators(self):
        """Set validators for color fields (letters only)"""
        color_fields = [
            self.ui.lineEdit_AddROOF_Color,
            self.ui.lineEdit_AddSPANDREL_Color,
            self.ui.lineEdit_AddGUTTER_Color,
            self.ui.lineEdit_AddOTHER_Color,
            self.ui.lineEdit_EditROOF_Color,
            self.ui.lineEdit_EditSPANDREL_Color,
            self.ui.lineEdit_EditGUTTER_Color,
            self.ui.lineEdit_EditOTHER_Color
        ]
        for field in color_fields:
            # Use QRegularExpressionValidator to allow only letters and spaces
            validator = QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("^[A-Za-z ]+$"),
                field
            )
            field.setValidator(validator)

    def _add_peso_symbol(self, field):
        """Add ₱ symbol and format as currency if a valid number is entered"""
        text = field.text()
        try:
            value = float(text.replace('₱', '').replace(',', ''))
            if value > 0:
                field.setText(f'₱{value:,.2f}')
            else:
                field.setText("") # Clear if 0 or less
        except ValueError:
            # If text is not a valid number after stripping, clear it or leave as is
            if text.strip() and text != "₱": # Avoid clearing if user just typed '₱'
                self._show_error_message("Invalid price format. Please enter a number.", title="Input Error")
                field.clear() # Clear invalid input
            
    def _parse_peso(self, peso_str):
        """Convert ₱1,234.56 → 1234.56"""
        try:
            return float(str(peso_str).replace('₱','').replace(',',''))
        except (ValueError, TypeError):
            return 0.0

    def _validate_inputs(self, price_str, stock_str):
        """Super simple validation"""
        try:
            price = self._parse_peso(price_str)
            if price <= 0:
                return False, "Price must be greater than 0."
            stock = int(stock_str)
            if stock < 11:
                return False, "Stock must be 11 or more."
            return True, ""
        except ValueError:
            return False, "Please enter valid numbers for price and stock."

    def _capitalize_first_letter(self, text):
        """Capitalize ONLY the first letter of the first word (e.g., 'light blue' → 'Light blue')"""
        if not text:
            return text
        return text[0].upper() + text[1:].lower()  # Only first letter capitalized

    def _auto_capitalize(self, widget):
        """Auto-capitalize the first letter of text in a widget"""
        if hasattr(widget, 'text'):
            current_text = widget.text()
            if current_text:
                capitalized = self._capitalize_first_letter(current_text)
                if capitalized != current_text:
                    widget.setText(capitalized)
        elif hasattr(widget, 'toPlainText'):
            current_text = widget.toPlainText()
            if current_text:
                capitalized = self._capitalize_first_letter(current_text)
                if capitalized != current_text:
                    widget.setPlainText(capitalized)

    # -------------------- Utility Setup --------------------
    def _setup_button_groups(self):
        self.table_view_buttons = [
            self.ui.pushButton_Inventory_ALL_ITEMS_table,
            self.ui.pushButton_Inventory_ROOF_table,
            self.ui.pushButton_Inventory_SPANDREL_table,
            self.ui.pushButton_Inventory_GUTTER_table,
            self.ui.pushButton_Inventory_OTHER_table,
        ]
        self.action_buttons = [
            self.ui.pushButton_OWNER_Add_Inventory,
            self.ui.pushButton_OWNER_Edit_Inventory,
            self.ui.pushButton_OWNER_Delete_Inventory,
        ]

    def _show_error_message(self, message, title="Error"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(title)
        msg.setInformativeText(message)
        msg.setWindowTitle(title)
        msg.exec_()

    def _show_success_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setInformativeText(message)
        msg.setWindowTitle("Success")
        msg.exec_()

    def _show_info_message(self, message):
        QMessageBox.information(self.parent, "Info", message)

    def _reset_button_styles(self, buttons):
        for btn in buttons:
            btn.setProperty('class', '')
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def set_active_inventorytable_button(self, button):
        self._reset_button_styles(self.table_view_buttons)
        self._reset_button_styles(self.action_buttons)
        button.setProperty('class', 'activeButton')
        button.style().unpolish(button)
        button.style().polish(button)

    def set_active_inventory_updateStock_button(self, button):
        self._reset_button_styles(self.action_buttons)
        self._reset_button_styles(self.table_view_buttons)
        button.setProperty('class', 'activeActionButton')
        button.style().unpolish(button)
        button.style().polish(button)

    # -------------------- Connect Buttons --------------------
    def connect_inventory_buttons(self):
        # Table view buttons
        self.ui.pushButton_Inventory_ALL_ITEMS_table.clicked.connect(self.view_all_items_table_inventory)
        self.ui.pushButton_Inventory_ROOF_table.clicked.connect(self.view_roof_table_inventory)
        self.ui.pushButton_Inventory_SPANDREL_table.clicked.connect(self.view_spandrel_table_inventory)
        self.ui.pushButton_Inventory_GUTTER_table.clicked.connect(self.view_gutter_table_inventory)
        self.ui.pushButton_Inventory_OTHER_table.clicked.connect(self.view_other_table_inventory)
        
        # Search button
        self.ui.pushButton_SEARCHitems.clicked.connect(self.perform_quick_search)
        
        # Action buttons
        self.ui.pushButton_OWNER_Add_Inventory.clicked.connect(self.show_form_add_inventory)
        self.ui.pushButton_OWNER_Edit_Inventory.clicked.connect(self.show_form_edit_inventory)
        self.ui.pushButton_OWNER_Delete_Inventory.clicked.connect(self.show_form_delete_inventory)
        
        # Add Stock
        self.ui.comboBox_Select_Prod_Type_toAdd.currentIndexChanged.connect(self.switch_add_stock_form)
        self.ui.pushButton_Confirm_ROOFadd.clicked.connect(lambda: self.confirm_add_stock("ROOF"))
        self.ui.pushButton_Close_ROOFadd.clicked.connect(self.close_add_stock_form)
        self.ui.pushButton_Confirm_SPANDRELadd.clicked.connect(lambda: self.confirm_add_stock("SPANDREL"))
        self.ui.pushButton_Close_SPANDRELadd.clicked.connect(self.close_add_stock_form)
        self.ui.pushButton_Confirm_GUTTERadd.clicked.connect(lambda: self.confirm_add_stock("GUTTER"))
        self.ui.pushButton_Close_GUTTERadd.clicked.connect(self.close_add_stock_form)
        self.ui.pushButton_Confirm_OTHERadd.clicked.connect(lambda: self.confirm_add_stock("OTHER"))
        self.ui.pushButton_Close_OTHERadd.clicked.connect(self.close_add_stock_form)
        
        # Edit Stock
        self.ui.comboBox_Select_Prod_Type_toEdit.currentIndexChanged.connect(self.switch_edit_stock_form)
        self.ui.pushButton_Save_ROOFedit.clicked.connect(lambda: self.save_edit_stock("ROOF"))
        self.ui.pushButton_Discard_ROOFedit.clicked.connect(self.close_edit_stock_form)
        self.ui.pushButton_Save_SPANDRELedit.clicked.connect(lambda: self.save_edit_stock("SPANDREL"))
        self.ui.pushButton_Discard_SPANDRELedit.clicked.connect(self.close_edit_stock_form)
        self.ui.pushButton_Save_GUTTERedit.clicked.connect(lambda: self.save_edit_stock("GUTTER"))
        self.ui.pushButton_Discard_GUTTERedit.clicked.connect(self.close_edit_stock_form)
        self.ui.pushButton_Save_OTHERedit.clicked.connect(lambda: self.save_edit_stock("OTHER"))
        self.ui.pushButton_Discard_OTHERedit.clicked.connect(self.close_edit_stock_form)
        
        # Delete Stock
        self.ui.comboBox_Select_Prod_Type_toDelete.currentIndexChanged.connect(self.switch_delete_stock_form)
        self.ui.pushButton_Confirm_ROOFdelete.clicked.connect(lambda: self.confirm_delete_stock("ROOF"))
        self.ui.pushButton_Close_ROOFdelete.clicked.connect(self.close_delete_stock_form)
        self.ui.pushButton_Confirm_SPANDRELdelete.clicked.connect(lambda: self.confirm_delete_stock("SPANDREL"))
        self.ui.pushButton_Close_SPANDRELdelete.clicked.connect(self.close_delete_stock_form)
        self.ui.pushButton_Confirm_GUTTERdelete.clicked.connect(lambda: self.confirm_delete_stock("GUTTER"))
        self.ui.pushButton_Close_GUTTERdelete.clicked.connect(self.close_delete_stock_form)
        self.ui.pushButton_Confirm_OTHERdelete.clicked.connect(lambda: self.confirm_delete_stock("OTHER"))
        self.ui.pushButton_Close_OTHERdelete.clicked.connect(self.close_delete_stock_form)

    def load_all_inventory_products(self):
        """Load all inventory products into the ALL_ITEMS table"""
        try:
            products = self.inventory_model.get_all_products(self.current_user_shop_id)
            self.load_inventory_table(self.ui.tableWidget_ALL_ITEMS, products)
        except Exception as e:
            self._show_error_message(f"Error loading inventory products: {e}")

    def load_products_by_type(self, product_type):
        """Load products filtered by type"""
        try:
            products = self.inventory_model.get_products_by_type(product_type, self.current_user_shop_id)
            table_map = {
                "ROOF": self.ui.tableWidget_ROOF,
                "SPANDREL": self.ui.tableWidget_SPANDREL,
                "GUTTER": self.ui.tableWidget_GUTTER,
                "OTHER": self.ui.tableWidget_OTHER
            }
            if product_type in table_map:
                self.load_inventory_table(table_map[product_type], products)
        except Exception as e:
            self._show_error_message(f"Error loading {product_type} products: {e}")

    def load_inventory_table(self, table_widget, products):
        """Load products data into the specified table widget"""
        try:
            table_widget.setRowCount(0)
            if not products:
                return
            headers = [
                "Product ID", "Type", "Product Name", "Price", "Stock Qty", 
                "Color", "Length (mm)", "Thickness (mm)", "Width (mm)", 
                "Other", "Source", "Created At", "Updated At"
            ]
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.setRowCount(len(products))
            for row_idx, product in enumerate(products):
                table_widget.setItem(row_idx, self.COL_PRODUCT_ID, QTableWidgetItem(str(product.get('product_id', ''))))
                table_widget.setItem(row_idx, self.COL_PROD_TYPE_NAME, QTableWidgetItem(str(product.get('prod_type_name', ''))))
                table_widget.setItem(row_idx, self.COL_PRODUCT_NAME, QTableWidgetItem(str(product.get('product_name', ''))))
                
                # Format price
                price_value = product.get('product_price', 0.0)
                price_item = QTableWidgetItem(f"₱{float(price_value):,.2f}")
                price_item.setData(QtCore.Qt.UserRole, float(price_value))
                table_widget.setItem(row_idx, self.COL_PRODUCT_PRICE, price_item)
                
                table_widget.setItem(row_idx, self.COL_STOCK_QTY, QTableWidgetItem(str(product.get('stock_qty', ''))))
                table_widget.setItem(row_idx, self.COL_COLOR, QTableWidgetItem(str(product.get('color', ''))))
                table_widget.setItem(row_idx, self.COL_LENGTH_MM, QTableWidgetItem(str(product.get('length_mm', ''))))
                table_widget.setItem(row_idx, self.COL_THICKNESS_MM, QTableWidgetItem(str(product.get('thickness_mm', ''))))
                table_widget.setItem(row_idx, self.COL_WIDTH_MM, QTableWidgetItem(str(product.get('width_mm', ''))))
                table_widget.setItem(row_idx, self.COL_OTHER, QTableWidgetItem(str(product.get('other', ''))))
                table_widget.setItem(row_idx, self.COL_PRODUCT_SOURCE, QTableWidgetItem(str(product.get('product_source', ''))))
                table_widget.setItem(row_idx, self.COL_CREATED_AT, QTableWidgetItem(str(product.get('created_at', ''))))
                table_widget.setItem(row_idx, self.COL_UPDATED_AT, QTableWidgetItem(str(product.get('updated_at', ''))))
            table_widget.resizeColumnsToContents()
        except Exception as e:
            self._show_error_message(f"Error loading table data: {e}")

    # -------------------- Inventory Views --------------------
    def view_all_items_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
        self.current_edit_product = None
        self.load_all_inventory_products()

    def view_roof_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(1)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ROOF_table)
        self.current_edit_product = None
        self.load_products_by_type("ROOF")

    def view_spandrel_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(2)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_SPANDREL_table)
        self.current_edit_product = None
        self.load_products_by_type("SPANDREL")

    def view_gutter_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(3)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_GUTTER_table)
        self.current_edit_product = None
        self.load_products_by_type("GUTTER")

    def view_other_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(4)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_OTHER_table)
        self.current_edit_product = None
        self.load_products_by_type("OTHER")

    # -------------------- Form Display --------------------
    def show_form_add_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(5)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Add_Inventory)
        self.ui.comboBox_Select_Prod_Type_toAdd.setCurrentIndex(0)
        self.ui.Add_Select_Prod_Type.setCurrentIndex(0)
        self.ui.addStocklabel.setText("ADD STOCK")

    def show_form_edit_inventory(self):
        """Show edit form only if a product is selected"""
        if not hasattr(self, 'current_edit_product') or not self.current_edit_product:
            self._show_error_message("Please select a product from the table first!\n\n"
                                   "1. Go to any product table (All Items, Roof, etc.)\n"
                                   "2. Click on a product row to select it\n"
                                   "3. Then click Edit button")
            return
        # Ensure 'prod_type_name' is present and uppercase
        product_type = self.current_edit_product.get('prod_type_name', '').upper()
        if not product_type:
             self._show_error_message("Selected product has no product type. Cannot edit.", title="Invalid Product")
             return

        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(6)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Edit_Inventory)
        self.ui.comboBox_Select_Prod_Type_toEdit.setCurrentText(product_type) # Set combo box to selected product type
        self.populate_edit_form(self.current_edit_product, product_type)
        self.ui.editStocklabel.setText(f"EDIT {product_type} STOCK")

    def show_form_delete_inventory(self):
        """Show delete form only if a product is selected"""
        if not hasattr(self, 'current_delete_product') or not self.current_delete_product:
            self._show_error_message("Please select a product from the table first!\n\n"
                                "1. Go to any product table (All Items, Roof, etc.)\n"
                                "2. Click on a product row to select it (make sure the entire row is highlighted)\n"
                                "3. Then click the DELETE button.")
            return
        
        # Ensure 'prod_type_name' is present and uppercase
        product_type = self.current_delete_product.get('prod_type_name', '').upper()
        if not product_type:
            self._show_error_message("Selected product has no product type. Cannot delete.", title="Invalid Product")
            return

        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(7)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Delete_Inventory)
        self.ui.comboBox_Select_Prod_Type_toDelete.setCurrentText(product_type) # Set combo box to selected product type
        self.populate_delete_form(self.current_delete_product, product_type)
        self.ui.deleteStocklabel.setText(f"DELETE {product_type} STOCK")

    def update_all_source_labels(self):
        """Update all source labels with current user information"""
        # The source is a fixed string, not dynamic per type based on your model's get_product_source_by_type
        source = "J&J FACTORY-MOALBOAL" 
        
        # Update Add Inventory labels
        if hasattr(self.ui, 'label_AddProduct_SourceValue'):
            self.ui.label_AddProduct_SourceValue.setText(source)
        if hasattr(self.ui, 'label_AddProduct_SourceValue2'):
            self.ui.label_AddProduct_SourceValue2.setText(source)
        if hasattr(self.ui, 'label_AddProduct_SourceValue3'):
            self.ui.label_AddProduct_SourceValue3.setText(source)
        if hasattr(self.ui, 'label_AddProduct_SourceValue4'):
            self.ui.label_AddProduct_SourceValue4.setText(source)
        
        # Update Edit Inventory labels
        if hasattr(self.ui, 'label_EditProduct_SourceValue'):
            self.ui.label_EditProduct_SourceValue.setText(source)
        if hasattr(self.ui, 'label_EditProduct_SourceValue2'):
            self.ui.label_EditProduct_SourceValue2.setText(source)
        if hasattr(self.ui, 'label_EditProduct_SourceValue3'):
            self.ui.label_EditProduct_SourceValue3.setText(source)
        if hasattr(self.ui, 'label_EditProduct_SourceValue4'):
            self.ui.label_EditProduct_SourceValue4.setText(source)

    # -------------------- Add --------------------
    def switch_add_stock_form(self, index):
        mapping = {
            "ROOF": (1, "ADD ROOF STOCK"),
            "SPANDREL": (2, "ADD SPANDREL STOCK"),
            "GUTTER": (3, "ADD GUTTER STOCK"),
            "OTHER": (4, "ADD OTHER STOCK")
        }
        text = self.ui.comboBox_Select_Prod_Type_toAdd.currentText().upper()
        idx, label = mapping.get(text, (0, "ADD STOCK"))
        self.ui.Add_Select_Prod_Type.setCurrentIndex(idx)
        self.ui.addStocklabel.setText(label)

    def confirm_add_stock(self, product_type):
        try:
            # Prepare data based on product_type
            product_name = ""
            product_price = ""
            prod_spec_other = ""
            prod_spec_stock_qty = ""
            prod_spec_length_mm = ""
            prod_spec_thickness_mm = ""
            prod_spec_color = ""
            prod_spec_width_mm = ""

            if product_type == "ROOF":
                product_name = self.ui.lineEdit_AddROOF_Name.text().strip()
                product_price = self.ui.lineEdit_AddROOF_Price.text()
                prod_spec_other = self.ui.lineEdit_AddROOF_OtherSpecifications.text().strip()
                prod_spec_stock_qty = self.ui.lineEdit_AddROOF_Qty.text().strip()
                prod_spec_length_mm = self.ui.lineEdit_AddROOF_Length.text().strip()
                prod_spec_thickness_mm = self.ui.lineEdit_AddROOF_Thickness.text().strip()
                prod_spec_color = self.ui.lineEdit_AddROOF_Color.text().strip()
                prod_spec_width_mm = self.ui.lineEdit_AddROOF_Width.text().strip()
            elif product_type == "SPANDREL":
                product_name = self.ui.lineEdit_AddSPANDREL_Name.text().strip()
                product_price = self.ui.lineEdit_AddSPANDREL_Price.text()
                prod_spec_other = self.ui.lineEdit_AddSPANDREL_OtherSpecifications.text().strip()
                prod_spec_stock_qty = self.ui.lineEdit_AddSPANDREL_Qty.text().strip()
                prod_spec_length_mm = self.ui.lineEdit_AddSPANDREL_Length.text().strip()
                prod_spec_thickness_mm = self.ui.lineEdit_AddSPANDREL_Thickness.text().strip()
                prod_spec_color = self.ui.lineEdit_AddSPANDREL_Color.text().strip()
                prod_spec_width_mm = self.ui.lineEdit_AddSPANDREL_Width.text().strip()
            elif product_type == "GUTTER":
                product_name = self.ui.lineEdit_AddGUTTER_Name.text().strip()
                product_price = self.ui.lineEdit_AddGUTTER_Price.text()
                prod_spec_other = self.ui.lineEdit_AddGUTTER_OtherSpecifications.text().strip()
                prod_spec_stock_qty = self.ui.lineEdit_AddGUTTER_Qty.text().strip()
                prod_spec_length_mm = self.ui.lineEdit_AddGUTTER_Length.text().strip()
                prod_spec_thickness_mm = self.ui.lineEdit_AddGUTTER_Thickness.text().strip()
                prod_spec_color = self.ui.lineEdit_AddGUTTER_Color.text().strip()
                prod_spec_width_mm = self.ui.lineEdit_AddGUTTER_Width.text().strip()
            else:  # OTHER
                product_name = self.ui.lineEdit_AddOTHER_Name.text().strip()
                product_price = self.ui.lineEdit_AddOTHER_Price.text()
                prod_spec_other = self.ui.lineEdit_AddOTHER_OtherSpecifications.text().strip()
                prod_spec_stock_qty = self.ui.lineEdit_AddOTHER_Qty.text().strip()
                prod_spec_length_mm = self.ui.lineEdit_AddOTHER_Length.text().strip()
                prod_spec_thickness_mm = self.ui.lineEdit_AddOTHER_Thickness.text().strip()
                prod_spec_color = self.ui.lineEdit_AddOTHER_Color.text().strip()
                prod_spec_width_mm = self.ui.lineEdit_AddOTHER_Width.text().strip()

            # Validate essential fields minimally
            if not product_name or not product_price or not prod_spec_stock_qty:
                raise ValueError("Product Name, Price, and Stock Quantity are required.")
            
            is_valid, error_msg = self._validate_inputs(product_price, prod_spec_stock_qty)
            if not is_valid:
                self._show_error_message(error_msg)
                return

            # Convert to numbers
            price_num = self._parse_peso(product_price)
            stock_num = int(prod_spec_stock_qty)
            
            # Step 1: Get product_type_id from model
            product_type_id = self.inventory_model.get_product_type_id(product_type)
            if not product_type_id:
                raise Exception(f"Product type '{product_type}' not found in database.")

            # Step 2: Insert product and get the new product_id
            product_id = self.inventory_model.insert_product(
                shop_id=self.current_user_shop_id, # Use dynamic shop_id
                product_type_id=product_type_id,
                name=product_name,
                price=str(price_num), # Pass formatted price string if model expects string
                source="J&J FACTORY-MOALBOAL" # This seems to be a fixed source
            )
            if not product_id:
                raise Exception("Failed to insert product.")

            # Step 3: Insert specification with the returned product_id
            spec_id = self.inventory_model.insert_specification(
                shop_id=self.current_user_shop_id, # Use dynamic shop_id
                product_id=product_id,
                stock_qty=stock_num, # Pass integer
                length=float(prod_spec_length_mm) if prod_spec_length_mm else None,
                thickness=float(prod_spec_thickness_mm) if prod_spec_thickness_mm else None,
                width=float(prod_spec_width_mm) if prod_spec_width_mm else None,
                color=prod_spec_color or None,
                other=prod_spec_other or None,
            )
            if not spec_id:
                # If spec insert fails, try to roll back product insertion (though model should handle this)
                self.inventory_model.delete_product_only(product_id) # Add a method to cleanup product if spec fails
                raise Exception("Failed to insert product specification.")
            
            # Step 4: Record history for adding stock
            # product_name is already available
            self.inventory_model.stock_history_model.add_history_entry(
                product_id=product_id,
                old_stock_qty=0, # Assuming 0 old stock for new product
                new_stock_qty=stock_num,
                action_type="ADD",
                user_acc_id=self.current_user_id,
                shop_id=self.current_user_shop_id
            )

            self._show_success_message(f"{product_type} stock added successfully!")
            self.view_all_items_table_inventory()
            
        except ValueError as ve:
            self._show_error_message(str(ve))
        except Exception as e:
            self._show_error_message(f"Failed to add {product_type} stock:\n{str(e)}")

    def close_add_stock_form(self):
        """Close add form and return to main view"""
        self.view_all_items_table_inventory()

    # -------------------- Edit --------------------
    def populate_edit_form(self, product, product_type):
        """Fills the edit form with existing product data"""
        def safe_str(value):
            if value is None:
                return ""
            # Format numbers (especially prices) correctly with 2 decimal places
            if isinstance(value, (int, float)):
                if '_price' in str(product_type).lower(): # Simple check for price field values
                     return f"₱{float(value):,.2f}"
                return str(value)
            return value

        # Use the corrected key 'stock_qty' which is now mapped in the model
        # from 'prod_spec_stock_qty'
        stock_qty_val = product.get('stock_qty', '')
        price_val = product.get('product_price', 0.0)

        if product_type == "ROOF":
            self.ui.lineEdit_EditROOF_Name.setText(product.get('product_name', ''))
            self.ui.lineEdit_EditROOF_Price.setText(safe_str(price_val))
            self.ui.lineEdit_EditROOF_Qty.setText(safe_str(stock_qty_val))
            self.ui.lineEdit_EditROOF_Color.setText(safe_str(product.get('color', '')))
            self.ui.lineEdit_EditROOF_Length.setText(safe_str(product.get('length_mm', '')))
            self.ui.lineEdit_EditROOF_Thickness.setText(safe_str(product.get('thickness_mm', '')))
            self.ui.lineEdit_EditROOF_Width.setText(safe_str(product.get('width_mm', '')))
            self.ui.lineEdit_EditROOF_OtherSpecifications.setText(product.get('other', ''))
        elif product_type == "SPANDREL":
            self.ui.lineEdit_EditSPANDREL_Name.setText(product.get('product_name', ''))
            self.ui.lineEdit_EditSPANDREL_Price.setText(safe_str(price_val))
            self.ui.lineEdit_EditSPANDREL_Qty.setText(safe_str(stock_qty_val))
            self.ui.lineEdit_EditSPANDREL_Color.setText(safe_str(product.get('color', '')))
            self.ui.lineEdit_EditSPANDREL_Length.setText(safe_str(product.get('length_mm', '')))
            self.ui.lineEdit_EditSPANDREL_Thickness.setText(safe_str(product.get('thickness_mm', '')))
            self.ui.lineEdit_EditSPANDREL_Width.setText(safe_str(product.get('width_mm', '')))
            self.ui.lineEdit_EditSPANDREL_OtherSpecifications.setText(product.get('other', ''))
        elif product_type == "GUTTER":
            self.ui.lineEdit_EditGUTTER_Name.setText(product.get('product_name', ''))
            self.ui.lineEdit_EditGUTTER_Price.setText(safe_str(price_val))
            self.ui.lineEdit_EditGUTTER_Qty.setText(safe_str(stock_qty_val))
            self.ui.lineEdit_EditGUTTER_Color.setText(safe_str(product.get('color', '')))
            self.ui.lineEdit_EditGUTTER_Length.setText(safe_str(product.get('length_mm', '')))
            self.ui.lineEdit_EditGUTTER_Thickness.setText(safe_str(product.get('thickness_mm', '')))
            self.ui.lineEdit_EditGUTTER_Width.setText(safe_str(product.get('width_mm', '')))
            self.ui.lineEdit_EditGUTTER_OtherSpecifications.setText(product.get('other', ''))
        else:  # OTHER
            self.ui.lineEdit_EditOTHER_Name.setText(product.get('product_name', ''))
            self.ui.lineEdit_EditOTHER_Price.setText(safe_str(price_val))
            self.ui.lineEdit_EditOTHER_Qty.setText(safe_str(stock_qty_val))
            self.ui.lineEdit_EditOTHER_Color.setText(safe_str(product.get('color', '')))
            self.ui.lineEdit_EditOTHER_Length.setText(safe_str(product.get('length_mm', '')))
            self.ui.lineEdit_EditOTHER_Thickness.setText(safe_str(product.get('thickness_mm', '')))
            self.ui.lineEdit_EditOTHER_Width.setText(safe_str(product.get('width_mm', '')))
            self.ui.lineEdit_EditOTHER_OtherSpecifications.setText(product.get('other', ''))

    def switch_edit_stock_form(self, index):
        mapping = {
            "ROOF": (1, "EDIT ROOF STOCK"),
            "SPANDREL": (2, "EDIT SPANDREL STOCK"),
            "GUTTER": (3, "EDIT GUTTER STOCK"),
            "OTHER": (4, "EDIT OTHER STOCK")
        }
        text = self.ui.comboBox_Select_Prod_Type_toEdit.currentText().upper()
        idx, label = mapping.get(text, (0, "EDIT STOCK"))
        self.ui.Edit_Select_Prod_Type.setCurrentIndex(idx)
        self.ui.editStocklabel.setText(label)

    def save_edit_stock(self, product_type):
        try:
            if not self.current_edit_product:
                self._show_error_message("No product selected for editing.")
                return

            # Get old stock quantity for history logging
            old_stock_qty = self.current_edit_product.get('stock_qty', 0)

            # Get updated values based on product type
            product_name = ""
            product_price_str = ""
            stock_qty_str = ""
            color = ""
            length = ""
            thickness = ""
            width = ""
            other = ""

            if product_type == "ROOF":
                product_name = self.ui.lineEdit_EditROOF_Name.text().strip()
                product_price_str = self.ui.lineEdit_EditROOF_Price.text()
                stock_qty_str = self.ui.lineEdit_EditROOF_Qty.text().strip()
                color = self.ui.lineEdit_EditROOF_Color.text().strip()
                length = self.ui.lineEdit_EditROOF_Length.text().strip()
                thickness = self.ui.lineEdit_EditROOF_Thickness.text().strip()
                width = self.ui.lineEdit_EditROOF_Width.text().strip()
                other = self.ui.lineEdit_EditROOF_OtherSpecifications.text().strip()
            elif product_type == "SPANDREL":
                product_name = self.ui.lineEdit_EditSPANDREL_Name.text().strip()
                product_price_str = self.ui.lineEdit_EditSPANDREL_Price.text()
                stock_qty_str = self.ui.lineEdit_EditSPANDREL_Qty.text().strip()
                color = self.ui.lineEdit_EditSPANDREL_Color.text().strip()
                length = self.ui.lineEdit_EditSPANDREL_Length.text().strip()
                thickness = self.ui.lineEdit_EditSPANDREL_Thickness.text().strip()
                width = self.ui.lineEdit_EditSPANDREL_Width.text().strip()
                other = self.ui.lineEdit_EditSPANDREL_OtherSpecifications.text().strip()
            elif product_type == "GUTTER":
                product_name = self.ui.lineEdit_EditGUTTER_Name.text().strip()
                product_price_str = self.ui.lineEdit_EditGUTTER_Price.text()
                stock_qty_str = self.ui.lineEdit_EditGUTTER_Qty.text().strip()
                color = self.ui.lineEdit_EditGUTTER_Color.text().strip()
                length = self.ui.lineEdit_EditGUTTER_Length.text().strip()
                thickness = self.ui.lineEdit_EditGUTTER_Thickness.text().strip()
                width = self.ui.lineEdit_EditGUTTER_Width.text().strip()
                other = self.ui.lineEdit_EditGUTTER_OtherSpecifications.text().strip()
            else:  # OTHER
                product_name = self.ui.lineEdit_EditOTHER_Name.text().strip()
                product_price_str = self.ui.lineEdit_EditOTHER_Price.text()
                stock_qty_str = self.ui.lineEdit_EditOTHER_Qty.text().strip()
                color = self.ui.lineEdit_EditOTHER_Color.text().strip()
                length = self.ui.lineEdit_EditOTHER_Length.text().strip()
                thickness = self.ui.lineEdit_EditOTHER_Thickness.text().strip()
                width = self.ui.lineEdit_EditOTHER_Width.text().strip()
                other = self.ui.lineEdit_EditOTHER_OtherSpecifications.text().strip()

            # Validate inputs
            if not product_name or not product_price_str or not stock_qty_str:
                raise ValueError("Product Name, Price, and Stock Quantity are required.")
            
            is_valid, error_msg = self._validate_inputs(product_price_str, stock_qty_str)
            if not is_valid:
                self._show_error_message(error_msg)
                return

            # Convert to appropriate types for model
            product_price_num = self._parse_peso(product_price_str)
            stock_qty_num = int(stock_qty_str)
            length_num = float(length) if length else None
            thickness_num = float(thickness) if thickness else None
            width_num = float(width) if width else None

            # Update the product
            product_success = self.inventory_model.update_product(
                product_id=self.current_edit_product['product_id'],
                name=product_name,
                price=product_price_num, # Pass as float
                source=self.current_edit_product.get('product_source', 'J&J FACTORY-MOALBOAL')
            )

            # Update the specification
            spec_success = self.inventory_model.update_specification(
                product_id=self.current_edit_product['product_id'],
                stock_qty=stock_qty_num, # Pass as int
                color=color,
                length=length_num,
                thickness=thickness_num,
                width=width_num,
                other=other
            )

            if product_success and spec_success:
                # Log stock history if quantity changed
                if old_stock_qty != stock_qty_num:
                    self.inventory_model.stock_history_model.add_history_entry(
                        product_id=self.current_edit_product['product_id'],
                        old_stock_qty=old_stock_qty,
                        new_stock_qty=stock_qty_num,
                        action_type="UPDATE",
                        user_acc_id=self.current_user_id,
                        shop_id=self.current_user_shop_id
                    )
                self._show_success_message(f"{product_type} stock updated successfully!")
                self.view_all_items_table_inventory()
            else:
                self._show_error_message("Failed to update product.")
        except ValueError as ve:
            self._show_error_message(str(ve))
        except Exception as e:
            self._show_error_message(f"Failed to update {product_type} stock:\n{str(e)}")

    def close_edit_stock_form(self):
        """Close edit form and clear data"""
        # Clear all edit form fields
        self._clear_edit_form_fields()
        self.current_edit_product = None
        self.view_all_items_table_inventory()

    def _clear_edit_form_fields(self):
        """Helper to clear all edit form fields"""
        # Clear ROOF fields
        self.ui.lineEdit_EditROOF_Name.clear()
        self.ui.lineEdit_EditROOF_Price.clear()
        self.ui.lineEdit_EditROOF_Qty.clear()
        self.ui.lineEdit_EditROOF_Color.clear()
        self.ui.lineEdit_EditROOF_Length.clear()
        self.ui.lineEdit_EditROOF_Thickness.clear()
        self.ui.lineEdit_EditROOF_Width.clear()
        self.ui.lineEdit_EditROOF_OtherSpecifications.clear()
        
        # Clear SPANDREL fields
        self.ui.lineEdit_EditSPANDREL_Name.clear()
        self.ui.lineEdit_EditSPANDREL_Price.clear()
        self.ui.lineEdit_EditSPANDREL_Qty.clear()
        self.ui.lineEdit_EditSPANDREL_Color.clear()
        self.ui.lineEdit_EditSPANDREL_Length.clear()
        self.ui.lineEdit_EditSPANDREL_Thickness.clear()
        self.ui.lineEdit_EditSPANDREL_Width.clear()
        self.ui.lineEdit_EditSPANDREL_OtherSpecifications.clear()
        
        # Clear GUTTER fields
        self.ui.lineEdit_EditGUTTER_Name.clear()
        self.ui.lineEdit_EditGUTTER_Price.clear()
        self.ui.lineEdit_EditGUTTER_Qty.clear()
        self.ui.lineEdit_EditGUTTER_Color.clear()
        self.ui.lineEdit_EditGUTTER_Length.clear()
        self.ui.lineEdit_EditGUTTER_Thickness.clear()
        self.ui.lineEdit_EditGUTTER_Width.clear()
        self.ui.lineEdit_EditGUTTER_OtherSpecifications.clear()
        
        # Clear OTHER fields
        self.ui.lineEdit_EditOTHER_Name.clear()
        self.ui.lineEdit_EditOTHER_Price.clear()
        self.ui.lineEdit_EditOTHER_Qty.clear()
        self.ui.lineEdit_EditOTHER_Color.clear()
        self.ui.lineEdit_EditOTHER_Length.clear()
        self.ui.lineEdit_EditOTHER_Thickness.clear()
        self.ui.lineEdit_EditOTHER_Width.clear()
        self.ui.lineEdit_EditOTHER_OtherSpecifications.clear()
        
        # Reset form to default state
        self.ui.comboBox_Select_Prod_Type_toEdit.setCurrentIndex(0)
        self.ui.Edit_Select_Prod_Type.setCurrentIndex(0)
        self.ui.editStocklabel.setText("EDIT STOCK")

    # -------------------- Delete --------------------
    def populate_delete_form(self, product, product_type):
        """Fills the delete form with existing product data (mainly name)"""
        self._clear_delete_form_fields(product_type)
        
        if product_type == "ROOF":
            self.ui.lineEdit_DeleteROOF_Name.setText(product.get('product_name', ''))
        elif product_type == "SPANDREL":
            self.ui.lineEdit_DeleteSPANDREL_Name.setText(product.get('product_name', ''))
        elif product_type == "GUTTER":
            self.ui.lineEdit_DeleteGUTTER_Name.setText(product.get('product_name', ''))
        else:  # OTHER
            self.ui.lineEdit_DeleteOTHER_Name.setText(product.get('product_name', ''))

    def switch_delete_stock_form(self, index):
        """Switches the visible panel on the delete form based on product type"""
        mapping = {
            "ROOF": (1, "DELETE ROOF STOCK"),
            "SPANDREL": (2, "DELETE SPANDREL STOCK"),
            "GUTTER": (3, "DELETE GUTTER STOCK"),
            "OTHER": (4, "DELETE OTHER STOCK")
        }
        text = self.ui.comboBox_Select_Prod_Type_toDelete.currentText().upper()
        idx, label = mapping.get(text, (0, "DELETE STOCK"))
        self.ui.Delete_Select_Prod_Type.setCurrentIndex(idx)
        self.ui.deleteStocklabel.setText(label)
        if self.current_delete_product and self.current_delete_product.get('prod_type_name', '').upper() == text:
            self.populate_delete_form(self.current_delete_product, text)
        else:
            self._clear_delete_form_fields(text)

    def confirm_delete_stock(self, product_type):
        """Performs the actual product deletion from the database"""
        try:
            if not self.current_delete_product:
                raise ValueError("No product selected for deletion. Please select a product from the table first.")
            
            product_id_to_delete = self.current_delete_product['product_id']
            
            # Validate that the name field isn't empty
            name_field_text = ""
            if product_type == "ROOF":
                name_field_text = self.ui.lineEdit_DeleteROOF_Name.text().strip()
            elif product_type == "SPANDREL":
                name_field_text = self.ui.lineEdit_DeleteSPANDREL_Name.text().strip()
            elif product_type == "GUTTER":
                name_field_text = self.ui.lineEdit_DeleteGUTTER_Name.text().strip()
            else:  # OTHER
                name_field_text = self.ui.lineEdit_DeleteOTHER_Name.text().strip()
            
            if not name_field_text:
                raise ValueError("Product name is required to confirm deletion. Please ensure a product is selected.")

            # Display confirmation dialog
            reply = QMessageBox.question(self.inventory_widget, 'Confirm Deletion',
                                       f"Are you sure you want to permanently delete '{name_field_text}' ({product_type} stock)?\n\n"
                                       "WARNING! This action cannot be undone.",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.No:
                self._show_info_message("Deletion cancelled.")
                return
            
            # Perform deletion via model, which now includes history logging
            delete_successful, msg = self.inventory_model.delete_product_by_id(
                product_id=product_id_to_delete,
                shop_id=self.current_user_shop_id,
                user_id=self.current_user_id
            )          
            
            if delete_successful:
                self._show_success_message(f"{product_type} stock deleted successfully!")
                self.load_all_inventory_products()
                self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
                self._clear_delete_form_fields(product_type)
                self.current_delete_product = None
            else:
                self._show_error_message(f"Failed to delete product: {msg}")
                
        except ValueError as ve:
            self._show_error_message(str(ve))
        except Exception as e:
            self._show_error_message(f"Failed to delete product: {str(e)}")

    def close_delete_stock_form(self):
        """Closes the delete form and reloads the inventory table"""
        self.load_all_inventory_products()
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
        self.current_delete_product = None
        self._clear_delete_form_fields(self.ui.comboBox_Select_Prod_Type_toDelete.currentText().upper())

    def _clear_delete_form_fields(self, product_type):
        """Helper to clear input fields on the delete form"""
        if product_type == "ROOF":
            self.ui.lineEdit_DeleteROOF_Name.clear()
        elif product_type == "SPANDREL":
            self.ui.lineEdit_DeleteSPANDREL_Name.clear()
        elif product_type == "GUTTER":
            self.ui.lineEdit_DeleteGUTTER_Name.clear()
        else:  # OTHER
            self.ui.lineEdit_DeleteOTHER_Name.clear()