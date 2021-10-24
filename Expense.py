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

with open('test_input.txt') as f:
    test_lines = f.readlines()
    f.close()


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

# monthly_info stores all the monthly budget and expenses
monthly_info = {}
# expense only stores the expenses and is appended to the monthly_info after reading all the lines or reading a new month in the txt file
expense = {}
tracker = None

for each_line in test_lines:
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

## Sum the total expense for each category

## Sum the total expense for each month

## Function to trigger threshold alert 





# Edit Budget 
## Allow user to edit the existing budget


