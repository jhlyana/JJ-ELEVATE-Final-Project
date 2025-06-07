from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from database import Database
from core.models.OInventory_pageModel import InventoryModel

class InventoryPageController:
    
    COL_PRODUCT_ID = 0 # Assuming Product ID is the first column (index 0)
    COL_PROD_TYPE_NAME = 1
    COL_PRODUCT_NAME = 2
    COL_PRODUCT_PRICE = 3
    COL_STOCK_QTY = 4
    COL_UPDATED_AT = 5
    COL_COLOR = 6
    COL_LENGTH_MM = 7
    COL_THICKNESS_MM = 8
    COL_WIDTH_MM = 9
    COL_OTHER = 10
    # COL_PRODUCT_SOURCE = 10
    # COL_CREATED_AT = 11
    # COL_UPDATED_AT = 12
    
    def __init__(self, inventory_ui, inventory_data=None, parent=None):
        self.ui = inventory_ui
        self.inventory_data = inventory_data or {}
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
        self.parent = parent  # Store the parent widget reference

        self.database = Database()
        self.database.connect()
        self.inventory_model = InventoryModel(self.database)

        self.current_edit_product = None
        self.current_delete_product = None

        # Add these lines:
        self._setup_button_groups()
        self._setup_tables()
        self._setup_price_validators()  # Add price validators
        self.connect_inventory_buttons()

        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
        self.load_all_inventory_products()

        self._setup_color_validators()  # Add this line

        self.update_all_source_labels() # This will set all source labels to the default "J&J FACTORY-MOALBOAL"
    
    def perform_quick_search(self):
        """
        Performs a quick search based on the product name entered in the search line edit.
        Displays results in the ALL_ITEMS table.
        """
        search_query = self.ui.lineEdit_OWNER_QuickSearch_Inventory.text().strip()

        if not search_query:
            # If search query is empty, reload all items in the ALL_ITEMS table
            self.load_all_inventory_products()
            self._show_success_message("Displaying all items. Search query was empty.")
            return

        try:
            # Call a new method in your InventoryModel to search for products by name
            # You will need to implement inventory_model.search_products_by_name
            found_products = self.inventory_model.search_products_by_name(search_query)

            if found_products:
                self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0) # Switch to ALL_ITEMS tab
                self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
                self.load_inventory_table(self.ui.tableWidget_ALL_ITEMS, found_products)
                self._show_success_message(f"Found {len(found_products)} matching products for '{search_query}'.")
            else:
                # If no products found, clear the table and show a message
                self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0) # Switch to ALL_ITEMS tab
                self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
                self.ui.tableWidget_ALL_ITEMS.setRowCount(0) # Clear existing rows
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
                return
                
            selected_items = current_table.selectedItems()
            if selected_items:
                # Get product ID from first column
                product_id = selected_items[0].text()
                self.current_edit_product = self.inventory_model.get_product_by_id(product_id)
                current_table.selectRow(selected_items[0].row())
                
                # Debug print
                if self.current_edit_product:
                    print(f"Selected product: {self.current_edit_product['product_name']}")
        except Exception as e:
            print(f"Error handling selection: {e}")
            self.current_edit_product = None
    

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
            # Set up validator
            validator = QtGui.QDoubleValidator(0, 999999, 2, field)
            validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
            field.setValidator(validator)
            
            # Connect textChanged signal with lambda to pass the field
            # Connect textChanged signal with lambda to pass the field
            # Add focusOut event to validate when leaving field
    
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
            validator = QtGui.QDoubleValidator(0.01, 999999, 2, field)
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
        for widget in self.ui.findChildren(QtWidgets.QLineEdit):
            if widget.objectName() not in exclude_fields:
                widget.editingFinished.connect(
                    lambda w=widget: self._auto_capitalize(w)
                )
            
            # Connect to all QTextEdit fields
        for widget in self.ui.findChildren(QtWidgets.QTextEdit):
            widget.textChanged.connect(
                lambda w=widget: self._auto_capitalize(w)
            )
        
        # Auto-capitalize first letter for ALL other text fields
        exclude_fields = [f.objectName() for f in price_fields + stock_fields]
        
        # Connect to all QLineEdit fields
        for widget in self.ui.findChildren(QtWidgets.QLineEdit):
            if widget.objectName() not in exclude_fields:
                widget.editingFinished.connect(
                    lambda w=widget: self._auto_capitalize(w)
                )
        
        # Connect to all QTextEdit fields
        for widget in self.ui.findChildren(QtWidgets.QTextEdit):
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
            # Use QRegularExpressionValidator to allow only letters
            validator = QtGui.QRegularExpressionValidator(
                QtCore.QRegularExpression("^[A-Za-z ]+$"),  # Allows letters and spaces
                field
            )
            field.setValidator(validator)

    def _add_peso_symbol(self, field):
        """Simply add ₱ symbol if not present"""
        text = field.text()
        if text and not text.startswith('₱'):
            field.setText(f'₱{text}')

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
                return False, "Price must be greater than 0"
            
            stock = int(stock_str)
            if stock < 11:
                return False, "Stock must be 11 or more"
                
            return True, ""
        except ValueError:
            return False, "Please enter valid numbers"
    
    def _capitalize_first_letter(self, text):
        """Capitalize ONLY the first letter of the first word (e.g., 'light blue' → 'Light blue')"""
        if not text:
            return text
        return text[0].upper() + text[1:].lower()  # Only first letter capitalized
    
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

    def _show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    def _show_success_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Success")
        msg.setInformativeText(message)
        msg.setWindowTitle("Success")
        msg.exec_()

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

        self.ui.tableWidget_ALL_ITEMS.cellClicked.connect(lambda row, col: self.prepare_delete_from_table("ALL"))
        self.ui.tableWidget_ROOF.cellClicked.connect(lambda row, col: self.prepare_delete_from_table("ROOF"))
        self.ui.tableWidget_SPANDREL.cellClicked.connect(lambda row, col: self.prepare_delete_from_table("SPANDREL"))
        self.ui.tableWidget_GUTTER.cellClicked.connect(lambda row, col: self.prepare_delete_from_table("GUTTER"))
        self.ui.tableWidget_OTHER.cellClicked.connect(lambda row, col: self.prepare_delete_from_table("OTHER"))


    # -------------------- Load Inventory --------------------

    def load_all_inventory_products(self):
        try:
            data = self.inventory_model.get_all_products()
            self.load_inventory_table(self.ui.tableWidget_ALL_ITEMS, data)
        except Exception as e:
            self._show_error_message(f"Failed to load inventory: {e}")

    def load_inventory_table(self, table_widget, data):
        table_widget.setRowCount(0)
        for row_idx, row_data in enumerate(data):
            table_widget.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                if col_idx < table_widget.columnCount():
                    # Format price column (assuming price is column 3)
                    if col_idx == 3 and value is not None:
                        item = QTableWidgetItem(f"₱{float(value):,.2f}")
                        item.setData(QtCore.Qt.UserRole, float(value))  # For sorting
                    else:
                        item = QTableWidgetItem(str(value))
                    table_widget.setItem(row_idx, col_idx, item)
                    
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
        data = self.inventory_model.get_products_by_type("ROOF")
        self.load_inventory_table(self.ui.tableWidget_ROOF, data)

    def view_spandrel_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(2)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_SPANDREL_table)
        self.current_edit_product = None
        data = self.inventory_model.get_products_by_type("SPANDREL")
        self.load_inventory_table(self.ui.tableWidget_SPANDREL, data)

    def view_gutter_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(3)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_GUTTER_table)
        self.current_edit_product = None
        data = self.inventory_model.get_products_by_type("GUTTER")
        self.load_inventory_table(self.ui.tableWidget_GUTTER, data)

    def view_other_table_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(4)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_OTHER_table)
        self.current_edit_product = None
        data = self.inventory_model.get_products_by_type("OTHER")
        self.load_inventory_table(self.ui.tableWidget_OTHER, data)

    # -------------------- Form Display --------------------
    def show_form_add_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(5)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Add_Inventory)
        self.ui.comboBox_Select_Prod_Type_toAdd.setCurrentIndex(0)
        self.ui.Add_Select_Prod_Type.setCurrentIndex(0)
        self.ui.addStocklabel.setText("ADD STOCK")
    
    def populate_edit_form(self, product, product_type):
        """Fills the edit form with existing product data"""
        if product_type == "ROOF":
            self.ui.lineEdit_EditROOF_Name.setText(product['product_name'])
            self.ui.lineEdit_EditROOF_Price.setText(f"₱{product['product_price']:,.2f}")
            self.ui.lineEdit_EditROOF_Qty.setText(str(product['stock_qty']))
            self.ui.lineEdit_EditROOF_Color.setText(product['color'] or "")
            self.ui.lineEdit_EditROOF_Length.setText(str(product['length_mm'] or ""))
            self.ui.lineEdit_EditROOF_Thickness.setText(str(product['thickness_mm'] or ""))
            self.ui.lineEdit_EditROOF_Width.setText(str(product['width_mm'] or ""))
            self.ui.lineEdit_EditROOF_OtherSpecifications.setText(product['other'] or "")
        elif product_type == "SPANDREL":
            self.ui.lineEdit_EditSPANDREL_Name.setText(product['product_name'])
            self.ui.lineEdit_EditSPANDREL_Price.setText(f"₱{product['product_price']:,.2f}")
            self.ui.lineEdit_EditSPANDREL_Qty.setText(str(product['stock_qty']))
            self.ui.lineEdit_EditSPANDREL_Color.setText(product['color'] or "")
            self.ui.lineEdit_EditSPANDREL_Length.setText(str(product['length_mm'] or ""))
            self.ui.lineEdit_EditSPANDREL_Thickness.setText(str(product['thickness_mm'] or ""))
            self.ui.lineEdit_EditSPANDREL_Width.setText(str(product['width_mm'] or ""))
            self.ui.lineEdit_EditSPANDREL_OtherSpecifications.setText(product['other'] or "")
        elif product_type == "GUTTER":
            self.ui.lineEdit_EditGUTTER_Name.setText(product['product_name'])
            self.ui.lineEdit_EditGUTTER_Price.setText(f"₱{product['product_price']:,.2f}")
            self.ui.lineEdit_EditGUTTER_Qty.setText(str(product['stock_qty']))
            self.ui.lineEdit_EditGUTTER_Color.setText(product['color'] or "")
            self.ui.lineEdit_EditGUTTER_Length.setText(str(product['length_mm'] or ""))
            self.ui.lineEdit_EditGUTTER_Thickness.setText(str(product['thickness_mm'] or ""))
            self.ui.lineEdit_EditGUTTER_Width.setText(str(product['width_mm'] or ""))
            self.ui.lineEdit_EditGUTTER_OtherSpecifications.setText(product['other'] or "")
        else:  # OTHER
            self.ui.lineEdit_EditOTHER_Name.setText(product['product_name'])
            self.ui.lineEdit_EditOTHER_Price.setText(f"₱{product['product_price']:,.2f}")
            self.ui.lineEdit_EditOTHER_Qty.setText(str(product['stock_qty']))
            self.ui.lineEdit_EditOTHER_Color.setText(product['color'] or "")
            self.ui.lineEdit_EditOTHER_Length.setText(str(product['length_mm'] or ""))
            self.ui.lineEdit_EditOTHER_Thickness.setText(str(product['thickness_mm'] or ""))
            self.ui.lineEdit_EditOTHER_Width.setText(str(product['width_mm'] or ""))
            self.ui.lineEdit_EditOTHER_OtherSpecifications.setText(product['other'] or "")

    def show_form_delete_inventory(self):
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(7)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Delete_Inventory)
        self.ui.comboBox_Select_Prod_Type_toDelete.setCurrentIndex(0)
        self.ui.Delete_Select_Prod_Type.setCurrentIndex(0)
        self.ui.deleteStocklabel.setText("DELETE STOCK")

    # -------------------- Add --------------------

    def update_all_source_labels(self):
        # Get the source string from your model. It returns a fixed value.
        source = self.inventory_model.get_product_source_by_type("") # Parameter doesn't change output

        # --- Update Add Inventory labels ---
        # These are the specific labels for the ADD form, mapped to types for clarity in your UI.
        # Verify these names against your .ui file.
        if hasattr(self.ui, 'label_AddProduct_SourceValue'):
            self.ui.label_AddProduct_SourceValue.setText(source or "N/A") # For ROOF on ADD form
        if hasattr(self.ui, 'label_AddProduct_SourceValue2'):
            self.ui.label_AddProduct_SourceValue2.setText(source or "N/A") # For SPANDREL on ADD form
        if hasattr(self.ui, 'label_AddProduct_SourceValue3'):
            self.ui.label_AddProduct_SourceValue3.setText(source or "N/A") # For GUTTER on ADD form
        if hasattr(self.ui, 'label_AddProduct_SourceValue4'):
            self.ui.label_AddProduct_SourceValue4.setText(source or "N/A") # For GUTTER on ADD form
        # Assuming label_AddProduct_SourceValue is shared for "Other" or needs its own specific label:
        # If "Other" has a dedicated label that's not label_AddProduct_SourceValue, ensure it's handled here.
        # Example if it's label_AddProduct_SourceValue4_Other:
        # if hasattr(self.ui, 'label_AddProduct_SourceValue4_Other'):
        #     self.ui.label_AddProduct_SourceValue4_Other.setText(source or "N/A")

        # --- Update Edit Inventory labels ---
        # These are the specific labels for the EDIT form.
        # Verify these names against your .ui file.
        if hasattr(self.ui, 'label_EditProduct_SourceValue'):
            self.ui.label_EditProduct_SourceValue.setText(source or "N/A") # For ROOF on EDIT form
        if hasattr(self.ui, 'label_EditProduct_SourceValue2'):
            self.ui.label_EditProduct_SourceValue2.setText(source or "N/A") # For SPANDREL on EDIT form
        if hasattr(self.ui, 'label_EditProduct_SourceValue3'):
            self.ui.label_EditProduct_SourceValue3.setText(source or "N/A") # For GUTTER on EDIT form
        if hasattr(self.ui, 'label_EditProduct_SourceValue4'):
            self.ui.label_EditProduct_SourceValue4.setText(source or "N/A") # For OTHER on EDIT form

        # This method is designed to set all source labels to the consistent default.
        # It does NOT need to be triggered by combobox changes if the source is always the same.
        # It should be called once when the UI/forms are set up.

    def _on_confirm_add_clicked(self):
        selected_product_type = self.ui.comboBox_Select_Prod_Type_toAdd.currentText().upper()
        self.confirm_add_stock(selected_product_type) # Call your existing method

    def switch_add_stock_form(self, index):
            mapping = {
                "ROOF": (1, "ADD ROOF STOCK"),
                "SPANDREL": (2, "ADD SPANDREL STOCK"),
                "GUTTER": (3, "ADD GUTTER STOCK"),
                "OTHER": (4, "ADD OTHER STOCK")
            }
            text = self.ui.comboBox_Select_Prod_Type_toAdd.currentText()
            idx, label = mapping.get(text, (0, "ADD STOCK"))
            self.ui.Add_Select_Prod_Type.setCurrentIndex(idx)
            self.ui.addStocklabel.setText(label)

    def confirm_add_stock(self, product_type):
        try:
            # Prepare data based on product_type
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

            # Step 2: Insert product and get the new product_id
            product_id = self.inventory_model.insert_product(
                shop_id= "1",  # pass actual shop id
                product_type_id=product_type_id,
                name=product_name,
                price=product_price,
                source="J&J FACTORY-MOALBOAL"
            )
            if not product_id:
                raise Exception("Failed to insert product")
            
             # Step 3: Insert specification with the returned product_id
            self.inventory_model.insert_specification(
                shop_id="1",
                product_id=product_id,
                stock_qty=prod_spec_stock_qty,
                length=prod_spec_length_mm or None,
                thickness=prod_spec_thickness_mm or None,
                width=prod_spec_width_mm or None,
                color=prod_spec_color or None,
                other=prod_spec_other or None,
            )

            self._show_success_message(f"{product_type} stock added successfully!")
            self.view_all_items_table_inventory()
        
        except ValueError as ve:
            self._show_error_message(str(ve))
        except Exception as e:
            self._show_error_message(f"Failed to add {product_type} stock:\n{str(e)}")

    # -------------------- Edit --------------------

    def prepare_edit_from_table(self, table_type):
        """Stores the selected product when clicking a table row"""
        if table_type == "ALL":
            table = self.ui.tableWidget_ALL_ITEMS
        elif table_type == "ROOF":
            table = self.ui.tableWidget_ROOF
        # Add other table types...
        
        selected_row = table.currentRow()
        if selected_row >= 0:
            # Get product ID from first column (assuming ID is column 0)
            product_id = table.item(selected_row, 0).text()
            self.current_edit_product = self.inventory_model.get_product_by_id(product_id)

    def show_form_edit_inventory(self):
        """Show edit form only if a product is selected"""
        if not hasattr(self, 'current_edit_product') or not self.current_edit_product:
            self._show_error_message("Please select a product from the table first!\n\n"
                                "1. Go to any product table (All Items, Roof, etc.)\n"
                                "2. Click on a product row to select it\n"
                                "3. Then click Edit button")
            return
        
        product_type = self.current_edit_product['prod_type_name'].upper()
        
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(6)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Edit_Inventory)
        
        self.ui.comboBox_Select_Prod_Type_toEdit.setCurrentText(product_type)

        self.populate_edit_form(self.current_edit_product, product_type)
        self.ui.editStocklabel.setText(f"EDIT {product_type} STOCK")

    def populate_edit_form(self, product, product_type):
        """Fills the edit form with existing product data"""
        if product_type == "ROOF":
            self.ui.lineEdit_EditROOF_Name.setText(product['product_name'])
            self.ui.lineEdit_EditROOF_Price.setText(str(product['product_price']))
            self.ui.lineEdit_EditROOF_Qty.setText(str(product['stock_qty']))
            self.ui.lineEdit_EditROOF_Color.setText(product['color'] or "")
            self.ui.lineEdit_EditROOF_Length.setText(str(product['length_mm'] or ""))
            self.ui.lineEdit_EditROOF_Thickness.setText(str(product['thickness_mm'] or ""))
            self.ui.lineEdit_EditROOF_Width.setText(str(product['width_mm'] or ""))
            self.ui.lineEdit_EditROOF_OtherSpecifications.setText(product['other'] or "")
        elif product_type == "SPANDREL":
            # Similar for SPANDREL
            self.ui.lineEdit_EditSPANDREL_Name.setText(product['product_name'])

    def switch_edit_stock_form(self, index):
        mapping = {
            "ROOF": (1, "EDIT ROOF STOCK"),
            "SPANDREL": (2, "EDIT SPANDREL STOCK"),
            "GUTTER": (3, "EDIT GUTTER STOCK"),
            "OTHER": (4, "EDIT OTHER STOCK")
        }
        text = self.ui.comboBox_Select_Prod_Type_toEdit.currentText()
        idx, label = mapping.get(text, (0, "EDIT STOCK"))
        self.ui.Edit_Select_Prod_Type.setCurrentIndex(idx)
        self.ui.editStocklabel.setText(label)

    def save_edit_stock(self, product_type):
        try:
            if not self.current_edit_product:
                raise ValueError("Please select a product to edit first!")
            
            # Get updated values from form
            if product_type == "ROOF":
                name = self.ui.lineEdit_EditROOF_Name.text().strip()
                price = self._parse_peso(self.ui.lineEdit_EditROOF_Price.text())
                stock_qty = self.ui.lineEdit_EditROOF_Qty.text().strip()
                color = self.ui.lineEdit_EditROOF_Color.text().strip()
                length = self.ui.lineEdit_EditROOF_Length.text().strip()
                thickness = self.ui.lineEdit_EditROOF_Thickness.text().strip()
                width = self.ui.lineEdit_EditROOF_Width.text().strip()
                other = self.ui.lineEdit_EditROOF_OtherSpecifications.text().strip()
            elif product_type == "SPANDREL":
                name = self.ui.lineEdit_EditSPANDREL_Name.text().strip()
                price = self._parse_peso(self.ui.lineEdit_EditSPANDREL_Price.text())
                stock_qty = self.ui.lineEdit_EditSPANDREL_Qty.text().strip()
                color = self.ui.lineEdit_EditSPANDREL_Color.text().strip()
                length = self.ui.lineEdit_EditSPANDREL_Length.text().strip()
                thickness = self.ui.lineEdit_EditSPANDREL_Thickness.text().strip()
                width = self.ui.lineEdit_EditSPANDREL_Width.text().strip()
                other = self.ui.lineEdit_EditSPANDREL_OtherSpecifications.text().strip()
            elif product_type == "GUTTER":
                name = self.ui.lineEdit_EditGUTTER_Name.text().strip()
                price = self._parse_peso(self.ui.lineEdit_EditGUTTER_Price.text())
                stock_qty = self.ui.lineEdit_EditGUTTER_Qty.text().strip()
                color = self.ui.lineEdit_EditGUTTER_Color.text().strip()
                length = self.ui.lineEdit_EditGUTTER_Length.text().strip()
                thickness = self.ui.lineEdit_EditGUTTER_Thickness.text().strip()
                width = self.ui.lineEdit_EditGUTTER_Width.text().strip()
                other = self.ui.lineEdit_EditGUTTER_OtherSpecifications.text().strip()
            else:  # OTHER
                name = self.ui.lineEdit_EditOTHER_Name.text().strip()
                price = self._parse_peso(self.ui.lineEdit_EditOTHER_Price.text())
                stock_qty = self.ui.lineEdit_EditOTHER_Qty.text().strip()
                color = self.ui.lineEdit_EditOTHER_Color.text().strip()
                length = self.ui.lineEdit_EditOTHER_Length.text().strip()
                thickness = self.ui.lineEdit_EditOTHER_Thickness.text().strip()
                width = self.ui.lineEdit_EditOTHER_Width.text().strip()
                other = self.ui.lineEdit_EditOTHER_OtherSpecifications.text().strip()

            if not all([name, price, stock_qty]):
                raise ValueError("Name, Price and Quantity are required!")
            
            is_valid, error_msg = self._validate_inputs(price, stock_qty)
            if not is_valid:
                self._show_error_message(error_msg)
                return

            # Convert to numbers
            price_num = self._parse_peso(price)
            stock_num = int(stock_qty)
                
                # Update product in database
            success = self.inventory_model.update_product(
                    product_id=self.current_edit_product['product_id'],
                    name=name,
                    price=price,
                    source="J&J FACTORY-MOALBOAL"  # or get from form if editable
            )
                
            if not success:
                raise Exception("Failed to update product information")
                
                # Update specification in database
            success = self.inventory_model.update_specification(
                    product_id=self.current_edit_product['product_id'],
                    stock_qty=int(stock_qty),
                    length=length or None,
                    thickness=thickness or None,
                    width=width or None,
                    color=color or None,
                    other=other or None
            )
                
            if not success:
                raise Exception("Failed to update product specifications")

            self._show_success_message(f"{product_type} product updated successfully!")
            self.close_edit_stock_form()
                
        except ValueError as ve:
            self._show_error_message(str(ve))
        except Exception as e:
            self._show_error_message(f"Failed to update product: {str(e)}")

    def close_add_stock_form(self):
        # Clear all Add Stock input fields for all product types
        # ROOF fields
        self.ui.lineEdit_AddROOF_Name.clear()
        self.ui.lineEdit_AddROOF_Price.clear()
        self.ui.lineEdit_AddROOF_OtherSpecifications.clear()
        self.ui.lineEdit_AddROOF_Qty.clear()
        self.ui.lineEdit_AddROOF_Length.clear()
        self.ui.lineEdit_AddROOF_Thickness.clear()
        self.ui.lineEdit_AddROOF_Color.clear()
        self.ui.lineEdit_AddROOF_Width.clear()

        # SPANDREL fields
        self.ui.lineEdit_AddSPANDREL_Name.clear()
        self.ui.lineEdit_AddSPANDREL_Price.clear()
        self.ui.lineEdit_AddSPANDREL_OtherSpecifications.clear()
        self.ui.lineEdit_AddSPANDREL_Qty.clear()
        self.ui.lineEdit_AddSPANDREL_Length.clear()
        self.ui.lineEdit_AddSPANDREL_Thickness.clear()
        self.ui.lineEdit_AddSPANDREL_Color.clear()
        self.ui.lineEdit_AddSPANDREL_Width.clear()

        # GUTTER fields
        self.ui.lineEdit_AddGUTTER_Name.clear()
        self.ui.lineEdit_AddGUTTER_Price.clear()
        self.ui.lineEdit_AddGUTTER_OtherSpecifications.clear()
        self.ui.lineEdit_AddGUTTER_Qty.clear()
        self.ui.lineEdit_AddGUTTER_Length.clear()
        self.ui.lineEdit_AddGUTTER_Thickness.clear()
        self.ui.lineEdit_AddGUTTER_Color.clear()
        self.ui.lineEdit_AddGUTTER_Width.clear()

        # OTHER fields
        self.ui.lineEdit_AddOTHER_Name.clear()
        self.ui.lineEdit_AddOTHER_Price.clear()
        self.ui.lineEdit_AddOTHER_OtherSpecifications.clear()
        self.ui.lineEdit_AddOTHER_Qty.clear()
        self.ui.lineEdit_AddOTHER_Length.clear()
        self.ui.lineEdit_AddOTHER_Thickness.clear()
        self.ui.lineEdit_AddOTHER_Color.clear()
        self.ui.lineEdit_AddOTHER_Width.clear()

        # Reset combo box to default
        self.ui.comboBox_Select_Prod_Type_toAdd.setCurrentIndex(0)
        self.ui.Add_Select_Prod_Type.setCurrentIndex(0)
        self.ui.addStocklabel.setText("ADD STOCK")

        # Return to main view
        self.view_all_items_table_inventory()

    def close_edit_stock_form(self):
        """Clear all edit form fields and return to main view"""
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
   
        self.current_edit_product = None
    
        # Return to main view
        self.view_all_items_table_inventory()


    # -------------------- Delete --------------------
    def prepare_delete_from_table(self, table_type):
        """Stores the selected product when clicking a table row for deletion."""
        table = None
        if table_type == "ALL":
            table = self.ui.tableWidget_ALL_ITEMS
        elif table_type == "ROOF":
            table = self.ui.tableWidget_ROOF
        elif table_type == "SPANDREL": # Add your other tables
            table = self.ui.tableWidget_SPANDREL
        elif table_type == "GUTTER":
            table = self.ui.tableWidget_GUTTER
        elif table_type == "OTHER":
            table = self.ui.tableWidget_OTHER
        # Add other table types as needed

        if table is None:
            self._show_error_message(f"Error: Table type '{table_type}' not recognized for deletion preparation.")
            return

        selected_row = table.currentRow()
        if selected_row >= 0:
            product_id = table.item(selected_row, self.COL_PRODUCT_ID).text()
            self.current_delete_product = self.inventory_model.get_product_by_id(product_id)
            if not self.current_delete_product:
                self._show_error_message(f"Could not retrieve product details for deletion ID: {product_id}")
                self.current_delete_product = None # Clear if fetch fails
        else:
            self.current_delete_product = None # No row selected

    def show_form_delete_inventory(self):
        """Show delete form only if a product is selected."""
        if not hasattr(self, 'current_delete_product') or not self.current_delete_product:
            self._show_error_message("Please select a product from the table first!\n\n"
                                     "1. Go to any product table (All Items, Roof, etc.)\n"
                                     "2. Click on a product row to select it\n"
                                     "3. Then click the DELETE button.")
            return

        product_type = self.current_delete_product['prod_type_name'].upper()

        # Switch to the delete form panel (assuming index 7 for delete form)
        # Please adjust `7` to the correct index for your DELETE form in `INVENTORY_afterBUTTONSclick`
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(7)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Delete_Inventory) # If you have this method

        # Set the product type combobox on the delete form
        self.ui.comboBox_Select_Prod_Type_toDelete.setCurrentText(product_type)
        # This will automatically trigger switch_delete_stock_form due to currentIndexChanged connection

        # Populate the name field on the delete form
        self.populate_delete_form(self.current_delete_product, product_type)
        self.ui.deleteStocklabel.setText(f"DELETE {product_type} STOCK") # Update the form label

    def populate_delete_form(self, product, product_type):
        """Fills the delete form with existing product data (mainly name)."""
        # Clear fields first
        self._clear_delete_form_fields(product_type)

        # Populate the name field (assuming there's a lineEdit for name on delete forms)
        if product_type == "ROOF":
            self.ui.lineEdit_DeleteROOF_Name.setText(product['product_name'] or "")
        elif product_type == "SPANDREL":
            self.ui.lineEdit_DeleteSPANDREL_Name.setText(product['product_name'] or "")
        elif product_type == "GUTTER":
            self.ui.lineEdit_DeleteGUTTER_Name.setText(product['product_name'] or "")
        else: # OTHER
            self.ui.lineEdit_DeleteOTHER_Name.setText(product['product_name'] or "")

        # Make sure the name field is read-only on the delete form
        # The user should not be able to edit the name when deleting
        # Example for ROOF:
        # self.ui.lineEdit_DeleteROOF_Name.setReadOnly(True)
        # You'll need to do this for all delete name fields.


    def switch_delete_stock_form(self, index):
        """Switches the visible panel on the delete form based on product type."""
        mapping = {
            "ROOF": (1, "DELETE ROOF STOCK"),
            "SPANDREL": (2, "DELETE SPANDREL STOCK"),
            "GUTTER": (3, "DELETE GUTTER STOCK"),
            "OTHER": (4, "DELETE OTHER STOCK")
        }
        text = self.ui.comboBox_Select_Prod_Type_toDelete.currentText().upper()
        idx, label = mapping.get(text, (0, "DELETE STOCK"))
        self.ui.Delete_Select_Prod_Type.setCurrentIndex(idx) # Assuming Delete_Select_Prod_Type is your QStackedWidget
        self.ui.deleteStocklabel.setText(label)

        # If the product type in the combobox changes *while* the form is open
        # and it still matches the type of the currently selected product for deletion,
        # re-populate the form to ensure consistency.
        if self.current_delete_product and self.current_delete_product['prod_type_name'].upper() == text:
            self.populate_delete_form(self.current_delete_product, text)
        else:
            # If the selected type in the combobox doesn't match the actual product to delete,
            # or if no product is selected, clear the fields.
            self._clear_delete_form_fields(text)


    def _on_confirm_delete_clicked(self):
        """Handler for the CONFIRM button on the delete form."""
        selected_product_type = self.ui.comboBox_Select_Prod_Type_toDelete.currentText().upper()
        self.confirm_delete_stock(selected_product_type)


    def confirm_delete_stock(self, product_type):
        """
        Performs the actual product deletion from the database.
        This is the method that needs the core logic for deletion.
        """
        try:
            if not self.current_delete_product:
                raise ValueError("No product selected for deletion. Please select a product from the table first.")

            product_id_to_delete = self.current_delete_product['product_id']

            # Validate that the name field isn't empty, even though it's read-only
            # This is a safety check if the user somehow clears it.
            name_field_text = ""
            if product_type == "ROOF":
                name_field_text = self.ui.lineEdit_DeleteROOF_Name.text().strip()
            elif product_type == "SPANDREL":
                name_field_text = self.ui.lineEdit_DeleteSPANDREL_Name.text().strip()
            elif product_type == "GUTTER":
                name_field_text = self.ui.lineEdit_DeleteGUTTER_Name.text().strip()
            else: # OTHER
                name_field_text = self.ui.lineEdit_DeleteOTHER_Name.text().strip()

            if not name_field_text:
                raise ValueError("Product name is required to confirm deletion. Please ensure a product is selected.")

            # Display a confirmation dialog to the user
            reply = QMessageBox.question(self.parent, 'Confirm Deletion',
                                         f"Are you sure you want to permanently delete '{name_field_text}' ({product_type} stock)?\n\n"
                                         "WARNING! This action cannot be undone.",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.No:
                self._show_info_message("Deletion cancelled.")
                return

            # --- Call your inventory_model to delete the product ---
            # Your model needs a method like `delete_product_by_id`
            delete_successful = self.inventory_model.delete_product_by_id(product_id_to_delete)

            if delete_successful:
                self._show_success_message(f"{product_type} stock deleted successfully!")
                self.load_all_inventory_products() # Refresh the main table
                self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0) # Go back to "All Items" tab
                # Assuming you have a frame for the delete form to hide
                self._clear_delete_form_fields(product_type) # Clear fields after successful deletion
                self.current_delete_product = None # Clear the stored product after deletion
            else:
                raise Exception("Failed to delete product from the database.")

        except ValueError as ve:
            self._show_error_message(str(ve))
        except Exception as e:
            self._show_error_message(f"Failed to delete product: {str(e)}")

    def close_delete_stock_form(self):
        """Closes the delete form and reloads the inventory table."""
        # This method is likely connected to your "CLOSE" button on the delete form
        self.load_all_inventory_products()
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0) # Go back to "All Items" tab
        # Clear the current product in case the user closes without deleting
        self.current_delete_product = None
        # Clear all fields on the delete form.
        self._clear_delete_form_fields(self.ui.comboBox_Select_Prod_Type_toDelete.currentText().upper())


    def _clear_delete_form_fields(self, product_type):
        """Helper to clear input fields on the delete form."""
        if product_type == "ROOF":
            self.ui.lineEdit_DeleteROOF_Name.clear()
        elif product_type == "SPANDREL":
            self.ui.lineEdit_DeleteSPANDREL_Name.clear()
        elif product_type == "GUTTER":
            self.ui.lineEdit_DeleteGUTTER_Name.clear()
        else: # OTHER
            self.ui.lineEdit_DeleteOTHER_Name.clear()


    # --- Common Helper Methods (ensure these are in your controller) ---
    def _show_error_message(self, message):
        QMessageBox.critical(self.parent, "Error", message)

    def _show_success_message(self, message):
        QMessageBox.information(self.parent, "Success", message)

    def _show_info_message(self, message): # Added for "Deletion cancelled"
        QMessageBox.information(self.parent, "Info", message)

    # ... (Your existing load_all_inventory_products, load_inventory_table,
    #      prepare_edit_from_table, show_form_edit_inventory, etc.) ...