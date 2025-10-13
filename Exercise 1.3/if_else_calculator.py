a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))
operator = input("Enter an operator (+ -): ")

if operator == "+":
    print("The result is:", a + b)
elif operator == "-":
    print("The result is:", a - b)
else:
    print("Unknown operator. Please use + or -.")