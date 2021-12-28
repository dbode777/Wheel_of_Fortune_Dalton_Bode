# Wheel of Fortune Game - Dalton Bode

# Download the phrases.json file into same directory as this program so the game can run properly.

# Courtesy of Scott Parcaz for the creation of the word-to-hint dictionary

# from bs4 import BeautifulSoup
# import requests
# import json

# dict = {}

# hints = ["around-the-house","before-and-after","book-title","classic-movie","classic-tv","college-life","event","family","fictional-character","fictional-place","food-and-drink","fun-and-games","headline","husband-and-wife","in-the-kitchen","landmark","living-thing","megaword","movie-quotes"]

# for y in hints:
#     counter = 0
#     html = requests.get("https://wheeloffortuneanswer.com/" + y + "/").text

#     soup = BeautifulSoup(html, 'lxml')
#     for s in soup.select('a'):
#         s.extract()
#     phrases = soup.find_all("td",class_ = "column-1")

#     for x in range(0,50):
#         phrases.pop(len(phrases) - 1)


#     for x in phrases:
#         if counter < 10 and True:
#             key = x.get_text().strip()
#             dict[key] = y
#             counter += 1
        
# file = open("phrases.json","w")
# file = json.dump(dict, file)

# Functions
import random
import json

def bank():
    """
    DOCSTRING: This function doesn't take in any parameters.
    The function returns a dictionary of exactly 3 players, in which their names are the keys and their bank totals are the values.
    """
    players = dict()
    
    while True:
        name = str(input("\nHello Contestant Number 1! What name would you like to go with for this game? "))
        if len(name) > 30:
            print("\nYour username needs to be less than or equal to 30 characters.")
            continue
        else:
            players[name]=0
            print(f"\nWelcome to the show {name}!")
            break
    while True:
        name = str(input("\nHello Contestant Number 2! What name would you like to go with for this game? "))
        if name in players:
            print("\nSorry, looks like someone has already taken that name")
            continue
        elif len(name) > 30:
            print("\nYour username needs to be less than or equal to 30 characters.")
            continue
        else:
            players[name]=0
            print(f"\nWelcome to the show {name}!")
            break
    while True:
        name = str(input("\nHello Contestant Number 3! What name would you like to go with for this game? "))
        if name in players:
            print("\nSorry, looks like someone has already taken that name")
            continue
        elif len(name) > 30:
            print("\nYour username needs to be less than or equal to 30 characters.")
            continue
        else:
            players[name]=0
            print(f"\nWelcome to the show {name}!")
            break
    return players

# Use wheel_spin() function, randomly generates an integer that chooses from the set/wheel options, returning the value the player will be playing with.
def wheel_spin(wheel_options):
    """
    DOCSTRING: This function has the following signatures: wheel_options.
    The function picks from an iterable object randomly and returns that value. 
    """
    return random.choice(wheel_options)

def new_phrase_and_hint(phrase_list, hint_list, used_phrase_list=[]):
    """
    DOCSTRING: This function has the following signatures: phrase_list, used_phrase_list (optional)
    The function returns a list, with the first index being the phrase chosen from a list of phrases, 
    and the second index value returns the corresponding hint for that phrase.
    
    It checks to see if the phrase has been used before, cycling through until a phrase that hasn't been used is chosen.
    For a 3 round game and a relatively small list of phrases, this shouldn't result in any major delays.
    """
    import random
    unused_phrase = False
    while unused_phrase != True:
        random_num = random.randint(0,len(phrase_list))
        phrase = phrase_list[random_num]
        hint = hint_list[random_num]
        if phrase not in used_phrase_list:
            used_phrase_list.append(phrase)
            unused_phrase = True
    return [phrase, hint]

def board(phrase):
    """
    DOCSTRING: This function has the following signatures: phrase
    The function returns a new board for each round. 
    
    A string is created from the input phrase, with a space between each character and a new line for each word.
    This design choice is done for readability.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
    new_board = list(phrase).copy()
    for i in range(0,len(phrase)):
        if phrase[i] == '\n':
            new_board[i] = ' \n'
        elif phrase[i] not in alphabet:
            new_board[i] = f" {phrase[i]}" # Fills in special characters
        else:
            new_board[i] = " _"
    combining_string = ""
    new_board = combining_string.join(new_board) 
    
    return new_board.lstrip()

def fill_board(guess, board, phrase):
    """
    DOCSTRING: This function has the following signatures: guess, board, phrase.
    The function returns a filled board wherever the guessed letter matches in the phrase.
    """
    # Updates your guess to add the guessed letter if it appears in the phrase. Otherwise, the board is returned unchanged.
    split_phrase = list(phrase)
    board_list = board.split(' ')
    
    for i in range(0,len(split_phrase)):
        if split_phrase[i] == '\n':
            continue
        elif split_phrase[i] == guess:
            board_list[i] = guess # Index of the board should match the index of the phrase
            
    filled_board = ' '.join(board_list)
    return filled_board

def only_vowels_left (phrase, board):
    """
    DOCSTRING: This function has the following signatures: phrase, board
    The function returns True if there are only vowels left, False if there are consonants still on the board.
    """
    vowels = ['A','E','I','O','U']
    remaining_letters = []
    new_board = board.split(' ')
    phrase_list = list(phrase)
    for i in range(0,len(phrase)):
        if phrase_list[i] != new_board[i]:
            remaining_letters.append(phrase_list[i])
    
    # Checks to see if any consonants are left
    for i in remaining_letters:
        if i not in vowels: # There's at least one consonant left
            return False
    
    print("Only vowels are left now!")
    return True # There are only vowels left
            
def guess_letter(phrase, board, hint, spin, current_player, initial_guess, buy_vowel, guessed_letters, players_bank, round_bank):
    """
    DOCSTRING: This function has the following signatures: phrase, board, hint, spin, current_player, initial_guess, buy_vowel, guessed_letters, players_bank, and round_bank
    The function returns True if the player guessed a letter correctly, False if incorrectly, or the string complete if they completed the phrase after guessing the remaining letter.
    It also checks if the phrase only has vowels left, whether a player can purchase a vowel, and whether its the start of their turn or a turn after guessing correctly.
    """
    vowels = ['A','E','I','O','U']
    # Checks to see if only vowels are left in the phrase.
    if only_vowels_left(phrase, board) != True:
        
        if initial_guess == 0: # Can only guess consonants
            global new_board
            new_board = board
            print("===============================================")
            print(f"The current board:\n{new_board}")
            print(f"\nHint: {hint}")
            print(f"Previously guessed letters:\n{guessed_letters}")
            print("===============================================")

            while True:
                con_guess = str(input(f"\nAlright {current_player}, go ahead and pick a consonant: ")).upper()
                if len(con_guess) != 1:
                    print("\nI see you're a little nervous!\nJust take your time and guess a single consonant, they don't bite.\nExcept for X's, those do bite.")                
                elif not con_guess.isalpha():
                    print("That's a fancy letter, but that's not a consonant from the English alphabet!\nPlease pick a consonant from the English alphabet.")
                elif con_guess in guessed_letters:
                    print("\nLooks like someone beat ya to the punch on that letter! Go ahead and guess a different consonant.")
                elif con_guess in vowels:
                    print("\nThat's a vowel, silly-billy.")
                else: # Valid input
                    if con_guess not in phrase:
                        print("\nThat letter is not in the phrase.")
                        guessed_letters.append(con_guess)
                        return False
                    else:
                        new_board = fill_board(con_guess, new_board, phrase)
                        guessed_letters.append(con_guess)
                        total_earnings = phrase.count(con_guess)*spin
                        round_bank[current_player] = round_bank[current_player] + total_earnings
                        print(f"That's correct! Your new round total ($) is: {round_bank[current_player]}.")
                        print(f"The current round totals ($) for all players are: {round_bank}")
                        print(f"The overall bank totals ($) for each player are: {players_bank}")
                        
                        if phrase == ''.join(new_board.split(' ')):
                            # All letters have been guessed in the phrase and the phrase has been completed.
                            print(f"\nCongratulations, that's all the letters in the phrase! {current_player} has won the round!")
                            print(f"\nThe phrase was: {phrase}")

                            # Gives the winning player the money they won from the round and $2000
                            players_bank.update({current_player : players_bank[current_player] + round_bank[current_player] +2000})
                            print(f"The overall bank totals ($) are: {players_bank}")
                            return 'complete'
                        
                        print("===============================================")
                        print(f"The new board is:\n{new_board}")
                        print("===============================================")
                        return True


        elif initial_guess == 1: # Can buy vowels

            print("===============================================")
            print(f"The current board:\n{new_board}")
            print(f"\nHint: {hint}")
            print(f"Previously guessed letters:\n{guessed_letters}")
            print("===============================================")
            
            if buy_vowel == True: 
                
                # If all vowels have been guessed, make sure the player doesn't get charged for it and force them to guess a consonant instead.
                guessed_vowels = []
                for i in vowels:
                    if i in guessed_letters:
                        guessed_vowels.append(i)
                if guessed_vowels == vowels:
                    print("\nAll the vowels have been guessed. You'll have to guess a consonant instead.")
                    while True:
                        con_guess = str(input(f"Alright {current_player}, go ahead and pick a consonant: ")).upper()
                        if len(con_guess) != 1:
                            print("\nI see you're a little nervous!\nJust take your time and guess a single consonant, they don't bite.\nExcept for X's, those do bite.")                
                        elif not con_guess.isalpha():
                            print("\nThat's a fancy letter, but that's not a consonant from the English alphabet!\nPlease pick a consonant from the English alphabet.")
                        elif con_guess in guessed_letters:
                            print("\nLooks like someone beat ya to the punch on that letter! Go ahead and guess a different consonant.")
                        elif con_guess in vowels:
                            print("\nThat's a vowel, silly-billy.")
                        else: # Valid input
                            if con_guess not in phrase:
                                print("\nThat letter is not in the phrase.")
                                guessed_letters.append(con_guess)
                                return False
                            else:
                                new_board = fill_board(con_guess, board, phrase)
                                guessed_letters.append(con_guess)
                                total_earnings = phrase.count(con_guess)*spin
                                round_bank[current_player] = round_bank[current_player] + total_earnings
                                print(f"That's correct! Your new round total ($) is: {round_bank[current_player]}.")
                                print(f"The current round totals ($) for all players are: {round_bank}")
                                print(f"The overall bank totals ($) for each player are: {players_bank}")

                                if phrase == ''.join(new_board.split(' ')):
                                    # All letters have been guessed in the phrase and the phrase has been completed.
                                    print(f"\nCongratulations, that's all the letters in the phrase! {current_player} has won the round!")
                                    print(f"\nThe phrase was: {phrase}")

                                    # Gives the winning player the money they won from the round and $2000
                                    players_bank.update({current_player : players_bank[current_player] + round_bank[current_player] +2000})
                                    print(f"The overall bank totals ($) are: {players_bank}")
                                    return 'complete'

                                print("===============================================")
                                print(f"The new board is:\n{new_board}")
                                print("===============================================")

                                return True
                else:
                    round_bank[current_player] = round_bank[current_player] - 250
                    while True:
                        vowel_guess = str(input(f"\nAlright {current_player}, go ahead and pick a vowel: ")).upper()
                        if len(vowel_guess) != 1:
                            print("\nI see you're a little nervous!\nJust take your time and guess a single vowel.")                
                            continue
                        elif not vowel_guess.isalpha():
                            print("\nThat's a fancy letter, but that's not a vowel from the English alphabet!\nPlease pick a vowel from the English alphabet.")
                            continue
                        elif vowel_guess in guessed_letters:
                            print("\nLooks like someone already answered that one! Go ahead and guess a different vowel.")
                            continue
                        elif vowel_guess not in vowels:
                            print("\nThat's not a vowel! Try again.")
                            continue
                        else: # Valid input for vowel
                            if vowel_guess not in phrase:
                                print("\nThat letter is not in the phrase.")
                                guessed_letters.append(vowel_guess)
                                return False
                            else:
                                new_board = fill_board(vowel_guess, board, phrase)
                                guessed_letters.append(vowel_guess)
                                print(f"That's correct! Your new round total ($) is: {round_bank[current_player]}.")
                                print(f"The current round totals ($) for all players are: {round_bank}")
                                print(f"The overall bank totals ($) for each player are: {players_bank}")

                                if phrase == ''.join(new_board.split(' ')):
                                    # All letters have been guessed in the phrase and the phrase has been completed.
                                    print(f"\nCongratulations, that's all the letters in the phrase! {current_player} has won the round!")
                                    print(f"\nThe phrase was: {phrase}")

                                    # Gives the winning player the money they won from the round and $2000
                                    players_bank.update({current_player : players_bank[current_player] + round_bank[current_player] +2000})
                                    print(f"The overall bank totals ($) are: {players_bank}")
                                    return 'complete'

                                print("===============================================")
                                print(f"The new board is:\n{new_board}")
                                print("===============================================")
                                return True
            
            elif buy_vowel == False:
                # Allows user to guess a consonant if they don't want to purchase a vowel.
                while True:
                    con_guess = str(input(f"Alright {current_player}, go ahead and pick a consonant: ")).upper()
                    if len(con_guess) != 1:
                        print("\nI see you're a little nervous!\nJust take your time and guess a single consonant, they don't bite.\nExcept for X's, those do bite.")                
                    elif not con_guess.isalpha():
                        print("\nThat's a fancy letter, but that's not a consonant from the English alphabet!\nPlease pick a consonant from the English alphabet.")
                    elif con_guess in guessed_letters:
                        print("\nLooks like someone beat ya to the punch on that letter! Go ahead and guess a different consonant.")
                    elif con_guess in vowels:
                        print("\nThat's a vowel, silly-billy.")
                    else: # Valid input
                        if con_guess not in phrase:
                            print("\nThat letter is not in the phrase.")
                            guessed_letters.append(con_guess)
                            return False
                        else:
                            new_board = fill_board(con_guess, board, phrase)
                            guessed_letters.append(con_guess)
                            total_earnings = phrase.count(con_guess)*spin
                            round_bank[current_player] = round_bank[current_player] + total_earnings
                            print(f"That's correct! Your new round total ($) is: {round_bank[current_player]}.")
                            print(f"The current round totals ($) for all players are: {round_bank}")
                            print(f"The overall bank totals ($) for each player are: {players_bank}")
                            
                            if phrase == ''.join(new_board.split(' ')):
                                # All letters have been guessed in the phrase and the phrase has been completed.
                                print(f"\nCongratulations, that's all the letters in the phrase! {current_player} has won the round!")
                                print(f"\nThe phrase was: {phrase}")

                                # Gives the winning player the money they won from the round and $2000
                                players_bank.update({current_player : players_bank[current_player] + round_bank[current_player] +2000})
                                print(f"The overall bank totals ($) are: {players_bank}")
                                return 'complete'
                            
                            print("===============================================")
                            print(f"The new board is:\n{new_board}")
                            print("===============================================")
                            
                            return True
    else:
        round_bank[current_player] = round_bank[current_player] - 250
        while True:
            vowel_guess = str(input(f"Alright {current_player}, go ahead and pick a vowel: ")).upper()
            if len(vowel_guess) != 1:
                print("\nI see you're a little nervous!\nJust take your time and guess a single vowel.")                
            elif not vowel_guess.isalpha():
                print("\nThat's a fancy letter, but that's not a vowel from the English alphabet!\nPlease pick a vowel from the English alphabet.")
            elif vowel_guess in guessed_letters:
                print("\nLooks like someone already answered that letter! Go ahead and guess a one.")
                continue
            elif vowel_guess not in vowels:
                print("\nThat's not a vowel! Try again.")
                continue
            else: # Valid input for vowel
                if vowel_guess not in phrase:
                    print("\nThat letter is not in the phrase.")
                    guessed_letters.append(vowel_guess)
                    return False
                else:
                    new_board = fill_board(vowel_guess, board, phrase)
                    guessed_letters.append(vowel_guess)
                    print(f"That's correct! Your new round total ($) is: {round_bank[current_player]}.")
                    print(f"The current round totals ($) for all players are: {round_bank}")
                    print(f"The overall bank totals ($) for each player are: {players_bank}")
                    
                    if phrase == ''.join(new_board.split(' ')):
                        # All letters have been guessed in the phrase and the phrase has been completed.
                        print(f"\nCongratulations, that's all the letters in the phrase! {current_player} has won the round!")
                        print(f"\nThe phrase was: {phrase}")

                        # Gives the winning player the money they won from the round and $2000
                        players_bank.update({current_player : players_bank[current_player] + round_bank[current_player] +2000})
                        print(f"The overall bank totals ($) are: {players_bank}")
                        return 'complete'
                    
                    print("===============================================")
                    print(f"The new board is:\n{new_board}")
                    print("===============================================")
                    return True
                
def guess_phrase(phrase, board, hint, current_player, guessed_letters, players_bank, round_bank):
    """
    DOCSTRING: This function has the following signatures: phrase, board, hint, current_player, guessed_letters, players_bank, round_bank.
    The function returns the string 'complete' if the player guesses the phrase correctly, False if the guess is incorrect.
    """
    while True:
        
        print("===============================================")
        print(f"The current board:\n{board}")
        print(f"\nHint: {hint}")
        print(f"Previously guessed letters:\n{guessed_letters}")
        print("===============================================")
        
        print("\nWarning: Make sure to use spaces between each word that appears on a new line.\n Ex. phrase:\n\"corn\non\nthe\ncob!\"\nanswer: \"corn on the cob!\"")
        guess = str(input("\nGo ahead and guess the phrase.\nYour answer is not case-sensitive, but may require you to enter the pre-filled special characters in your answer, if the board has them.\nThe phrase you guessed is: ")).upper()
        if guess.isnumeric():
            print("\nLooks like you accidentally typed in a number. Go ahead and guess again.")
            continue
        else:
            guess_list = list(guess)
            for i in range(0,len(guess_list)):
                if guess_list[i] == ' ':
                    guess_list[i] = '\n'
            guess = ''.join(guess_list)
            if  guess == phrase:
                print(f"\nThat's absolutely correct, congratulations! {current_player} has won the round!")
                
                players_bank.update({current_player : players_bank[current_player] + round_bank[current_player]+2000})
                print(f"\nThe new overall bank totals are: {players_bank}")
                
                return 'complete'
            
            elif guess != phrase:
                print("\nThat is incorrect!")
                return False

def spin(wheel_options, phrase, board, hint, current_player, guessed_letters, players_bank, round_bank):
    """
    DOCSTRING: This function has the following signatures: wheel_options, phrase, board, hint, current_player, guessed_letters, players_bank, round_bank.
    The function spins the wheel for players guessing 
    """ 
    spin = wheel_spin(wheel_options)
    print(f"You tile you landed on was: {spin}.")
    if not spin.isnumeric():
        if (spin == "BANKRUPT"):
            round_bank.update({current_player:0})
            print(f"\nSorry, {current_player}! Looks like you landed on a bankrupt tile! Better luck next time.")
            return False
        elif (spin == 'Lose a Turn'):
            print(f"\nOof! Looks like {current_player} loses a turn!")
            return False
        
    elif spin.isnumeric():
        player_correct = guess_letter(phrase, board, hint, int(spin), current_player, 0, False, guessed_letters, players_bank, round_bank)
        return player_correct
    
def player_turn(wheel_options, phrase, board, hint, initial_guess, current_player, guessed_letters, players_bank, round_bank):
    """
    DOCSTRING: This function has the following signatures: wheel_options, phrase, board, hint, initial_guess, current_player, guessed_letters, players_bank, round_bank.
    The function returns either True if the player guesses a letter correctly or False if they guess the phrase/letter in the phrase incorrctly. It returns 3 if they completed the phrase
    """ 
    print(f"\nIt's {current_player}'s turn!")

    # Checks to see if the player wants to guess the word
    print("=================================")
    print(f"The current board is:\n{board}")
    print(f"\nHint: {hint}")
    print(f"Previously guessed letters:\n{guessed_letters}")
    print(f"Round totals are: {round_bank}")
    print(f"Overall bank totals are {players_bank}")
    print("=================================")
    
    guess_phrase_check = str(input("Would you like to guess the phrase before spinning?\nGuessing correctly rewards you with $2000 dollars along with the money you've accrued from this round.\nEnter y for yes, or n for no: ")).lower()

    new_board = board # Allows for the board to be updated inside the while loop
    if guess_phrase_check == "yes" or guess_phrase_check == 'y':
        # Still need to do this function
        return guess_phrase(phrase, new_board, hint, current_player, guessed_letters, players_bank, round_bank) # Returns True or False

    elif guess_phrase_check == "no" or guess_phrase_check == 'n':

        if initial_guess == 0:

            player_correct = spin(wheel_options, phrase, new_board, hint, current_player, guessed_letters, players_bank, round_bank)
            return player_correct

        elif initial_guess == 1:

            # Checks to see if only vowels left, if so, checks if player has enough money to continue buying vowels.
            if only_vowels_left(phrase, new_board):
                if round_bank[current_player] < 250:
                    print("\nYou don't have enough money to purchase a vowel. Try your luck at guessing the phrase!")
                    return guess_phrase(phrase, new_board, hint, guessed_letters, current_player, players_bank, round_bank)
                else:
                    player_correct = guess_letter(phrase, new_board, hint, 0, current_player, 1, True, guessed_letters, players_bank, round_bank)
                    return player_correct

            elif not only_vowels_left(phrase,new_board):
                # Allows players to buy a vowel or make a second guess at a consonant.
                while True:
                    buy_vowel = str(input("\nWould you like to purchase a vowel for $250? Enter y for yes or n for no: ")).lower()
                    if buy_vowel == "y" or buy_vowel == "yes":
                        if round_bank[current_player] < 250:
                            print(f"\nSorry {current_player}, looks like you don't have the funds to purchase a vowel this round.")

                            # Forces them to spin and guess a consonant instead of repeating to ask question. 
                            player_correct = spin(wheel_options, phrase, new_board, hint, current_player, guessed_letters, players_bank, round_bank)
                            return player_correct

                        else:
                            player_correct = guess_letter(phrase, new_board, hint, 0, current_player, initial_guess, True, guessed_letters, players_bank, round_bank)
                            return player_correct

                    elif buy_vowel == "n" or buy_vowel == "no":
                        player_correct = spin(wheel_options, phrase, new_board, hint, current_player, guessed_letters, players_bank, round_bank)
                        return player_correct
                    else:
                        print("\nPlease enter y or n.")
                        return 'Try again'
    else:
        print("\nPlease enter y or n.")
        return 'Try again'

def final_player_check(players_bank):
    """
    DOCSTRING: This function has the following signatures: players_bank.
    The function returns the final player that had the highest total. If there's a tie, a player is randomly selected out of the winners.
    """ 
    final_player = ""
    
    # Finds the maximum value in the players_dictionary
    winners = max(players_bank.values())
    
    # Checks for ties
    player_tie_list = []
    for i in range(0,len(players_bank)):
        if list(players_bank.values())[i] == winners:
            player_tie_list.append(list(players_bank.keys())[i])
    final_player = random.choice(player_tie_list)
    
    return final_player
    
def final_round(final_player, phrase, board, hint, spin, guessed_letters, players_bank):
    """
    DOCSTRING: This function has the following signatures: final_player, phrase, board, hint, spin, guessed_letters, players_bank.
    The function conducts the final round. The letters r, s, t, l, n, and e are all prefilled. The player must then guess 3 consonants, then one vowel. 
    This fills the board and then gives the player a chance to guess the phrase. If they get it right, they win the final_wheel prize plus their earnings.
    If they don't, they walk away with just their earnings, also seeing what they could have won from the final wheel.
    """ 
    
    global new_board
    new_board = board
    vowels = ['A','E','I','O','U']
    
    # Pre fills the board with R, S, T, L, N, and E
    for i in ["R","S","T","L","N","E"]:
        new_board = fill_board(i,new_board,phrase)
        guessed_letters.append(i)
        
    print("===============================================")
    print(f"The current board:\n{new_board}")
    print(f"\nHint: {hint}")
    print(f"Previously guessed letters:\n{guessed_letters}")
    print("===============================================")
    
    # First consonant
    while True:
        con_guess = str(input(f"\nAlright {final_player}, go ahead and pick your first consonant: ")).upper()
        if len(con_guess) != 1:
            print("\nI see you're a little nervous!\nJust take your time and guess a single consonant, they don't bite.\nExcept for X's, those do bite.")                
        elif not con_guess.isalpha():
            print("\nThat's a fancy letter, but that's not a consonant from the English alphabet!\nPlease pick a consonant from the English alphabet.")
        elif con_guess in guessed_letters:
            print("\nLooks like already guessed that letter! Go ahead and guess a different consonant.")
        elif con_guess in vowels:
            print("\nThat's a vowel, silly-billy.")
        else: # Valid input
            if con_guess not in phrase:
                guessed_letters.append(con_guess)
                break
            else:
                guessed_letters.append(con_guess)
                new_board = fill_board(con_guess, new_board, phrase)
                break
                
    # Second consonant
    while True:
        con_guess = str(input(f"\nAlright {final_player}, go ahead and pick the second consonant: ")).upper()
        if len(con_guess) != 1:
            print("\nI see you're a little nervous!\nJust take your time and guess a single consonant, they don't bite.\nExcept for X's, those do bite.")                
        elif not con_guess.isalpha():
            print("\nThat's a fancy letter, but that's not a consonant from the English alphabet!\nPlease pick a consonant from the English alphabet.")
        elif con_guess in guessed_letters:
            print("\nLooks like you already guessed that letter! Go ahead and guess a different consonant.")
        elif con_guess in vowels:
            print("\nThat's a vowel, silly-billy.")
        else: # Valid input
            if con_guess not in phrase:
                guessed_letters.append(con_guess)
                break
            else:
                guessed_letters.append(con_guess)
                new_board = fill_board(con_guess, new_board, phrase)
                break  
    # Third consonant
    while True:
        con_guess = str(input(f"Alright {final_player}, go ahead and pick the third consonant: ")).upper()
        if len(con_guess) != 1:
            print("\nI see you're a little nervous!\nJust take your time and guess a single consonant, they don't bite.\nExcept for X's, those do bite.")                
        elif not con_guess.isalpha():
            print("\nThat's a fancy letter, but that's not a consonant from the English alphabet!\nPlease pick a consonant from the English alphabet.")
        elif con_guess in guessed_letters:
            print("\nLooks like you already guessed that letter! Go ahead and guess a different consonant.")
        elif con_guess in vowels:
            print("\nThat's a vowel, silly-billy.")
        else: # Valid input
            if con_guess not in phrase:
                guessed_letters.append(con_guess)
                break
            else:
                guessed_letters.append(con_guess)
                new_board = fill_board(con_guess, new_board, phrase)
                break
    # Vowel
    while True:
        vowel_guess = str(input(f"Alright {current_player}, go ahead and pick a vowel: ")).upper()
        if len(vowel_guess) != 1:
            print("\nI see you're a little nervous!\nJust take your time and guess a single vowel.")                
        elif not vowel_guess.isalpha():
            print("\nThat's a fancy letter, but that's not a vowel from the English alphabet!\nPlease pick a vowel from the English alphabet.")
        elif vowel_guess not in vowels:
            print("\nThat's not a vowel! Please guess a vowel.")
        elif vowel_guess in guessed_letters:
            print("\n'E' has already been given to you. Try again.")
        else: # Valid input for vowel
            if vowel_guess not in phrase:
                guessed_letters.append(vowel_guess)
                break
            else:
                guessed_letters.append(vowel_guess)
                new_board = fill_board(vowel_guess, new_board, phrase)
                break

    # Chance to guess the phrase.
    while True:
        print("===============================================")
        print(f"The current board:\n{new_board}")
        print(f"\nHint: {hint}")
        print(f"Previously guessed letters:\n{guessed_letters}")
        print("===============================================")

        print("\nWarning: Make sure to use a single space between each word that appears on a new line.\n Ex. phrase: \"corn\non\nthe\ncob!\"\nanswer: \"corn on the cob!\"")
        final_guess = str(input("Alright, time to guess the phrase.\nYour answer is not case-sensitive, but may require you to enter the pre-filled special characters in your answer, if the board has them.\nThe phrase you guessed is: ")).upper()
        if final_guess.isnumeric():
            print("Looks like you accidentally typed in a number somewhere. Go ahead and guess again.")
            continue
        else:
            final_guess_list = list(final_guess)
            for i in range(0,len(final_guess_list)):
                if final_guess_list[i] == ' ':
                    final_guess_list[i] = '\n'
            final_guess = ''.join(final_guess_list)
            if final_guess == phrase:
                print(f"\nThat's absolutely correct, congratulations! {final_player} won the final round!")
                print(f"\nLet's see what you what you won: ${players_bank[final_player]} from the previous rounds, and from this round: {spin}")
                break
            elif final_guess != phrase:
                print("\nThat is incorrect!")
                print(f"\nThe phrase we were looking for was: {phrase}")
                print(f"\nLet's see what you could have won: {spin}")
                print(f"\nWell {final_player}, you'll still be walking away with ${players_bank[final_player]}.")
                break

# Start Game
# Set-up players dictionary of player names to bank total 

players_bank = bank() # Returns dictionary of player names as keys and their bank totals as values.

player_names = list(players_bank.keys())
# Wheel options
wheel_options = ["BANKRUPT",str(2500),str(1000),str(900),str(700),str(600),str(650),str(500),str(700),"Lose a Turn",str(600),str(550),str(500),str(600),
                 "BANKRUPT",str(650),str(1000),str(700),"Lose a Turn",str(800),str(500),str(650),str(500),str(900)]

# Set-up lists of all phrases and hints that can be used in the game (get from a file)
phrases_hints_file = open("phrases.json",'rt')

phrases_to_hints_dictionary = json.load(phrases_hints_file)
phrases = list(phrases_to_hints_dictionary.keys())
hints = list(phrases_to_hints_dictionary.values())

# Makes sure phrases aren't reused.
used_phrase_list = []

# Creates new temporary bank for each player round totals 
temporary_bank = dict()
for x in range(0,len(player_names)):
    temporary_bank[player_names[x]] = 0

# Randomly pick the player to start
current_player = random.choice(player_names)

# First round conditions
completed = "incomplete"
i = 1

# First Round
while i == 1:

    print("====================================")
    print("              Round 1               ")
    print("====================================")
    # Set up phrase and hint for the round
    
    phrase_hint_combo = new_phrase_and_hint(phrases, hints, used_phrase_list)
    unchanged_phrase = phrase_hint_combo[0].upper()
    hint = phrase_hint_combo[1]
    
    # Set-up list guessed letters to check through.
    guessed_letters = []

    # Changes spaces between words in phrase to new lines (matches board layout)
    phrase = unchanged_phrase.replace(' ','\n')     

    # Set up board for contestants, along with hints
    new_board = board(phrase)
    
    while completed != "complete":

        # Let's each player take turns guessing the word/phrase
        if current_player == player_names[0]:
            player_correct = True
            initial_guess = 0
            while player_correct == True or player_correct != 'complete' or player_correct == 'Try again':
                player_correct = player_turn(wheel_options, phrase, new_board, hint, initial_guess, current_player, guessed_letters, players_bank, temporary_bank)
                completed = player_correct
                if player_correct == True:
                    initial_guess = 1
                    continue
                elif player_correct == 'Try again':
                    continue
                elif player_correct == False:
                    break
                
            current_player = player_names[1]

        elif current_player == player_names[1]:
            player_correct = True
            initial_guess = 0
            while player_correct == True or player_correct != 'complete' or player_correct == 'Try again':
                player_correct = player_turn(wheel_options, phrase, new_board, hint, initial_guess, current_player, guessed_letters, players_bank, temporary_bank)
                completed = player_correct
                if player_correct == True:
                    initial_guess = 1
                    continue
                elif player_correct == 'Try again':
                    continue
                elif player_correct == False:
                    break
                
            current_player = player_names[2]
                
        elif current_player == player_names[2]:
            player_correct = True
            initial_guess = 0
            while player_correct == True or player_correct != 'complete' or player_correct == 'Try again':
                player_correct = player_turn(wheel_options, phrase, new_board, hint, initial_guess, current_player, guessed_letters, players_bank, temporary_bank)
                completed = player_correct
                if player_correct == True:
                    initial_guess = 1
                    continue
                elif player_correct == 'Try again':
                    continue
                elif player_correct == False:
                    break
                
            current_player = player_names[0]

    # Goes to the next round
    i += 1

#Second Round
while i == 2:
    print("====================================")
    print("              Round 2               ")
    print("====================================")
    # Resets round totals to 0
    
    temporary_bank = dict()
    for x in range(0,len(player_names)):
        temporary_bank[player_names[x]] = 0
        
    # Set up phrase and hint for the round
    phrase_hint_combo = new_phrase_and_hint(phrases, hints, used_phrase_list)
    unchanged_phrase = phrase_hint_combo[0].upper()
    hint = phrase_hint_combo[1]
    
    guessed_letters = []

    # Changes spaces between words in phrase to new lines (matches board layout)
    phrase = unchanged_phrase.replace(' ','\n')     

    # Set up board for contestants, along with hints
    new_board = board(phrase)
    completed = 'incomplete'

    while completed != 'complete':

        # Let's each player take turns guessing the word/phrase
        if current_player == player_names[0]:
            player_correct = True
            initial_guess = 0
            while player_correct == True or player_correct != 'complete' or player_correct == 'Try again':
                player_correct = player_turn(wheel_options, phrase, new_board, hint, initial_guess, current_player, guessed_letters, players_bank, temporary_bank)
                completed = player_correct
                if player_correct == True:
                    initial_guess = 1
                    continue
                elif player_correct == 'Try again':
                    continue
                elif player_correct == False:
                    break
                
            current_player = player_names[1]

        elif current_player == player_names[1]:
            player_correct = True
            initial_guess = 0
            while player_correct == True or player_correct != 'complete' or player_correct == 'Try again':
                player_correct = player_turn(wheel_options, phrase, new_board, hint, initial_guess, current_player, guessed_letters, players_bank, temporary_bank)
                completed = player_correct
                if player_correct == True:
                    initial_guess = 1
                    continue
                elif player_correct == 'Try again':
                    continue
                elif player_correct == False:
                    break
                    
            current_player = player_names[2]

        elif current_player == player_names[2]:
            player_correct = True
            initial_guess = 0
            while player_correct == True or player_correct != 'complete' or player_correct == 'Try again':
                player_correct = player_turn(wheel_options, phrase, new_board, hint, initial_guess, current_player, guessed_letters, players_bank, temporary_bank)
                completed = player_correct
                if player_correct == True:
                    initial_guess = 1
                    continue
                elif player_correct == 'Try again':
                    continue
                elif player_correct == False:
                    break
            
            current_player = player_names[0]

    # Goes to the final round
    i += 1

# Checks to see who the final player is 
# If there's a tie, a player is randomly chosen out of the winners
final_player = final_player_check(players_bank)
print(f"{final_player} has moved onto the final round!")

# Final round   
while i == 3:
    
    print("====================================")
    print("            Final Round             ")
    print("====================================")
    
    # Set up phrase and hint for the round
    phrase_hint_combo = new_phrase_and_hint(phrases, hints, used_phrase_list)
    unchanged_phrase = phrase_hint_combo[0].upper()
    hint = phrase_hint_combo[1]
    
    guessed_letters = []

    # Changes spaces between words in phrase to new lines (matches board layout)
    phrase = unchanged_phrase.replace(' ','\n')     

    # Set up board for contestants, along with hints
    new_board = board(phrase)
    
    final_wheel_spin = ["$1000000","New Car","Fancy Hat","PS5 and $15000","XBOX One and $15000","Trip to Paris","Trip to Fiji",
                       "$30000","A $500 Amazon gift card","The Infinity Gauntlet","15 pairs of socks","New Furniture"]
    spin = wheel_spin(final_wheel_spin)
    
    final_round(final_player, phrase, new_board, hint, spin, guessed_letters, players_bank)
    i += 1

while i==4:
    print("Thanks for playing the Wheel of Fortune!")
    break