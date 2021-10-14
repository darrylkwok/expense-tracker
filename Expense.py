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