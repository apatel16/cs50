import cs50

height = 0
while True:
    height = cs50.get_int("Enter height: ")

    if height < 0 or height > 23:
        continue
    else:
        break

for i in range(height):

    spaces = height - i - 1;
    print(" " * spaces, end="")

    hashes = height - spaces
    print("#" * hashes, end="")

    print("  ", end="")

    print("#" * hashes, end="")
    print()
