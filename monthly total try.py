##sum up monthly total

##example monthly dictionary
d = {"Nov_2021" : [500, {
            "15" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []},
            "16" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []},
            "17" : {'Food' : [("Macs", 10), ("Koufu", 6.50)], "Entertainment" : []}
           }]}

##accessing amounts to sum
month_expenses = [list(dict.values(i)) for i in list(dict.values(d["Nov_2021"][1]))]

daily_expenses =[]
for day in month_expenses:
    for i in range(len(day)):
        for j in range(len(day[i])):
            daily_expenses.append(day[i][j][1])

##sum
monthly_total = 0

for amount in daily_expenses:
    monthly_total=monthly_total+amount

print(monthly_total)
print(30+3*6.5)  ##check  
