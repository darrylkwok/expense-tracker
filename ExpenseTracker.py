# Main file
import sys
import math
# import pandas as pd
# import numpy as np
import sys, os
from datetime import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic

from Expense import *

# specifying the ui file 
qtCreatorFile = "ExpenseTracker.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# # Get full path of directory of current file
# ui_path = os.path.dirname(os.path.abspath(__file__))
# # Combine path with UI name, and pass to loadUiType
# Ui_MainWindow, QtBaseClass = uic.loadUiType(os.path.join(ui_path, "ExpenseTracker.ui"))

#Incomplete
class Main(QMainWindow, Ui_MainWindow):
    monthly_info = {}
    month_list = []
    current_month_budget = 0
    curren_month_expenses = {}
    filename = ""
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Hide alert on start up
        self.addMonth_alert.setVisible(False)
        
        self.uploadFile_button.clicked.connect(self.uploadFile)
        self.newFile_button.clicked.connect(self.createFile)
        
        self.selectMonth_list.currentTextChanged.connect(self.displayExpense)
        
        # Set up for expense table display
        self.expenseTable.setColumnCount(3)
        self.expenseTable.setColumnWidth(0, 120)
        self.expenseTable.setColumnWidth(1, 148)
        self.expenseTable.setColumnWidth(2, 80)

    def createFile(self):    
        # Create blank text file for new user:
        with open("user_data.txt", "w") as file:
            file.write("")
            
        self.monthly_info = {}
        
        # Read new file after creation
        self.readFile("user_data.txt")
        
        # Show alert on new file to remind user to create new month!
        self.addMonth_alert.setVisible(True)
        # Disable Add expense button as no month available in new file
        self.expenseAdd_button.setEnabled(False)
        # Reset Total Budget, Total Expense & Budget Left Display
        self.totalExpenses_text.setText("0.0")
        self.budgetLeft_text.setText("0.0")
        self.budgetDisplay.setText("0.0")

    def uploadFile(self):
        print('clicked upload file')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self,'Open file',
                                            os.getcwd(),'TXT(*.txt)',
                                            options=options)
        
        # If any file selected, get file name E.g."example.txt"
        if fname[0]:
            filepath = fname[0]
            self.filename = filepath[filepath.rfind('/') + 1:]
            print(self.filename)
            
            # Call read file to get the data out
            self.readFile(self.filename)
            
     
    def readFile(self, filename):
        # Enable Add New Month button When either new file created or file uploaded
        self.monthAdd_button.setEnabled(True)
        
        f=open(filename,"r")
        self.fileSelected_display.setText(filename)
        expense_lines=f.readlines()
        f.close()

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
        
        print("monthly_info")
        print(monthly_info)
        self.monthly_info = monthly_info
        
        # Loads all the months in the combobox
        self.loadMonth()
        

    def loadMonth(self):
        months = []
        for key in self.monthly_info:
            months.append(key)
        
        self.month_list = months
        
        # Clear dropdown first
        self.selectMonth_list.clear()
        
        # IF There's Existing Months, Enable Add New Expense button
        if (months != []):
            self.expenseAdd_button.setEnabled(True)
        
        # Start displaying the dropdown from the latest month
        for month in reversed(self.month_list):
            self.selectMonth_list.addItem(month)
        
        
    def displayExpense(self):
        # Obtain data of current month selected
        month_selected = self.selectMonth_list.currentText()
        # Clear Table and RowCount each time new month_data loaded
        self.expenseTable.clear()
        self.expenseTable.setRowCount(0)
            
        if (month_selected != ""):
            current_month_data = self.monthly_info[month_selected]
            print("Month Selected: " + month_selected)

            # Display Budget for current month -- if is int, convert to float to show decimals
            self.budgetDisplay.setText(str(float(current_month_data[0])))
            
            # Store Current Month's budget in global
            self.current_month_budget = float(current_month_data[0])
            
            if (len(current_month_data) != 1):
                # Get Current Month's expenses (Dict)
                expenses = current_month_data[1]
                # Store Current Month's expenses in global
                self.current_month_expenses = expenses
                print("Current Month Expenses")
                print(self.current_month_expenses)

                # Calculate & Display total spent this month
                self.calculateMonthExpenses()

                # Set Up Table RowCount before adding of items
                self.setUpTableRow()
                row = 0
                
                for day in expenses:
                    # Get expenses for each day (Dict)
                    day_expenses = expenses[day]
                    
                    # Calculate Total Expenses for each day (STRING)
                    total_daily = self.calculateDailyExpenses(day_expenses)
                    
                    # Display Row with Day + Total Daily Expense 
                    self.expenseTable.setItem(row, 0, QtWidgets.QTableWidgetItem(day + " " + month_selected))
                    total = QtWidgets.QTableWidgetItem(total_daily)
                    total.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.expenseTable.setItem(row, 2, total)
                    row += 1
                    
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

                            amount = QtWidgets.QTableWidgetItem(str(float(spend[0])))
                            amount.setTextAlignment(QtCore.Qt.AlignCenter)
                            self.expenseTable.setItem(row, 2, amount)
                            row += 1
        
    def calculateMonthExpenses(self):
        # Get all expenses into list regardless of dates
        month_expenses_list = [list(dict.values(i)) for i in list(dict.values(self.current_month_expenses))]
        
        # Calculate total expense in this month
        monthly_total = 0
        for day in month_expenses_list:
            for i in range(len(day)):
                for j in range(len(day[i])):
                    monthly_total += float(day[i][j][0])
        
        # Set Total Expenses Spent Display
        self.totalExpenses_text.setText(str(monthly_total))
        
        # Calculate Budget left and Set Display
        budget_left = self.current_month_budget - monthly_total
        self.budgetLeft_text.setText(str(budget_left))
        
    def calculateDailyExpenses(self, day_expenses):
        day_expenses_list = list(dict.values(day_expenses))

        daily_total = 0
        for category in day_expenses_list:
            for i in range(len(category)):
                daily_total += float(category[i][0])
                    
        print("daily_total: " + str(daily_total))
        return str(daily_total)
        
    
    def setUpTableRow(self):
        count = 0
        # Get all spend days in a list ["11", "12", "13", ...]
        days_list = list(self.current_month_expenses)
        for i in range(len(self.current_month_expenses)):
            # One row for one day
            count += 1
            day = days_list[i]
            
            # Get spend categories each day in a list ["Food", "Transport", "Shopping", ...]
            cats_list = list(self.current_month_expenses[day])
            for j in range(len(self.current_month_expenses[day])):
                cat = cats_list[j]
                # One row for one spend in all categories
                count += len(self.current_month_expenses[day][cat])
                
        print("Row Count: " + str(count))
        self.expenseTable.setRowCount(count)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())