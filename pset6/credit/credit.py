import cs50

while True:
    print("Enter credit card number: ")
    cc_number = cs50.get_float()

    if not cc_number:
        continue
    else:
        break

temp = cc_number
i = 0
sum1 = 0
sum2 = 0

while (temp != 0):

    digit = int(temp % 10)
    temp = int(temp / 10)

    if (i % 2 == 0):
        sum2 = sum2 + digit
    else:
        temp2 = digit * 2
        if (temp2 < 10):
            sum1 = sum1 + temp2

        else:
            sum1 = sum1 + (temp2 % 10) + (temp2 // 10)

    i = i + 1

# Check Checksum (Last digit should be 0)
if ((sum1 + sum2) % 10) != 0:
    print("INVALID")


temp3 = pow(10, (i - 2))
first_digit = cc_number // temp3

# Amex check
if (i == 15):
    if (first_digit == 34 or first_digit == 37):
        print("AMEX")


elif (i == 13 or i == 16):

    # MC
    if (first_digit == 51 or
        first_digit == 52 or
        first_digit == 53 or
        first_digit == 54 or
        first_digit == 55):
        print("MASTERCARD")

    # VC
    if(first_digit // 10 == 4):
        print("VISA")


else:
    print("INVALID")
