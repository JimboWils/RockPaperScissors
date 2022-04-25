# Imports nessecary libraries
import cv2
from keras.models import load_model
import numpy as np
import time
import random

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#Initialises nessecary variables
loss = 'You lose!'
win = 'You win!'
draw = 'You tie!'
choices = ["Rock", "Paper", "Scissors", 'Nothing' ]
player_score = 0
computer_score = 0
outcome = ''
message = ''
message2 = 'To start the game, please press G'
scoreboard = ''
g_pressed = False
game_over = False

time_start = time.time()

#Defines function to compares computer and player choices and determines the outcome of the game
def get_outcome():

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
    
    else:
        outcome = "N/A"
    

    
    # Prints outcome of the game to the user
    if outcome == loss or outcome == win or outcome == draw: 
        print(f'You chose {player_choice} and the computer chose {computer_choice}. {outcome}')
        
    else:
        print(f'You entered {player_choice}, which is not Rock, Paper or Scissors. What a shame!' )
    

    return outcome

def timer():
    
    time_elapsed = time.time() - time_start
    time_left = 3 - int(time_elapsed)
    
    return time_left

while True: 
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
    image_np = np.array(resized_frame)
    normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
    data[0] = normalized_image
    prediction = model.predict(data)
    
    keypress = cv2.waitKey(1) & 0xFF

    
    time_left = timer()
    
    # Determines the players choice using the webcam model 
    if prediction[0][0] > 0.5:
        player_choice = choices[0]
    elif prediction[0][1] > 0.5:
        player_choice = choices[1]
    elif prediction[0][2] > 0.5:
        player_choice = choices[2]
    else:
        player_choice = choices[3]
       
    #Uses random module to make a choice for the computer
    rng = random.randint(0,2)
    computer_choice = choices[rng]
     
    
    
   
    #Starts countdown when G is pressed
    if keypress == ord('g') and g_pressed == False and player_score != 3 and computer_score != 3:
        g_pressed = True
        
        time_start = time.time()
        time_left = timer()
        

        
    #Displays countdown after keypress   
    if g_pressed == True and time_left > 0:
        message = f'Please display your choice in {time_left} '
        message2 = ''

    #Determines outcome and updates player score and shown messages once timer reaches 0
    elif g_pressed == True and time_left < 1:
        g_pressed = False
        outcome = get_outcome()
        
        
        if outcome == 'N/A':
           message = "Oh dear, you chose nothing. You can't fight nothing! "

        else: 
            message = f'You chose {player_choice} and the computer chose {computer_choice}. {outcome}'

            if outcome == loss:
                computer_score = computer_score + 1
            
            elif outcome == win:
                player_score = player_score + 1
        # Uses the return of the run_game function to update the user and computer scores

        if player_score != 3 and computer_score != 3:
            
            message2 = ('The game continues! Press G to play again.')
            

        else:
            game_over = True
            time_start = time.time()
            time_left = timer()
            
    #Displays final win/loss message and exit instructions
    if  game_over == True and time_left < 1:
        game_over = None
        message2 = 'Press Q to exit!' 

        if player_score == 3:
            message = 'You won 3 games and beat the computer. Well Done!'
            print('You won 3 games and beat the computer. Well Done!')
        else:
             message = "The computer won 3 games. You've been defeated by the machines :("
             print("The computer won 3 games. You've been defeated by the machines :(")
        
    #Displays ganme over timer    
    elif game_over == True and time_left > 0:
        message2 = (f'Please wait for the final result in {time_left}')
         
    #Quits game if Q keypress is detected
    if keypress == ord('q'):
        break

    # Sets computer and player scores to be displayed on webcame feed
    cv2.putText(frame, f'Player Score: {player_score}', (5, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.65, (0, 100, 0), 1)   
    cv2.putText(frame, f'Computer Score: {computer_score}', (5, 60), cv2.FONT_HERSHEY_TRIPLEX, 0.65, (34, 34, 178), 1)  

    # Sets the current messages to the user to be displayed on webcam feed
    cv2.putText(frame, message, (5, 420), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (237, 149, 100), 1)
    cv2.putText(frame, message2, (5, 450), cv2.FONT_HERSHEY_TRIPLEX, 0.6, (255, 144, 30), 1)

    # Displays messages and scores on webcam feed 
    cv2.imshow('frame', frame)

   
    
            
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()