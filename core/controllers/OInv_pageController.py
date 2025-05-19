from PyQt5.QtWidgets import QMessageBox

class InventoryPageController:
    def __init__(self, ui):
        self.ui = ui
        # Initialize with all items table shown and ALL ITEMS button active
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
        self.connect_inventory_buttons()
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)
    
    def set_active_inventorytable_button(self, button):
        """Set the active state for inventory table view buttons"""
        # Define base style for all buttons
        base_style = """
            QPushButton {
                background-color: #ffffff;
                color: black;
                border: 1px solid #004aad; 
                padding: 10px;
                font-family: "Verdana", sans-serif; 
                text-align: center;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QPushButton:hover {
                background-color: #903929;
                color: white;
                font-weight: 700;
                border: 1px solid #903929; 
            }
        """
        
        # Reset all table view buttons
        self.ui.pushButton_Inventory_ALL_ITEMS_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_ROOF_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_SPANDREL_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_GUTTER_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_OTHER_table.setStyleSheet(base_style)
        
        # Also reset all action buttons
        base_action_style = """
            QPushButton {
                background-color: #a6a6a6;
                border-radius: 10px;
                color: black;
                padding: 2px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #c25b55;
                color: black;
            }
        """
        self.ui.pushButton_OWNER_Add_Inventory.setStyleSheet(base_action_style)
        self.ui.pushButton_OWNER_Edit_Inventory.setStyleSheet(base_action_style)
        self.ui.pushButton_OWNER_Delete_Inventory.setStyleSheet(base_action_style)
        
        # Set active button style
        active_style = """
            QPushButton {
                background-color: #903929;
                color: white;
                font-weight: 700;
                border: 1px solid #903929; 
                padding: 10px;
                font-family: "Verdana", sans-serif; 
                text-align: center;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QPushButton:hover {
                background-color: #903929;
                color: white;
                font-weight: 700;
                border: 1px solid #903929; 
            }
        """
        button.setStyleSheet(active_style)
    
    def set_active_inventory_updateStock_button(self, button):
        """Set the active state for inventory action buttons (Add/Edit/Delete)"""
        # Define base style for action buttons
        base_action_style = """
            QPushButton {
                background-color: #a6a6a6;
                border-radius: 10px;
                color: black;
                padding: 2px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #c25b55;
                color: black;
            }
        """
        
        # Reset all action buttons
        self.ui.pushButton_OWNER_Add_Inventory.setStyleSheet(base_action_style)
        self.ui.pushButton_OWNER_Edit_Inventory.setStyleSheet(base_action_style)
        self.ui.pushButton_OWNER_Delete_Inventory.setStyleSheet(base_action_style)
        
        # Also reset all table view buttons
        base_style = """
            QPushButton {
                background-color: #ffffff;
                color: black;
                border: 1px solid #004aad; 
                padding: 10px;
                font-family: "Verdana", sans-serif; 
                text-align: center;
                border-top-left-radius: 15px;
                border-top-right-radius: 15px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
            QPushButton:hover {
                background-color: #903929;
                color: white;
                font-weight: 700;
                border: 1px solid #903929; 
            }
        """
        self.ui.pushButton_Inventory_ALL_ITEMS_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_ROOF_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_SPANDREL_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_GUTTER_table.setStyleSheet(base_style)
        self.ui.pushButton_Inventory_OTHER_table.setStyleSheet(base_style)
        
        # Set active button style
        active_action_style = """
            QPushButton {
                background-color: #c25b55;
                color: black;
                border-radius: 10px;
                padding: 2px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #c25b55;
                color: black;
            }
        """
        button.setStyleSheet(active_action_style)

    # [Rest of your existing methods remain exactly the same...]
    def connect_inventory_buttons(self):
        """Connect all inventory page buttons to their handlers"""
        # Table view buttons
        self.ui.pushButton_Inventory_ALL_ITEMS_table.clicked.connect(
            self.view_all_items_table_inventory)
        
        self.ui.pushButton_Inventory_ROOF_table.clicked.connect(
            self.view_roof_table_inventory)
        
        self.ui.pushButton_Inventory_SPANDREL_table.clicked.connect(
            self.view_spandrel_table_inventory)
        
        self.ui.pushButton_Inventory_GUTTER_table.clicked.connect(
            self.view_gutter_table_inventory)
        
        self.ui.pushButton_Inventory_OTHER_table.clicked.connect(
            self.view_other_table_inventory)
        
        # Action buttons
        self.ui.pushButton_OWNER_Add_Inventory.clicked.connect(
            self.show_form_add_inventory)
        
        self.ui.pushButton_OWNER_Edit_Inventory.clicked.connect(
            self.show_form_edit_inventory)
        
        self.ui.pushButton_OWNER_Delete_Inventory.clicked.connect(
            self.show_form_delete_inventory)
        
        # Add stock form connections
        self.ui.comboBox_Select_Prod_Type_toAdd.currentIndexChanged.connect(
            self.switch_add_stock_form)
        
        self.ui.pushButton_Confirm_ROOFadd.clicked.connect(
            lambda: self.confirm_add_stock("ROOF"))
        self.ui.pushButton_Close_ROOFadd.clicked.connect(
            self.close_add_stock_form)
        
        self.ui.pushButton_Confirm_SPANDRELadd.clicked.connect(
            lambda: self.confirm_add_stock("SPANDREL"))
        self.ui.pushButton_Close_SPANDRELadd.clicked.connect(
            self.close_add_stock_form)
        
        self.ui.pushButton_Confirm_GUTTERadd.clicked.connect(
            lambda: self.confirm_add_stock("GUTTER"))
        self.ui.pushButton_Close_GUTTERadd.clicked.connect(
            self.close_add_stock_form)
        
        self.ui.pushButton_Confirm_OTHERadd.clicked.connect(
            lambda: self.confirm_add_stock("OTHER"))
        self.ui.pushButton_Close_OTHERadd.clicked.connect(
            self.close_add_stock_form)
        
        # Edit stock form connections
        self.ui.comboBox_Select_Prod_Type_toEdit.currentIndexChanged.connect(
            self.switch_edit_stock_form)
        
        self.ui.pushButton_Save_ROOFedit.clicked.connect(
            lambda: self.save_edit_stock("ROOF"))
        self.ui.pushButton_Discard_ROOFedit.clicked.connect(
            self.close_edit_stock_form)
        
        self.ui.pushButton_Save_SPANDRELedit.clicked.connect(
            lambda: self.save_edit_stock("SPANDREL"))
        self.ui.pushButton_Discard_SPANDRELedit.clicked.connect(
            self.close_edit_stock_form)
        
        self.ui.pushButton_Save_GUTTERedit.clicked.connect(
            lambda: self.save_edit_stock("GUTTER"))
        self.ui.pushButton_Discard_GUTTERedit.clicked.connect(
            self.close_edit_stock_form)        

        self.ui.pushButton_Save_OTHERedit.clicked.connect(
            lambda: self.save_edit_stock("OTHER"))
        self.ui.pushButton_Discard_OTHERedit.clicked.connect(
            self.close_edit_stock_form) 
        
        # Delete stock form connections
        self.ui.comboBox_Select_Prod_Type_toDelete.currentIndexChanged.connect(
            self.switch_delete_stock_form)
        
        self.ui.pushButton_Confirm_ROOFdelete.clicked.connect(
            lambda: self.confirm_delete_stock("ROOF"))
        self.ui.pushButton_Close_ROOFdelete.clicked.connect(
            self.close_delete_stock_form)
        
        self.ui.pushButton_Confirm_SPANDRELdelete.clicked.connect(
            lambda: self.confirm_delete_stock("SPANDREL"))
        self.ui.pushButton_Close_SPANDRELdelete.clicked.connect(
            self.close_delete_stock_form)
        
        self.ui.pushButton_Confirm_GUTTERdelete.clicked.connect(
            lambda: self.confirm_delete_stock("GUTTER"))
        self.ui.pushButton_Close_GUTTERdelete.clicked.connect(
            self.close_delete_stock_form) 

        self.ui.pushButton_Confirm_OTHERdelete.clicked.connect(
            lambda: self.confirm_delete_stock("OTHER"))
        self.ui.pushButton_Close_OTHERdelete.clicked.connect(
            self.close_delete_stock_form)  

    # --------------------- Inventory Table View Methods ---------------------
    
    def view_all_items_table_inventory(self):
        """Show all items inventory table view"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(0)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ALL_ITEMS_table)

    def view_roof_table_inventory(self):
        """Show roof items inventory table view"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(1)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_ROOF_table)
        
    def view_spandrel_table_inventory(self):
        """Show spandrel items inventory table view"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(2)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_SPANDREL_table)

    def view_gutter_table_inventory(self):
        """Show gutter items inventory table view"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(3)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_GUTTER_table)
        
    def view_other_table_inventory(self):
        """Show other items inventory table view"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(4)
        self.set_active_inventorytable_button(self.ui.pushButton_Inventory_OTHER_table)
        
    # --------------------- Form Display Methods ---------------------
    
    def show_form_add_inventory(self):
        """Show form to add new inventory items"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(5)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Add_Inventory) 
        # Reset ADD STOCK form to default state
        self.ui.comboBox_Select_Prod_Type_toAdd.setCurrentIndex(0)
        self.ui.Add_Select_Prod_Type.setCurrentIndex(0)
        self.ui.addStocklabel.setText("ADD STOCK")                    

    def show_form_edit_inventory(self):
        """Show form to edit existing inventory items"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(6)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Edit_Inventory)
        # Reset EDIT STOCK form to default state
        self.ui.comboBox_Select_Prod_Type_toEdit.setCurrentIndex(0)
        self.ui.Edit_Select_Prod_Type.setCurrentIndex(0)
        self.ui.editStocklabel.setText("EDIT STOCK")

    def show_form_delete_inventory(self):
        """Show form to delete inventory items"""
        self.ui.INVENTORY_afterBUTTONSclick.setCurrentIndex(7)
        self.set_active_inventory_updateStock_button(self.ui.pushButton_OWNER_Delete_Inventory)
        # Reset EDIT STOCK form to default state
        self.ui.comboBox_Select_Prod_Type_toDelete.setCurrentIndex(0)
        self.ui.Delete_Select_Prod_Type.setCurrentIndex(0)
        self.ui.deleteStocklabel.setText("DELETE STOCK")

    # --------------------- Add Stock Methods ---------------------
    
    def switch_add_stock_form(self, index):
        """Switch between different add stock forms based on product type selection"""
        selected_type = self.ui.comboBox_Select_Prod_Type_toAdd.currentText()
        
        if selected_type == "ROOF":
            self.ui.Add_Select_Prod_Type.setCurrentIndex(1)
            self.ui.addStocklabel.setText("ADD ROOF STOCK")
        elif selected_type == "SPANDREL":
            self.ui.Add_Select_Prod_Type.setCurrentIndex(2)
            self.ui.addStocklabel.setText("ADD SPANDREL STOCK")
        elif selected_type == "GUTTER":
            self.ui.Add_Select_Prod_Type.setCurrentIndex(3)
            self.ui.addStocklabel.setText("ADD GUTTER STOCK")
        elif selected_type == "OTHER":
            self.ui.Add_Select_Prod_Type.setCurrentIndex(4)
            self.ui.addStocklabel.setText("ADD OTHER STOCK")
        else:
            self.ui.Add_Select_Prod_Type.setCurrentIndex(0)
            self.ui.addStocklabel.setText("ADD STOCK")
            
    def confirm_add_stock(self, product_type):
        """Handle confirmation of adding new stock"""
        # TODO: Implement actual stock addition logic
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"{product_type} stock added successfully!")
        msg.exec_()
        
        # Return to inventory table view
        self.view_all_items_table_inventory()

    def close_add_stock_form(self):
        """Close the add stock form without saving changes"""
        self.view_all_items_table_inventory()

    # --------------------- Edit Stock Methods ---------------------
    
    def switch_edit_stock_form(self, index):
        """Switch between different edit stock forms based on product type selection"""
        selected_type = self.ui.comboBox_Select_Prod_Type_toEdit.currentText()
        
        if selected_type == "ROOF":
            self.ui.Edit_Select_Prod_Type.setCurrentIndex(1)
            self.ui.editStocklabel.setText("EDIT ROOF STOCK")
        elif selected_type == "SPANDREL":
            self.ui.Edit_Select_Prod_Type.setCurrentIndex(2)
            self.ui.editStocklabel.setText("EDIT SPANDREL STOCK")
        elif selected_type == "GUTTER":
            self.ui.Edit_Select_Prod_Type.setCurrentIndex(3)
            self.ui.editStocklabel.setText("EDIT GUTTER STOCK")
        elif selected_type == "OTHER":
            self.ui.Edit_Select_Prod_Type.setCurrentIndex(4)
            self.ui.editStocklabel.setText("EDIT OTHER STOCK")
        else:
            self.ui.Edit_Select_Prod_Type.setCurrentIndex(0)
            self.ui.editStocklabel.setText("EDIT STOCK")
            
    def save_edit_stock(self, product_type):
        """Handle saving of edited stock information"""
        # TODO: Implement actual stock editing logic
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"{product_type} stock updated successfully!")
        msg.exec_()
        
        # Return to inventory table view
        self.view_all_items_table_inventory()

    def close_edit_stock_form(self):
        """Close the edit stock form without saving changes"""
        self.view_all_items_table_inventory()
        
    # --------------------- Delete Stock Methods ---------------------
    
    def switch_delete_stock_form(self, index):
        """Switch between different delete stock forms based on product type selection"""
        selected_type = self.ui.comboBox_Select_Prod_Type_toDelete.currentText()
        
        if selected_type == "ROOF":
            self.ui.Delete_Select_Prod_Type.setCurrentIndex(1)
            self.ui.deleteStocklabel.setText("DELETE ROOF STOCK")
        elif selected_type == "SPANDREL":
            self.ui.Delete_Select_Prod_Type.setCurrentIndex(2)
            self.ui.deleteStocklabel.setText("DELETE SPANDREL STOCK")
        elif selected_type == "GUTTER":
            self.ui.Delete_Select_Prod_Type.setCurrentIndex(3)
            self.ui.deleteStocklabel.setText("DELETE GUTTER STOCK")
        elif selected_type == "OTHER":
            self.ui.Delete_Select_Prod_Type.setCurrentIndex(4)
            self.ui.deleteStocklabel.setText("DELETE OTHER STOCK")
        else:
            self.ui.Delete_Select_Prod_Type.setCurrentIndex(0)
            self.ui.deleteStocklabel.setText("DELETE STOCK")
            
    def confirm_delete_stock(self, product_type):
        """Handle confirmation of deleting stock"""
        # Create confirmation dialog
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirm Deletion")
        msg.setText(f"Are you sure you want to delete this {product_type} stock?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        # Show dialog and get response
        response = msg.exec_()
        
        if response == QMessageBox.Yes:
            # TODO: Implement actual stock deletion logic
            success_msg = QMessageBox()
            success_msg.setIcon(QMessageBox.Information)
            success_msg.setWindowTitle("Success")
            success_msg.setText(f"{product_type} stock deleted successfully!")
            success_msg.exec_()
            
            # Return to inventory table view
            self.view_all_items_table_inventory()

    def close_delete_stock_form(self):
        """Close the delete stock form without deleting"""
        self.view_all_items_table_inventory()