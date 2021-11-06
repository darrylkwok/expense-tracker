##sum up monthly total

##example monthly dictionary
d = {"Nov_2021" : [500, {
            "15" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []},
            "16" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []},
            "17" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []}
           }]}

# ##accessing amounts to sum
# ##the "Nov_2021" is what is selected -- need to add to UI code
# month_expenses = [list(dict.values(i)) for i in list(dict.values(d["Nov_2021"][1]))]
# print("month_expense")
# print(month_expenses)

# # monthly_expenses =[]
# monthly_total = 0
# for day in month_expenses:
#     for i in range(len(day)):
#         for j in range(len(day[i])):
#             # monthly_expenses.append(day[i][j][1])
#             monthly_total += day[i][j][1]

# ##sum
# # monthly_total = 0

# # for amount in monthly_expenses:
# #     monthly_total=monthly_total+amount

# print(monthly_total)
# print(30+3*6.5)  ##check  


##daily total
##the "Nov_2021" and "15" is what is selected -- need to add to UI code
day_expenses=list(dict.values(d["Nov_2021"][1]["15"]))
print(d["Nov_2021"][1]["15"])
print(day_expenses)

daily_expenses =[]
for category in day_expenses:
    for i in range(len(category)):
        for j in range(len(category[i])):
            if type(category[i][j])==int:
                daily_expenses.append(category[i][j])
            elif type(category[i][j])==float:
                daily_expenses.append(category[i][j])
            
            
daily_total = 0

for amount in daily_expenses:
    daily_total=daily_total+amount

print(daily_total)
