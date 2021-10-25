# Main file
import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic

from Expense import *

# specifying the ui file 
qtCreatorFile = "ExpenseTracker.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#Incomplete
class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.uploadFile_button.clicked.connect(self.uploadFile)


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
            print("AM BEFORE RETURN EXPENSE_LINES")
            print(expense_lines)
            self.readFile(expense_lines)
            # Call read file to get the data out
            # To implement
        
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
                        if line_list[i+1] != "0":
                            expense[line_list[1]][line_list[i]].append((line_list[i+1], line_list[-1]))
                    
                    else:
                        if line_list[i+1] != "0":
                            expense[line_list[1]][line_list[i]] = [(line_list[i+1], line_list[-1])]

        # Finish reading all the lines in the txt file
        if tracker != None and expense != {}:
            monthly_info[tracker].append(expense)
        
        print("monthly_info")
        print(monthly_info)
        return monthly_info




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())