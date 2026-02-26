def calculator():
    try:
        print("Calculator")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5.floor division")
        print("6.modulus")
        
        choose = input("Select operation (1/2/3/4/5/6): ")
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        
        if choose == '1':
            print("Result: ",{num1 + num2})
        elif choose == '2':
            print("Result:",{num1 - num2})
        elif choose == '3':
            print("Result:",{num1 * num2})
        elif choose == '4':
            print("Result:",{num1 / num2})
        elif choose == '5':
            print("Result:",{num1 // num2})
        elif choose == '6':
            print("Result:",{num1 % num2})
                
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        calculator()
calculator()