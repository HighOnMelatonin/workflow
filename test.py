

date = str(input("Date (YYYY/MM/DD): "))

date = date.split('/')

for i in range(len(date)):
    date[i] = int(date[i])

print(tuple(date))
