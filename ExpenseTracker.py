# Main file
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic

from Expense import *

# specifying the ui file 
qtCreatorFile = "ExpenseTracker.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#Incomplete
class Main(QMainWindow, Ui_MainWindow):
    monthly_info = {}
    month_list = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.uploadFile_button.clicked.connect(self.uploadFile)
        self.selectMonth_list.currentTextChanged.connect(self.displayExpense)
        
        # Set up for expense table display
        self.expenseTable.setColumnCount(3)
        self.expenseTable.setColumnWidth(0, 120)
        self.expenseTable.setColumnWidth(1, 148)
        self.expenseTable.setColumnWidth(2, 80)

    def uploadFile(self):
        print('clicked upload file')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self,'Open file',
                                            os.getcwd(),'TXT(*.txt)',
                                            options=options)
        
        # If any file selected, just import test_input.txt :')
        if fname[0]:
            f=open("test_input.txt","r")
            self.fileSelected_display.setText("test_input.txt")
            expense_lines=f.readlines()
            f.close()

            # Call read file to get the data out
            self.readFile(expense_lines)
            
        
    def readFile(self, expense_lines):
        # monthly_info stores all the monthly budget and expenses
        monthly_info = {}
        # expense only stores the expenses and is appended to the monthly_info after reading all the lines or reading a new month in the txt file
        expense = {}
        tracker = None

        for each_line in expense_lines:
            line_list = each_line.strip().split(",") # ['MONTH_YEAR', 'Oct 2021']
            if line_list[0] == 'MONTH_YEAR': 
                if tracker == None:
                    monthly_info[line_list[1]] = []
                    tracker = line_list[1]
                else:
                    monthly_info[tracker].append(expense)
                    expense = {}
                    monthly_info[line_list[1]] = []
                    tracker = line_list[1]

            elif line_list[0] == "BUDGET":
                monthly_info[tracker].append(line_list[1])
            
            elif line_list[0] == "Day": # {Day : {'Food' : [], "Entertainment" : []} }
                if line_list[1] not in expense:
                    expense[line_list[1]] = {}

                # loop till the fourth last element
                for i in range(2, len(line_list) - 3, 2):
                    if line_list[i] in expense[line_list[1]]:
                        if (line_list[i+1] != "0"):
                            expense[line_list[1]][line_list[i]].append((line_list[i+1], line_list[-1]))
                    
                    else:
                        if (line_list[i+1] != "0"):
                            expense[line_list[1]][line_list[i]] = [(line_list[i+1], line_list[-1])]

        # Finish reading all the lines in the txt file
        if tracker != None and expense != {}:
            monthly_info[tracker].append(expense)
        
         # print("monthly_info")
        # print(monthly_info)
        self.monthly_info = monthly_info
        
        # Loads all the months in the combobox
        self.loadMonth()
        

    def loadMonth(self):
        for key in self.monthly_info:
            self.month_list.append(key)

        # Start displaying the dropdown from the latest month
        for month in reversed(self.month_list):
            self.selectMonth_list.addItem(month)

    def displayExpense(self):
        month_selected = self.selectMonth_list.currentText()
        self.current_month_data = self.monthly_info[month_selected]
        # print(self.current_month_data)

        # Display Budget for current month
        self.budgetDisplay.setText(self.current_month_data[0])
        
        # Get Current Month's expenses (Dict)
        expenses = self.current_month_data[1]
        print(expenses)
        row = 0
        self.expenseTable.setRowCount(9)
        
        for day in expenses:
            self.expenseTable.setItem(row, 0, QtWidgets.QTableWidgetItem(day + " " + month_selected))
            row += 1
            # Get expenses for each day (Dict)
            day_expenses = expenses[day]
            for category in day_expenses:
                # Get expenses for each category (List)
                cat_expenses = day_expenses[category]

                # Get individual item spent (Tuple)
                for spend in cat_expenses:
                    # Create QTableWidgetItems
                    cat = QtWidgets.QTableWidgetItem(category)
                    cat.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.expenseTable.setItem(row, 0, cat)
                    
                    desc = QtWidgets.QTableWidgetItem(spend[1])
                    desc.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.expenseTable.setItem(row, 1, desc)
                    
                    amount = QtWidgets.QTableWidgetItem(spend[0])
                    amount.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.expenseTable.setItem(row, 2, amount)
                    row += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())