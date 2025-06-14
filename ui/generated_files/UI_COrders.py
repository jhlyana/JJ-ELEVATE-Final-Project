# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/raw_files/UI_COrders.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CASHIER_ORDERS(object):
    def setupUi(self, CASHIER_ORDERS):
        CASHIER_ORDERS.setObjectName("CASHIER_ORDERS")
        CASHIER_ORDERS.resize(1933, 1005)
        CASHIER_ORDERS.setStyleSheet("background: white;")
        self.LeftMenuBar = QtWidgets.QFrame(CASHIER_ORDERS)
        self.LeftMenuBar.setGeometry(QtCore.QRect(0, 0, 301, 1011))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LeftMenuBar.setFont(font)
        self.LeftMenuBar.setStyleSheet("background-color: rgba(235, 224, 204, 0.47); /* #ebe0cc with 47% opacity */")
        self.LeftMenuBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LeftMenuBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.LeftMenuBar.setObjectName("LeftMenuBar")
        self.JJelevate_text_2 = QtWidgets.QLabel(self.LeftMenuBar)
        self.JJelevate_text_2.setGeometry(QtCore.QRect(60, 220, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.JJelevate_text_2.setFont(font)
        self.JJelevate_text_2.setStyleSheet("color: #12245c;\n"
"font-family: \"Arial Black\", Arial, sans-serif; \n"
"background: transparent;\n"
"font-size: 30px;")
        self.JJelevate_text_2.setScaledContents(True)
        self.JJelevate_text_2.setObjectName("JJelevate_text_2")
        self.Logo = QtWidgets.QLabel(self.LeftMenuBar)
        self.Logo.setGeometry(QtCore.QRect(30, 50, 241, 171))
        self.Logo.setStyleSheet("background: transparent;")
        self.Logo.setText("")
        self.Logo.setPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/JJLOGO.png"))
        self.Logo.setScaledContents(True)
        self.Logo.setAlignment(QtCore.Qt.AlignCenter)
        self.Logo.setObjectName("Logo")
        self.pushButton_Dashboard = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Dashboard.setGeometry(QtCore.QRect(30, 310, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_Dashboard.setFont(font)
        self.pushButton_Dashboard.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/dashboard_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Dashboard.setIcon(icon)
        self.pushButton_Dashboard.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_Dashboard.setObjectName("pushButton_Dashboard")
        self.pushButton_Order_History = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Order_History.setGeometry(QtCore.QRect(30, 470, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Order_History.setFont(font)
        self.pushButton_Order_History.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/inventory_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Order_History.setIcon(icon1)
        self.pushButton_Order_History.setIconSize(QtCore.QSize(46, 42))
        self.pushButton_Order_History.setObjectName("pushButton_Order_History")
        self.pushButton_Sales = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Sales.setGeometry(QtCore.QRect(30, 550, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Sales.setFont(font)
        self.pushButton_Sales.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/sales_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Sales.setIcon(icon2)
        self.pushButton_Sales.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_Sales.setObjectName("pushButton_Sales")
        self.pushButton_Account = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Account.setGeometry(QtCore.QRect(30, 630, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Account.setFont(font)
        self.pushButton_Account.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/account_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Account.setIcon(icon3)
        self.pushButton_Account.setIconSize(QtCore.QSize(48, 48))
        self.pushButton_Account.setObjectName("pushButton_Account")
        self.pushButton_LogOut = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_LogOut.setGeometry(QtCore.QRect(30, 890, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(87)
        self.pushButton_LogOut.setFont(font)
        self.pushButton_LogOut.setStyleSheet("QPushButton {\n"
"    background-color:#022162;\n"
"color:white;\n"
"font-weight: 700;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"font-size: 14;\n"
"text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"        background-color: rgba(2, 33, 98, 0.8);\n"
"        color: white;\n"
"    font-weight: 700;\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/WHITElogout_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_LogOut.setIcon(icon4)
        self.pushButton_LogOut.setIconSize(QtCore.QSize(38, 38))
        self.pushButton_LogOut.setObjectName("pushButton_LogOut")
        self.JJelevate_text_3 = QtWidgets.QLabel(self.LeftMenuBar)
        self.JJelevate_text_3.setGeometry(QtCore.QRect(130, 220, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.JJelevate_text_3.setFont(font)
        self.JJelevate_text_3.setStyleSheet("color: #d75413;\n"
"font-family: \"Arial Black\", Arial, sans-serif; \n"
"background: transparent;\n"
"font-size: 29px;\n"
"")
        self.JJelevate_text_3.setScaledContents(True)
        self.JJelevate_text_3.setObjectName("JJelevate_text_3")
        self.pushButton_Orders = QtWidgets.QPushButton(self.LeftMenuBar)
        self.pushButton_Orders.setGeometry(QtCore.QRect(30, 390, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat Medium")
        font.setPointSize(12)
        self.pushButton_Orders.setFont(font)
        self.pushButton_Orders.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"    border-radius: 25px;\n"
"    padding: 9px;\n"
"    text-align: left;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"QPushButton.activeButton {\n"
"    background-color:#c25b55;\n"
"    color:black;\n"
"    font-weight: 700;\n"
"}\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ui/raw_files\\../resources/images/orders_icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_Orders.setIcon(icon5)
        self.pushButton_Orders.setIconSize(QtCore.QSize(46, 42))
        self.pushButton_Orders.setObjectName("pushButton_Orders")
        self.stackedWidget = QtWidgets.QStackedWidget(CASHIER_ORDERS)
        self.stackedWidget.setGeometry(QtCore.QRect(300, 0, 1631, 1001))
        self.stackedWidget.setObjectName("stackedWidget")
        self.TakeOrder = QtWidgets.QWidget()
        self.TakeOrder.setObjectName("TakeOrder")
        self.tableWidget_ProdList = QtWidgets.QTableWidget(self.TakeOrder)
        self.tableWidget_ProdList.setGeometry(QtCore.QRect(50, 170, 1541, 551))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        self.tableWidget_ProdList.setFont(font)
        self.tableWidget_ProdList.setStyleSheet("QTableWidget {\n"
"    background-color: white;\n"
"    gridline-color: lightgray;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #003366; \n"
"    color: #ffffff;\n"
"    font-weight: bold;\n"
"padding: 3;\n"
"}\n"
"")
        self.tableWidget_ProdList.setObjectName("tableWidget_ProdList")
        self.tableWidget_ProdList.setColumnCount(11)
        self.tableWidget_ProdList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_ProdList.setHorizontalHeaderItem(10, item)
        self.tableWidget_ProdList.horizontalHeader().setDefaultSectionSize(265)
        self.frame_46 = QtWidgets.QFrame(self.TakeOrder)
        self.frame_46.setGeometry(QtCore.QRect(50, 750, 1541, 211))
        self.frame_46.setStyleSheet("\n"
"    background-color: #f6f3ee;\n"
"    border-radius: 16;\n"
"    padding: 10px;\n"
"\n"
"")
        self.frame_46.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_46.setObjectName("frame_46")
        self.label_647 = QtWidgets.QLabel(self.frame_46)
        self.label_647.setGeometry(QtCore.QRect(10, 70, 341, 61))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label_647.setFont(font)
        self.label_647.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_647.setObjectName("label_647")
        self.pushButton_Save_OTHERedit_2 = QtWidgets.QPushButton(self.frame_46)
        self.pushButton_Save_OTHERedit_2.setGeometry(QtCore.QRect(0, 0, 1541, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Save_OTHERedit_2.setFont(font)
        self.pushButton_Save_OTHERedit_2.setStyleSheet("\n"
"    background-color: rgba(141, 39, 33, 0.8);\n"
"    color: white;\n"
"    border-radius: 15px;\n"
"    border: 1px solid #000000;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"\n"
"")
        self.pushButton_Save_OTHERedit_2.setObjectName("pushButton_Save_OTHERedit_2")
        self.label_648 = QtWidgets.QLabel(self.frame_46)
        self.label_648.setGeometry(QtCore.QRect(720, 60, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label_648.setFont(font)
        self.label_648.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_648.setObjectName("label_648")
        self.OrderInput_prodnameDisplay_2 = QtWidgets.QLineEdit(self.frame_46)
        self.OrderInput_prodnameDisplay_2.setGeometry(QtCore.QRect(210, 70, 451, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.OrderInput_prodnameDisplay_2.setFont(font)
        self.OrderInput_prodnameDisplay_2.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 9px;\n"
"")
        self.OrderInput_prodnameDisplay_2.setObjectName("OrderInput_prodnameDisplay_2")
        self.OrderInput_Qty_2 = QtWidgets.QLineEdit(self.frame_46)
        self.OrderInput_Qty_2.setGeometry(QtCore.QRect(860, 70, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.OrderInput_Qty_2.setFont(font)
        self.OrderInput_Qty_2.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 9px;\n"
"")
        self.OrderInput_Qty_2.setObjectName("OrderInput_Qty_2")
        self.Add_Order_2 = QtWidgets.QPushButton(self.frame_46)
        self.Add_Order_2.setGeometry(QtCore.QRect(860, 140, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Add_Order_2.setFont(font)
        self.Add_Order_2.setStyleSheet("/* Default Inactive Button */\n"
"QPushButton {\n"
"    background-color: #003366;\n"
"    color: #fefefe;\n"
"    border-radius: 15px;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect on Inactive Buttons */\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 51, 102, 0.9); /* 90% opacity of #003366 */\n"
"}")
        self.Add_Order_2.setObjectName("Add_Order_2")
        self.label_649 = QtWidgets.QLabel(self.frame_46)
        self.label_649.setGeometry(QtCore.QRect(1070, 60, 291, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(13)
        font.setBold(False)
        font.setWeight(50)
        self.label_649.setFont(font)
        self.label_649.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_649.setObjectName("label_649")
        self.OrderInput_Discount_2 = QtWidgets.QLineEdit(self.frame_46)
        self.OrderInput_Discount_2.setGeometry(QtCore.QRect(1380, 70, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.OrderInput_Discount_2.setFont(font)
        self.OrderInput_Discount_2.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 9px;\n"
"")
        self.OrderInput_Discount_2.setObjectName("OrderInput_Discount_2")
        self.View_OrderSummary = QtWidgets.QPushButton(self.frame_46)
        self.View_OrderSummary.setGeometry(QtCore.QRect(1140, 140, 361, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.View_OrderSummary.setFont(font)
        self.View_OrderSummary.setStyleSheet("/* Default Inactive Button */\n"
"QPushButton {\n"
"    background-color: #c25b55;\n"
"    color: #fefefe;\n"
"    border-radius: 15px;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect on Inactive Buttons */\n"
"QPushButton:hover {\n"
"    background-color: rgba(194, 91, 85, 0.9); /* 90% opacity of #c25b55 */\n"
"}")
        self.View_OrderSummary.setObjectName("View_OrderSummary")
        self.frame_45 = QtWidgets.QFrame(self.TakeOrder)
        self.frame_45.setGeometry(QtCore.QRect(0, 0, 1601, 151))
        self.frame_45.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_45.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_45.setObjectName("frame_45")
        self.comboBox_filterProduct_List = QtWidgets.QComboBox(self.frame_45)
        self.comboBox_filterProduct_List.setGeometry(QtCore.QRect(1330, 50, 241, 71))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.comboBox_filterProduct_List.setFont(font)
        self.comboBox_filterProduct_List.setStyleSheet("    background-color: #ebe0cc;\n"
"    border-radius: 15px;\n"
"font-size:28px;\n"
"text-align: center;")
        self.comboBox_filterProduct_List.setObjectName("comboBox_filterProduct_List")
        self.comboBox_filterProduct_List.addItem("")
        self.comboBox_filterProduct_List.addItem("")
        self.comboBox_filterProduct_List.addItem("")
        self.comboBox_filterProduct_List.addItem("")
        self.comboBox_filterProduct_List.addItem("")
        self.comboBox_filterProduct_List.addItem("")
        self.frame_4 = QtWidgets.QFrame(self.frame_45)
        self.frame_4.setGeometry(QtCore.QRect(810, 50, 511, 71))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.lineEdit__QuicksearchProduct = QtWidgets.QLineEdit(self.frame_4)
        self.lineEdit__QuicksearchProduct.setGeometry(QtCore.QRect(10, 10, 291, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit__QuicksearchProduct.setFont(font)
        self.lineEdit__QuicksearchProduct.setStyleSheet("\n"
"    background-color: transparent;\n"
"    color: black;\n"
"    padding: 2px;\n"
"    text-align: center;\n"
"\n"
"\n"
"\n"
"")
        self.lineEdit__QuicksearchProduct.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit__QuicksearchProduct.setClearButtonEnabled(False)
        self.lineEdit__QuicksearchProduct.setObjectName("lineEdit__QuicksearchProduct")
        self.label_18 = QtWidgets.QLabel(self.frame_4)
        self.label_18.setGeometry(QtCore.QRect(10, 10, 71, 51))
        self.label_18.setStyleSheet("background: transparent;\n"
"padding: 5;\n"
"")
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("ui/raw_files\\../../../../resources/images/search.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")
        self.pushButton_searchProduct = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_searchProduct.setGeometry(QtCore.QRect(300, 10, 181, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_searchProduct.setFont(font)
        self.pushButton_searchProduct.setStyleSheet("    QPushButton {\n"
"        background-color: #003366;\n"
"        color: white;\n"
"        padding: 2px;\n"
"        text-align: center;\n"
"    }\n"
"    QPushButton:hover {\n"
"        background-color: rgba(0, 51, 102, 0.9);\n"
"    }")
        self.pushButton_searchProduct.setObjectName("pushButton_searchProduct")
        self.orderReportText = QtWidgets.QLabel(self.frame_45)
        self.orderReportText.setGeometry(QtCore.QRect(50, 50, 761, 71))
        self.orderReportText.setStyleSheet("color: #12245c;\n"
"font-family: \"Arial Black\", Arial, sans-serif; \n"
"background: transparent;\n"
"font-size: 50px;")
        self.orderReportText.setObjectName("orderReportText")
        self.stackedWidget.addWidget(self.TakeOrder)
        self.ViewOrderSummary = QtWidgets.QWidget()
        self.ViewOrderSummary.setObjectName("ViewOrderSummary")
        self.frame_47 = QtWidgets.QFrame(self.ViewOrderSummary)
        self.frame_47.setGeometry(QtCore.QRect(50, 50, 1531, 911))
        self.frame_47.setStyleSheet("\n"
"    background-color: #f6f3ee;\n"
"    border-radius: 16;\n"
"    padding: 10px;\n"
"\n"
"")
        self.frame_47.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_47.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_47.setObjectName("frame_47")
        self.pushButton_Save_OTHERedit_3 = QtWidgets.QPushButton(self.frame_47)
        self.pushButton_Save_OTHERedit_3.setGeometry(QtCore.QRect(0, 0, 1531, 51))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Save_OTHERedit_3.setFont(font)
        self.pushButton_Save_OTHERedit_3.setStyleSheet("\n"
"    background-color: #8d2721;\n"
"    color: white;\n"
"    border-radius: 15px;\n"
"    border: 1px solid #000000;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"\n"
"")
        self.pushButton_Save_OTHERedit_3.setObjectName("pushButton_Save_OTHERedit_3")
        self.label_650 = QtWidgets.QLabel(self.frame_47)
        self.label_650.setGeometry(QtCore.QRect(30, 50, 281, 81))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_650.setFont(font)
        self.label_650.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_650.setObjectName("label_650")
        self.label_651 = QtWidgets.QLabel(self.frame_47)
        self.label_651.setGeometry(QtCore.QRect(30, 90, 281, 111))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_651.setFont(font)
        self.label_651.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_651.setObjectName("label_651")
        self.label_654 = QtWidgets.QLabel(self.frame_47)
        self.label_654.setGeometry(QtCore.QRect(850, 30, 311, 121))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_654.setFont(font)
        self.label_654.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_654.setObjectName("label_654")
        self.label_653 = QtWidgets.QLabel(self.frame_47)
        self.label_653.setGeometry(QtCore.QRect(30, 140, 341, 111))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_653.setFont(font)
        self.label_653.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_653.setObjectName("label_653")
        self.OrderSummary_CusName = QtWidgets.QLineEdit(self.frame_47)
        self.OrderSummary_CusName.setGeometry(QtCore.QRect(320, 70, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrderSummary_CusName.setFont(font)
        self.OrderSummary_CusName.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 4px;\n"
"")
        self.OrderSummary_CusName.setText("")
        self.OrderSummary_CusName.setObjectName("OrderSummary_CusName")
        self.OrderSummary_CusAddress = QtWidgets.QLineEdit(self.frame_47)
        self.OrderSummary_CusAddress.setGeometry(QtCore.QRect(320, 120, 1161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrderSummary_CusAddress.setFont(font)
        self.OrderSummary_CusAddress.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 4px;\n"
"")
        self.OrderSummary_CusAddress.setText("")
        self.OrderSummary_CusAddress.setObjectName("OrderSummary_CusAddress")
        self.OrderSummary_CusContactNumber = QtWidgets.QLineEdit(self.frame_47)
        self.OrderSummary_CusContactNumber.setGeometry(QtCore.QRect(1140, 70, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrderSummary_CusContactNumber.setFont(font)
        self.OrderSummary_CusContactNumber.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 4px;\n"
"")
        self.OrderSummary_CusContactNumber.setText("")
        self.OrderSummary_CusContactNumber.setObjectName("OrderSummary_CusContactNumber")
        self.OrderSummary_CusService = QtWidgets.QLineEdit(self.frame_47)
        self.OrderSummary_CusService.setGeometry(QtCore.QRect(320, 170, 461, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrderSummary_CusService.setFont(font)
        self.OrderSummary_CusService.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 4px;\n"
"")
        self.OrderSummary_CusService.setText("")
        self.OrderSummary_CusService.setObjectName("OrderSummary_CusService")
        self.label_656 = QtWidgets.QLabel(self.frame_47)
        self.label_656.setGeometry(QtCore.QRect(850, 130, 311, 131))
        font = QtGui.QFont()
        font.setFamily("Poppins Medium")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_656.setFont(font)
        self.label_656.setStyleSheet("    background-color: transparent;\n"
"")
        self.label_656.setObjectName("label_656")
        self.OrderSummary_CusCash = QtWidgets.QLineEdit(self.frame_47)
        self.OrderSummary_CusCash.setGeometry(QtCore.QRect(1140, 170, 341, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.OrderSummary_CusCash.setFont(font)
        self.OrderSummary_CusCash.setStyleSheet("    background-color: #ffffff;\n"
"    color: black;\n"
"    border-radius: 15px;\n"
"border: 1px solid #000000; \n"
"    padding: 4px;\n"
"")
        self.OrderSummary_CusCash.setText("")
        self.OrderSummary_CusCash.setObjectName("OrderSummary_CusCash")
        self.ConfirmandPrint = QtWidgets.QPushButton(self.frame_47)
        self.ConfirmandPrint.setGeometry(QtCore.QRect(680, 830, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.ConfirmandPrint.setFont(font)
        self.ConfirmandPrint.setStyleSheet("/* Default Inactive Button */\n"
"QPushButton {\n"
"    background-color: #003366;\n"
"    color: #fefefe;\n"
"    border-radius: 15px;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect on Inactive Buttons */\n"
"QPushButton:hover {\n"
"    background-color: rgba(0, 51, 102, 0.9); /* 90% opacity of #003366 */\n"
"}")
        self.ConfirmandPrint.setObjectName("ConfirmandPrint")
        self.Remove = QtWidgets.QPushButton(self.frame_47)
        self.Remove.setGeometry(QtCore.QRect(1180, 830, 301, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Remove.setFont(font)
        self.Remove.setStyleSheet("/* Default Inactive Button */\n"
"QPushButton {\n"
"    background-color: #c25b55;\n"
"    color: #fefefe;\n"
"    border-radius: 15px;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect on Inactive Buttons */\n"
"QPushButton:hover {\n"
"    background-color: rgba(194, 91, 85, 0.9); /* 90% opacity of #c25b55 */\n"
"}")
        self.Remove.setObjectName("Remove")
        self.Back = QtWidgets.QPushButton(self.frame_47)
        self.Back.setGeometry(QtCore.QRect(460, 830, 171, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat Black")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Back.setFont(font)
        self.Back.setStyleSheet("/* Default Inactive Button */\n"
"QPushButton {\n"
"    background-color: #808080; /* Gray background */\n"
"    color: #fefefe; /* White text */\n"
"    border-radius: 15px;\n"
"    padding: 9px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"/* Hover Effect on Inactive Buttons */\n"
"QPushButton:hover {\n"
"    background-color: rgba(128, 128, 128, 0.9); /* 90% opacity of gray (#808080) */\n"
"}")
        self.Back.setObjectName("Back")
        self.tableWidget_OrderSummary = QtWidgets.QTableWidget(self.ViewOrderSummary)
        self.tableWidget_OrderSummary.setGeometry(QtCore.QRect(90, 290, 1441, 561))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        self.tableWidget_OrderSummary.setFont(font)
        self.tableWidget_OrderSummary.setStyleSheet("QTableWidget {\n"
"    background-color: white;\n"
"    gridline-color: lightgray;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #003366; \n"
"    color: #ffffff;\n"
"    font-weight: bold;\n"
"padding: 3;\n"
"}\n"
"")
        self.tableWidget_OrderSummary.setObjectName("tableWidget_OrderSummary")
        self.tableWidget_OrderSummary.setColumnCount(5)
        self.tableWidget_OrderSummary.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_OrderSummary.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_OrderSummary.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_OrderSummary.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_OrderSummary.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.tableWidget_OrderSummary.setHorizontalHeaderItem(4, item)
        self.tableWidget_OrderSummary.horizontalHeader().setDefaultSectionSize(360)
        self.stackedWidget.addWidget(self.ViewOrderSummary)

        self.retranslateUi(CASHIER_ORDERS)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(CASHIER_ORDERS)

    def retranslateUi(self, CASHIER_ORDERS):
        _translate = QtCore.QCoreApplication.translate
        CASHIER_ORDERS.setWindowTitle(_translate("CASHIER_ORDERS", "Form"))
        self.JJelevate_text_2.setText(_translate("CASHIER_ORDERS", "J&J "))
        self.pushButton_Dashboard.setText(_translate("CASHIER_ORDERS", "  Home   "))
        self.pushButton_Order_History.setText(_translate("CASHIER_ORDERS", "Order History"))
        self.pushButton_Sales.setText(_translate("CASHIER_ORDERS", "  Sales"))
        self.pushButton_Account.setText(_translate("CASHIER_ORDERS", " Account     "))
        self.pushButton_LogOut.setText(_translate("CASHIER_ORDERS", "   Log out"))
        self.JJelevate_text_3.setText(_translate("CASHIER_ORDERS", "Elevate"))
        self.pushButton_Orders.setText(_translate("CASHIER_ORDERS", " Orders"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(0)
        item.setText(_translate("CASHIER_ORDERS", "Product ID"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(1)
        item.setText(_translate("CASHIER_ORDERS", "Product Type"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(2)
        item.setText(_translate("CASHIER_ORDERS", "Name"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(3)
        item.setText(_translate("CASHIER_ORDERS", "Price"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(4)
        item.setText(_translate("CASHIER_ORDERS", "Stock Qty."))
        item = self.tableWidget_ProdList.horizontalHeaderItem(5)
        item.setText(_translate("CASHIER_ORDERS", "Updated At"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(6)
        item.setText(_translate("CASHIER_ORDERS", "Color"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(7)
        item.setText(_translate("CASHIER_ORDERS", "Length"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(8)
        item.setText(_translate("CASHIER_ORDERS", "Thickness"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(9)
        item.setText(_translate("CASHIER_ORDERS", "Width"))
        item = self.tableWidget_ProdList.horizontalHeaderItem(10)
        item.setText(_translate("CASHIER_ORDERS", "Other Specifications"))
        self.label_647.setText(_translate("CASHIER_ORDERS", "Product Name      "))
        self.pushButton_Save_OTHERedit_2.setText(_translate("CASHIER_ORDERS", "Specification"))
        self.label_648.setText(_translate("CASHIER_ORDERS", "Quantity"))
        self.OrderInput_prodnameDisplay_2.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.OrderInput_Qty_2.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.Add_Order_2.setText(_translate("CASHIER_ORDERS", "Add to Order"))
        self.label_649.setText(_translate("CASHIER_ORDERS", "Discount (if applicable)"))
        self.OrderInput_Discount_2.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.View_OrderSummary.setText(_translate("CASHIER_ORDERS", "View Order Summary"))
        self.comboBox_filterProduct_List.setCurrentText(_translate("CASHIER_ORDERS", "    Filter Product"))
        self.comboBox_filterProduct_List.setItemText(0, _translate("CASHIER_ORDERS", "    Filter Product"))
        self.comboBox_filterProduct_List.setItemText(1, _translate("CASHIER_ORDERS", "Roof"))
        self.comboBox_filterProduct_List.setItemText(2, _translate("CASHIER_ORDERS", "Spandrel"))
        self.comboBox_filterProduct_List.setItemText(3, _translate("CASHIER_ORDERS", "Gutter"))
        self.comboBox_filterProduct_List.setItemText(4, _translate("CASHIER_ORDERS", "Others"))
        self.comboBox_filterProduct_List.setItemText(5, _translate("CASHIER_ORDERS", "All Products"))
        self.lineEdit__QuicksearchProduct.setPlaceholderText(_translate("CASHIER_ORDERS", "      Quick Search"))
        self.pushButton_searchProduct.setText(_translate("CASHIER_ORDERS", "Search"))
        self.orderReportText.setText(_translate("CASHIER_ORDERS", "Product List"))
        self.pushButton_Save_OTHERedit_3.setText(_translate("CASHIER_ORDERS", "Order Summary"))
        self.label_650.setText(_translate("CASHIER_ORDERS", "Customer Name               :"))
        self.label_651.setText(_translate("CASHIER_ORDERS", "Address                              :"))
        self.label_654.setText(_translate("CASHIER_ORDERS", "Contact number           :"))
        self.label_653.setText(_translate("CASHIER_ORDERS", "Service                              :"))
        self.OrderSummary_CusName.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.OrderSummary_CusAddress.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.OrderSummary_CusContactNumber.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.OrderSummary_CusService.setPlaceholderText(_translate("CASHIER_ORDERS", "Install / Supply / Repair / Deliver"))
        self.label_656.setText(_translate("CASHIER_ORDERS", "Enter Amount Payed    :"))
        self.OrderSummary_CusCash.setPlaceholderText(_translate("CASHIER_ORDERS", "....."))
        self.ConfirmandPrint.setText(_translate("CASHIER_ORDERS", "Confirm Order and Print Receipt"))
        self.Remove.setText(_translate("CASHIER_ORDERS", "Remove from Order"))
        self.Back.setText(_translate("CASHIER_ORDERS", "Back"))
        item = self.tableWidget_OrderSummary.horizontalHeaderItem(0)
        item.setText(_translate("CASHIER_ORDERS", "Name"))
        item = self.tableWidget_OrderSummary.horizontalHeaderItem(1)
        item.setText(_translate("CASHIER_ORDERS", "Qty."))
        item = self.tableWidget_OrderSummary.horizontalHeaderItem(2)
        item.setText(_translate("CASHIER_ORDERS", "Price"))
        item = self.tableWidget_OrderSummary.horizontalHeaderItem(3)
        item.setText(_translate("CASHIER_ORDERS", "Discount"))
        item = self.tableWidget_OrderSummary.horizontalHeaderItem(4)
        item.setText(_translate("CASHIER_ORDERS", "Total"))
