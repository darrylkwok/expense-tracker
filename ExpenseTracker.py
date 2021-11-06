# Main file
import sys
import sys, os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic

from Expense import *

# specifying the ui file 
qtCreatorFile = "ExpenseTracker.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Main(QMainWindow, Ui_MainWindow):
    monthly_info = {}
    current_month_budget = 0
    current_month_expenses = {}
    filename = ""
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Hide alerts on start up
        self.addMonth_alert.setVisible(False)
        self.newMonthError_alert.setVisible(False)
        self.newExpenseError_alert.setVisible(False)
        
        # Upload / Create File buttons
        self.uploadFile_button.clicked.connect(self.uploadFile)
        self.newFile_button.clicked.connect(self.createFile)
        
        # Observe Selected Month dropdown changes
        self.selectMonth_list.currentTextChanged.connect(self.displayExpense)
        
        # Add New Month / Expense buttons
        self.expenseAdd_button.clicked.connect(self.addNewExpense)
        self.monthAdd_button.clicked.connect(self.addNewMonth)
        
        # Set up for expense table display
        self.expenseTable.setColumnCount(3)
        self.expenseTable.setColumnWidth(0, 120)
        self.expenseTable.setColumnWidth(1, 151)
        self.expenseTable.setColumnWidth(2, 80)

    def createFile(self):    
        # Create blank text file for new user:
        with open("user_data.txt", "w") as file:
            file.write("")
        
        # Save filename to global
        self.filename = "user_data.txt"
        
        # Reset Global Monthly_info dict
        self.monthly_info = {}
        
        # Reset Total Budget, Total Expense & Budget Left Display
        self.totalExpenses_text.setText("0.0")
        self.budgetLeft_text.setText("0.0")
        self.budgetDisplay.setText("0.0")
        
        # Read new file after creation
        self.readFile("user_data.txt")
        
        # Show alert on new file to remind user to create new month!
        self.addMonth_alert.setVisible(True)
        # Hide all other possible alerts
        self.newExpenseError_alert.setVisible(False)
        self.newMonthError_alert.setVisible(False)
        
        # Disable Add expense button as no month available in new file
        self.expenseAdd_button.setEnabled(False)
        

    def uploadFile(self):
        print('clicked upload file')
        # Open File Dialog Pop up for File selection
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self,'Open file',
                                            os.getcwd(),'TXT(*.txt)',
                                            options=options)
        
        # If any file selected, get file name E.g."example.txt"
        if fname[0]:
            filepath = fname[0]
            # Save filename to global
            self.filename = filepath[filepath.rfind('/') + 1:]
            print(self.filename)
            
            # Reset Total Budget, Total Expense & Budget Left Display
            self.totalExpenses_text.setText("0.0")
            self.budgetLeft_text.setText("0.0")
            self.budgetDisplay.setText("0.0")

            # Remove all alerts for new upload
            self.addMonth_alert.setVisible(False)
            self.newExpenseError_alert.setVisible(False)
            self.newMonthError_alert.setVisible(False)

            # Call read file to get the data out
            self.readFile(self.filename)
            
     
    def readFile(self, filename):
        # Enable Add New Month button When either new file created or file uploaded
        self.monthAdd_button.setEnabled(True)
        
        # Obtain all text from file 
        f=open(filename,"r")
        self.fileSelected_display.setText(filename)
        expense_lines=f.readlines()
        f.close()

        # monthly_info stores all the monthly budget and expenses
        monthly_info = {}
        # expense only stores the expenses and is appended to the monthly_info 
        # after reading all the lines or reading a new month in the txt file
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
        
        # Store monthly_info dict in global
        # {'Oct 2021': ['300', 
        #     {'11': {'Shopping': [('10', 'Books')], 'Groceries': [('2', 'Bus')]}, 
        #      '12': {'Shopping': [('10', 'Books')]}}]
        # }
        self.monthly_info = monthly_info
        
        # Loads all the months in the combobox
        self.loadMonth()
        

    def loadMonth(self):
        # Get list of months
        months = []
        for key in self.monthly_info:
            months.append(key)
        
        print("months")
        print(months)
        # If there are months in dropdown, Enable Add New Expense button
        if (len(months) > 0):
            print("yes months")
            self.expenseAdd_button.setEnabled(True)
        else:
            print("no months")
            self.expenseAdd_button.setEnabled(False)
            self.addMonth_alert.setVisible(True)

        # Clear existing data in dropdown
        self.selectMonth_list.clear()
        
        # Start displaying the dropdown from the latest month
        for month in reversed(months):
            self.selectMonth_list.addItem(month)
        
        
    def displayExpense(self):
        # Obtain data of current month selected
        month_selected = self.selectMonth_list.currentText()
        
        # Clear Table and RowCount each time new month is selected
        self.expenseTable.clear()
        self.expenseTable.setRowCount(0)
        
        # Check if any months selected
        # New file has no months available/selected, hence Nothing to display
        if (month_selected != ""):
            # Obtain Current Month's Data, [Budget, {All expenses}]
            # ['300', {'11': {'Shopping': [('10', 'Books')], 'Groceries': [('2', 'Bus')]}, 
            #  '12': {'Shopping': [('10', 'Books')]}}]
            current_month_data = self.monthly_info[month_selected]
            
            # Display Budget for current month -- if is int, convert to float to show decimals
            self.budgetDisplay.setText(str(round(float(current_month_data[0]),2)))
            self.budgetLeft_text.setText(str(round(float(current_month_data[0]),2)))
            
            # Store Current Month's budget in global
            self.current_month_budget = float(current_month_data[0])
            
            # If not new month (E.g. 'Dec 2021': ['300', {}]), Else Nothing to Display
            print("current_month_data")
            print(current_month_data)
            if (len(current_month_data) > 1):
                # Get Current Month's expenses (Dict)
                # {'11': {'Shopping': [('10', 'Books')], 'Groceries': [('2', 'Bus')]}}
                expenses = current_month_data[1]
                
                # Store Current Month's expenses in global
                self.current_month_expenses = expenses

                # Calculate & Display total spent this month
                self.calculateMonthExpenses()

                # Set Up Table RowCount before adding of items
                self.setUpTableRow()
                row = 0
                
                for day in expenses:
                    # Get expenses for each day (Dict)
                    # {'Shopping': [('10', 'Books')], 'Groceries': [('2', 'Bus')]}
                    day_expenses = expenses[day]
                    
                    # Calculate Total Expenses for each day (STRING)
                    total_daily = self.calculateDailyExpenses(day_expenses)
                    
                    # Display Row with Day + Total Daily Expense 
                    date = QtWidgets.QTableWidgetItem(day + " " + month_selected)
                    date.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.expenseTable.setItem(row, 0, date)
                    self.expenseTable.setItem(row, 1, QtWidgets.QTableWidgetItem())
                    total = QtWidgets.QTableWidgetItem(total_daily)
                    total.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.expenseTable.setItem(row, 2, total)
                    
                    # Colour Row for Date blue
                    self.expenseTable.item(row, 0).setBackground(QtGui.QColor(170, 255, 255))
                    self.expenseTable.item(row, 1).setBackground(QtGui.QColor(170, 255, 255))
                    self.expenseTable.item(row, 2).setBackground(QtGui.QColor(170, 255, 255))
                                          
                    row += 1
                    for category in day_expenses:
                        # Get expenses for each category (List)
                        # [('10', 'Books'), ('2', 'Pen')]
                        cat_expenses = day_expenses[category]

                        # Get individual item spent (Tuple)
                        # ('10', 'Books')
                        for spend in cat_expenses:
                            # Create QTableWidgetItems
                            cat = QtWidgets.QTableWidgetItem(category)
                            cat.setTextAlignment(QtCore.Qt.AlignCenter)
                            self.expenseTable.setItem(row, 0, cat)

                            desc = QtWidgets.QTableWidgetItem(spend[1])
                            desc.setTextAlignment(QtCore.Qt.AlignCenter)
                            self.expenseTable.setItem(row, 1, desc)

                            amount = QtWidgets.QTableWidgetItem(str(round(float(spend[0]),2)))
                            amount.setTextAlignment(QtCore.Qt.AlignCenter)
                            self.expenseTable.setItem(row, 2, amount)
                            row += 1
        
    
    def calculateMonthExpenses(self):
        # Get all expenses into list regardless of dates
        # [[('100', 'Malaysia'), ('99', 'Thailand')], [('10', 'Books')]], [[('2', 'Train')]]]
        month_expenses_list = [list(dict.values(i)) for i in list(dict.values(self.current_month_expenses))]

        # Calculate total expense in this month
        monthly_total = 0
        for day in month_expenses_list:
            # day = [[('100', 'Malaysia'), ('99', 'Thailand')], [('10', 'Books')]]
            
            for i in range(len(day)):
                # day[i] = [('100', 'Malaysia'), ('99', 'Thailand')]
                
                for j in range(len(day[i])):
                    # day[i][j] = ('100', 'Malaysia')
                    monthly_total += float(day[i][j][0])
        
        # Set Total Expenses Spent Display
        self.totalExpenses_text.setText(str(round(monthly_total,2)))
        
        # Calculate Budget left and Set Display
        budget_left = self.current_month_budget - monthly_total
        self.budgetLeft_text.setText(str(round(budget_left,2)))
        
        
    def calculateDailyExpenses(self, day_expenses):
        # Get all expenses in a day into list
        # [('100', 'Malaysia'), ('99', 'Thailand')], [('10', 'Books')]]
        day_expenses_list = list(dict.values(day_expenses))
        
        # Calculate total expense on this day
        daily_total = 0
        for category in day_expenses_list:
            # category = [('100', 'Malaysia'), ('99', 'Thailand')]
            
            for i in range(len(category)):
                # category[i] = ('100', 'Malaysia')
                daily_total += float(category[i][0])
                    
        return str(round(daily_total,2))
        
    
    def setUpTableRow(self):
        # Count number of rows needed for month selected
        count = 0
        
        # Get all spend days in a list ["11", "12", "13", ...]
        days_list = list(self.current_month_expenses)
        
        for i in range(len(self.current_month_expenses)):
            # One row for one day
            count += 1
            
            # Get spend categories each day in a list ["Food", "Transport", "Shopping", ...]
            day = days_list[i]
            cats_list = list(self.current_month_expenses[day])
            
            for j in range(len(self.current_month_expenses[day])):
                cat = cats_list[j]
                # One row for one spend in all categories
                count += len(self.current_month_expenses[day][cat])
                
        self.expenseTable.setRowCount(count)
    
    def addNewExpense(self):
        # If Alert was visible, set invisible after each click first
        if (self.newExpenseError_alert.isVisible()):
            self.newExpenseError_alert.setVisible(False)
            
        # Get All Required Text
        day = self.expenseDate_edit.text().strip()
        category = self.expenseCategory_list.currentText()
        amount = self.expenseAmount_edit.text().strip()
        description = self.expenseDescription_edit.text().strip()
        current_month = self.selectMonth_list.currentText()
        
        # Check if all fields have values, if not show error
        if (day == "" or amount == "" or description == ""):
            self.newExpenseError_alert.setText("No empty fields allowed")
            self.newExpenseError_alert.setVisible(True)
            
        # Check if this is an existing date in the month
        else:
            if (day in self.current_month_expenses):
                # Check if this is an existing category in the day
                if (category in self.current_month_expenses[day]):
                    # Append spend to existing category in the day
                    self.current_month_expenses[day][category].append((amount,description))

                else:
                    # Create new category spend for the day
                    self.current_month_expenses[day][category] = [(amount,description)]

            else:
                # Create new day in the month with expense data
                self.current_month_expenses[day] = {category: [(amount,description)]}
            
            # Update new expense into global monthly_info and display in table
            if (len(self.monthly_info[current_month]) > 1):
                self.monthly_info[current_month][1] = self.current_month_expenses
            else:
                self.monthly_info[current_month].append(self.current_month_expenses)
                
            self.displayExpense()
            
            # Reset all input fields
            self.expenseDate_edit.setText("")
            self.expenseCategory_list.setCurrentIndex(0)
            self.expenseAmount_edit.setText("")
            self.expenseDescription_edit.setText("")
            
            # Overwrite current file with new information
            self.updateFile()
    
    def addNewMonth(self):
        # If Alert was visible, set invisible after each click first
        if (self.newMonthError_alert.isVisible()):
            self.newMonthError_alert.setVisible(False)
            
        # Get All Required Text
        new_month = self.newMonth_edit.text().strip()
        new_budget = self.newBudget_edit.text().strip()
        
        # Check if all fields have values, if not show error
        if (new_month == "" or new_budget == ""):
            self.newMonthError_alert.setText("No empty fields allowed")
            self.newMonthError_alert.setVisible(True)
            
        # Update new month into monthly_info dict to be displayed
        else:
            self.monthly_info[new_month] = [new_budget]

            # Reset Data for New, Empty Month
            self.current_month_expenses = {}
            self.totalExpenses_text.setText("0.00")
            self.budgetLeft_text.setText(new_budget) 

            # Display New Month 
            self.loadMonth()
            self.displayExpense()
            
            # If from new file, remove alert for user to add new month
            if (self.addMonth_alert.isVisible()):
                self.addMonth_alert.setVisible(False)
        
            # Reset all input fields
            self.newMonth_edit.setText("")
            self.newBudget_edit.setText("")
            
            # Overwrite current file with new information
            self.updateFile()
    
    def updateFile(self):
        # Initialise fixed category list
        categories = ["Food", "Entertainment", "Shopping", "Groceries", "Transport", "Other", "Description"]
        
        # Open current file selected and overwrite
        with open(self.filename, "w") as file:
            # {'Oct 2021': ['500', {'15': {'Food': [('10', 'Macs'), ('6', Burger)], 'Entertainment': [('10', 'Movie')]}, 
            #    '16': {'Transport': [('3', 'Bus')]}}]}
            for month_year in (self.monthly_info):
                file.write("MONTH_YEAR," + month_year + "\n")
                current_month_budget = self.monthly_info[month_year][0]
                file.write("BUDGET," + current_month_budget + "\n")
                
                print("monthly_info")
                print(self.monthly_info)
                
                # If not just ['500'] (i.e only have budget no expense)
                if (len(self.monthly_info[month_year]) > 1):
                    # {'15': {'Food': [('10', 'Macs'), ('6', Burger)], 'Entertainment': [('10', 'Movie')]}, 
                    #  '16': {'Transport': [('3', 'Bus')]}}
                    current_month_expense = self.monthly_info[month_year][1]
                    for day in current_month_expense:
                        day_output = "Day," + day

                        # {'Food': [('10', 'Macs'), ('6', Burger)], 'Entertainment': [('10', 'Movie')]}
                        current_day_expense = current_month_expense[day]
                        for category in current_day_expense:
                            category_output = category

                            # [('10', 'Macs'), ('6', Burger)]
                            current_cat_expense = current_day_expense[category]
                            for expense in current_cat_expense:
                                amount_output = expense[0]
                                desc_output = expense[1]

                                # Prepare data to be written in line
                                values = ["0", "0", "0", "0", "0", "0", "0"]
                                # find the index of the category this expense belongs to
                                cat_index = categories.index(category_output)
                                # replace the amount in the category index position
                                values[cat_index] = amount_output

                                # replace the description value in the categories list
                                values[-1] = desc_output

                                # Initalise line_output with day info "Day,1"
                                line_output = day_output 
                                # Day,1,Food,0,Entertainment,0,Shopping,12,Groceries,0,Transport,0,Other,0,Description,Mac
                                for i in range(len(categories)):
                                    line_output += "," + categories[i] + "," + values[i]

                                file.write(line_output + "\n")
                            
            file.close()
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())