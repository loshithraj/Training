import random

def play():

    print("\n1. Stone")
    print("2. Paper")
    print("3. Scissors")
    print("4. Exit")

    user = input("Enter number: ")

    if user == "4":
        print("Game Over")
        return

    if user != "1" and user != "2" and user != "3":
        print("Wrong input")
        play()   # recursion
        return

    computer = random.randint(1, 3)

    print("Computer number:", computer)

    if user == str(computer):
        print("Draw")
    elif user == "1" and computer == 3:
        print("You Win")
    elif user == "2" and computer == 1:
        print("You Win")
    elif user == "3" and computer == 2:
        print("You Win")
    else:
        print("Computer Wins")

    play()   # recursion again

play()
