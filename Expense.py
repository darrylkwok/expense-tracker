# Helper functions

class Expense:
    def __init__(self, selectMonth, selectCategory, expenseMade, expenseBudget):
        self.selectMonth = selectMonth
        self.selectCategory = selectCategory
        self.expenseMade = expenseMade
        self.expenseBudget = expenseBudget


    def budgetLeft(self):
        budget_left = self.expenseBudget - self.expenseMade

        return budget_left

    


# Create file 
## Set up with open txt file, retrieve the system date (MONTH_YEAR, BUDGET = 0)

# Upload file
## Read the file, read all the content
## Helper functions

# Helper functions

## monthly_budget and monthly expense dictionaries
### {"Nov_2021" : [
###               500, 
###               {
###                "15" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []},
###                "16" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []},
###                "17" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []}
###               }
###               ]
### }

for each_line in test_input:
    monthly_budget = {}
    expense = {}
    line_list = each_line.split(",") # ['MONTH_YEAR', 'Oct 2021']
    if line_list[0] == 'MONTH_YEAR':
        monthly_budget[line_list[1]] = 0
        tracker = line_list[0]
    
    elif line_list[0] == "BUDGET":
        monthly_budget[tracker] = line_list[1]
    
    elif line_list[0] == "Day": # {'Day' : [], 'Food' : [], "Entertainment" : []}
        for item in len(line_list) - 1:
            expense[item] = []

    else: # {'Day' : 15, 'Food' : [("Macs",10), ("Koufu" : 6.50)], "Entertainment" : []}
        # Update the day in the dict
        expense['Day'] = line_list[0]

        # Add transaction to that day
        for i in range(1, len(expense) - 1): 
            expense[list(expense.keys())[i]].append((line_list[-1], line_list[i]))


## Sum the total expense for each category

## Sum the total expense for each month

## Sum the total expense for each year 

## Function to trigger threshold alert 





# Edit Budget 
## Allow user to edit the existing budget


# MONTH_YEAR, Oct 2021
# BUDGET, 500
# Day, Food, Entertainment, Transport, School, Travel, Description
# 15,  10, 0, 0, 0, 0, Macs
# 15,  10, 0, 0, 0, 0, Koufu 
# 15,  0, 10, 0, 0, 0
# 15,  0, 0, 10, 0, 0
# 15,  0, 0, 0, 10, 0
# 15,  0, 0, 0, 0, 10
# MONTH_YEAR, Nov 2021
# BUDGET, 500
# Day, Food, Entertainment, Transport, School
# 15, 0, 10, 0, 0 
# 15, 50, 0, 0, 0