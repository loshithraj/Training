class bank_account:
    def __init__(self):
        self.name=input("Enter your name:")
        self.age=int(input("Enter your age:"))
        self.amount=int(input("Enter your deposit:"))
    def display(self):
        print("Thanks for Opening Account in Our Bank ",self.name)
    
kaviya=bank_account()
print(kaviya.name)