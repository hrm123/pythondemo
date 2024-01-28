import math
import random

# treasure map
line1 = [" ", " ", " "]
line2 = [" ", " ", " "]
line3 = [" ", " ", " "]
treasureMap = [line1, line2, line3]
print("where do you want to hide your treasure?")  # example 'B3'
position = input()
letter = position[0].lower()
abc = ["a", "b", "c"]
letter_index = abc.index(letter)
number_index = int(position[1])-1
treasureMap[number_index][letter_index] = "X"
print(f"{line1}\n{line2}\n{line3}")

# rock paper scissors
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''
rockValue = 1
scissorsValue = 2
paperValue = 3
mapIndexToFigure = ["nothing", rock, scissors, paper]
mapIndexToName = ["nothing", "rock", "scissors", "paper"]

print("what do you choose (type 1 for Rock, 2 for scissors, 3 for paper)")
user_choice = int(input())
if 3 < user_choice < 0:
    print(f"You choose {mapIndexToFigure[user_choice]}")

    computer_choice = user_choice
    while computer_choice == user_choice:
        computer_choice = random.randint(1, 3)

    print(f"Computer choose {mapIndexToFigure[computer_choice]}")

    if user_choice == rockValue:
        if computer_choice == paperValue:
            print("computer wins by choosing paper")
        else:
            print(f"computer lost by choosing {mapIndexToName[computer_choice]}")

    if user_choice == scissorsValue:
        if computer_choice == rockValue:
            print("computer wins by choosing rock")
        else:
            print(f"computer lost by choosing {mapIndexToName[computer_choice]}")

    if user_choice == paperValue:
        if computer_choice == scissorsValue:
            print("computer wins by choosing scissor")
        else:
            print(f"computer lost by choosing {mapIndexToName[computer_choice]}")
else:
    print("invalid choice. You loose")

