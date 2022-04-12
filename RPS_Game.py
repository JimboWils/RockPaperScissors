def run_game():
    import random

    loss = 'You lose!'
    win = 'You win!'
    draw = 'You tie!'

    choices = ["Rock", "Paper", "Scissors", 'Nothing' ]
    rng = random.randint(0,2)
    computer_choice = choices[rng]
    #Uses random module to make a choice for the computer 

    player_choice = input("Please enter your choice (Rock, Paper or Scissors): ")
    #Gets players choice

    if player_choice == computer_choice :
        outcome = draw

    elif player_choice == 'Rock':
        if computer_choice == 'Paper':
            outcome = loss
        else:
            outcome = win

    elif player_choice == 'Paper':
        if computer_choice == 'Scissors':
            outcome = loss
        else:
            outcome = win

    elif player_choice == 'Scissors':
        if computer_choice == 'Rock':
            outcome = loss
        else:
            outcome = win
    #Compares computer and player choices and determines the outcome of the game

    

    if outcome == loss or outcome == win or outcome == draw:
        print(f'You chose {player_choice} and the computer chose {computer_choice}. {outcome}')
    else:
        print(f'You entered {player_choice}, which is not Rock, Paper or Scissors. What a shame!' )
    #Displays outcome of the game to the user

games = 0
    
while True:
    run_game()
    games = games + 1
    print(f'You have played {games} games.')
    
    if games == 3:
        break

    else:
        cont = input('Would you like to continue playing?[y/n]: ')

        if cont =='n':
            break
#Repeats the game up to 3 times if the user wishes to continue, and records the total number of games played
