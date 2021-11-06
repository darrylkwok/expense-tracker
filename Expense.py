
# Helper functions
def addNewExpense(day, category, description, amount):
    categories = ["Food", "Entertainment", "Shopping", "Groceries", "Other", "Description"]
    values = ["0", "0", "0", "0", "0", "0"]

    day_output = "Day," + day.strip()
    desc_output = description.strip()
    amount_output = amount.strip()
    category_output  = category.strip()

    # find the index of the category this expense belongs to
    cat_index = categories.index(category_output)
    # replace the amount in the category index position
    values[cat_index] = amount_output

    # replace the description value in the categories list
    values[-1] = desc_output

    output = day_output 

    for i in range(len(categories)):
        output += "," + categories[i] + "," + values[i]
    
    return output


def addNewMonth(month, year):
    month_year = f'MONTH_YEAR,{month} {year}'

    return month_year

def addNewBudget(budget_amount):
    output = "BUDGET," + budget_amount

    return output
