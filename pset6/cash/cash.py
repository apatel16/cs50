import cs50

print("O hai! ")
while True:
    change = cs50.get_float("How much change is owed? ")
    if change < 0.0:
        continue
    else:
        break

cents = change * 100.0
leftover = round(cents)

number_of_quarters = int(leftover / 25)
leftover = leftover % 25

number_of_dimes = int(leftover / 10)
leftover = leftover % 10

number_of_nickels = int(leftover / 5)
leftover = leftover % 5

number_of_pennies =  int(leftover)

total_coins = number_of_quarters + number_of_dimes + number_of_nickels + number_of_pennies
print(total_coins)

