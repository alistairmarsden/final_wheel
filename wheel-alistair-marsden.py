from config import maxrounds
from config import vowelcost
from config import finalprize
import random

players={0:{"name":"Player 1","roundtotal":0,"gametotal":0},
         1:{"name":"Player 2","roundtotal":0,"gametotal":0},
         2:{"name":"Player 3","roundtotal":0,"gametotal":0},
        }
round_num = 0
spin_num = 0
final_round = False
round_end = False
dictionary = []
wheel_list = []
round_word = ""
blank_word = []
vowels = {"a", "e", "i", "o", "u"}
round_status = ""
guessed_letters =[]
final_guess = []

def read_dictionary_file():
    global dictionary
    d = open(r'data\dictionary.txt')
    dictionary = [x.strip() for x in d.readlines()]
    d.close()
def read_wheel_txt_file():
    global wheel_list
    w = open(r'data\wheeldata.txt')
    wheel_list = [x.strip() for x in w.readlines()]
    w.close()
   
def game_setup():
    global wheel_list
    global dictionary
    print('This is Wheel of Fortune!')
    read_dictionary_file()
    read_wheel_txt_file()

def consonant():
    global guessed_letters
    valid = False
    while not valid:
        letter = input('Guess a consonant: ')
        if letter.isalpha() and letter not in vowels and letter not in guessed_letters:
            valid = True
        else:
            print('Please guess a new consonant')
    return letter

def vowel():
    valid = False
    while not valid:
        letter = input('Guess a vowel:')
        if letter.isalpha() and letter in vowels and letter not in guessed_letters:
            valid = True
        else:
            print('Guess a new vowel: ')
        return letter

def word_guess():
    valid = False
    while not valid:
        word = input('Guess the word: ')
        if word.isalpha():
            valid = True
        else:
            print('Guess another word: ')
    return word

def letter_prompt(letter, count):
    if count > 0:
        print(f'There are {count} {letter}(s)')
    else:
        print(f'There were no {letter}s')

def get_word():
    global dictionary
    round_word = random.choice(dictionary)
    round_underscore_word = '_' * (len(round_word))
    return round_word, round_underscore_word


def wof_round_setup():
    global players
    global round_word
    global blank_word
    global guessed_letters
    global round_num
    guessed_letters.clear()
    print(f'Round {round_num+1}')
    players[0].__setitem__("roundtotal", 0)
    players[1].__setitem__("roundtotal", 0)
    players[2].__setitem__("roundtotal", 0)
    initPlayer = random.choice(list(players.keys()))
    round_word, blank_word = get_word()
    return initPlayer

def spin_wheel(player_num):
    global wheel_list
    global players
    global vowels
    still_in_turn=False
    spin_value = random.choice(wheel_list)
    print(f'You spun {spin_value}') 
    if spin_value == "bankrupt":
        players[player_num]['roundtotal']=0
        print(f'Bankrupt! Your round total is now {players[player_num].get("roundtotal")}')
        still_in_turn = False
    elif spin_value == 'loseturn':
        print('You lost a turn')
        still_in_turn = False       
    else:
        spin_value = int(spin_value)
        guess = consonant()
        good_guess, count = guess_letter(guess, player_num)
        if good_guess:
            players[player_num].__setitem__("roundtotal", players[player_num].get("roundtotal")+ ((spin_value)*(count)))
            print(f'Player Totals: {players[player_num]}')
            still_in_turn = True
        if not good_guess:
            still_in_turn = False
        return still_in_turn

def guess_letter(letter, player_num):
    global players
    global blank_word
    global final_round
    global guessed_letters
    good_guess = False
    count = 0
    guessed_letters.append(letter)
    if letter in round_word:
        index = round_word.find(letter)
        blank_word = blank_word[:index] + letter + blank_word[index + 1:]
        if not final_round:
            print(f'Good job! {letter} was in the word')
            index = round_word.find(letter)
            blank_word = blank_word[:index] + letter + blank_word[index + 1:]
            count += 1
            print(blank_word)
            good_guess = True
    else:
        if not final_round:
            print(f'{letter} is not in the word.')
            good_guess = False
    return good_guess, count

def buy_vowel(player_num):
    global players
    global vowels
    if players[player_num]['roundtotal']>= vowelcost:
        guess = vowel()
        good_guess, letter = guess_letter(guess, player_num)
        if guess in round_word:
            print(f'{guess} was in the word')
            players[player_num]['roundtotal'] -= vowelcost
    else:
        print(f'You need at least {vowelcost} to purchase a vowel')
        good_guess = True

    return good_guess

def guess_word(player_num):
    global players
    global blank_word
    global round_word
    global round_end
    global final_guess
    global round_num
    word_guess=input('What is your guess for the word? ')
    if not final_round:
        if word_guess == round_word:
            print(f'You got it! The word was {round_word}')
            round_num += 1
            round_end = True
        else:
            print('That is not the word')
            round_end = False
    else:
        final_guess.append(word_guess)    
    return False   

def wofTurn(player_num):  
    global round_word
    global blank_word
    global players
    global round_end
    global round_status
    global round_num
    round_end = False
    still_in_turn = True
    spin_num = 0
    while still_in_turn:
        round_status = f"{players[player_num]['name']} is up"
        print(f'Guessed letters {guessed_letters}')
        print(blank_word)
        #print(round_word) #to make checking easier
        print(f'{round_status}')
        print('S = spin the wheel, B = buy a vowel, G = guess the word')
        choice = input('What would you like to do? ')    
        if(choice.strip().upper() == "S"):
            still_in_turn = spin_wheel(player_num)
            spin_num += 1
        elif(choice.strip().upper() == "B"):
            if spin_num > 0:
                still_in_turn = buy_vowel(player_num)
            else:
                print('You need to spin once before buying a vowel')
        elif(choice.upper() == "G"):
            still_in_turn = guess_word(player_num)
        else:
            print("Not a correct option") 
    if round_end:
        for i, x in enumerate(players):
            if i == player_num:
                players[i]['gametotal'] += players[i]['roundtotal']
            else:
                players[i]['gametotal'] += 0
    return round_end

def wof_round():
    global round_word
    global blank_word
    global round_status
    global players
    initPlayer = wof_round_setup()
    round_end = False
    while round_end == False:
        round_end = wofTurn(initPlayer)
        if initPlayer != 2:
            initPlayer += 1
        else:
            initPlayer = 0
    print('Game total:')
    round_status = ''
    for i, x in enumerate(players):
        round_status = f"{round_status}{players[i]['name']}: {players[i]['gametotal']}\n"
    print(f'{round_status}')
   
def wof_final_round():
    global round_word
    global blank_word
    global final_guess
    global final_round
    global guessed_letters
    win_player = 0
    amount = 0
    final_round= True
    guessed_letters.clear()
    for i, x in enumerate(players):
        if players[i]['gametotal'] > amount:
            win_player = i
            amount = players[i]['gametotal']
    print(f"Congrats to {players[win_player]['name']}")
    round_word, blank_word = get_word()
    print('Added letters R, S, T, L, N, E')
    for letter in {'r', 's', 't', 'l', 'n', 'e'}:
        guess_letter(letter, win_player)
        print (blank_word)
    final_letters = [None]*4
    for i in range(len(final_letters)):
        if i < len(final_letters) - 1:
            final_letters[i] = consonant()
        else:
            final_letters[i]= vowel()
    for letter in final_letters:
        guess_letter(letter, win_player)
    print(blank_word)
    #print(round_word) #makes it easier to check
    guess_word(win_player)
    if round_word in final_guess:
        print(f"Congrats! {players[win_player]['name']} won {finalprize}")
    else:
        print(f'You did not get the word\nThe word was {round_word}. Thank you for playing')

def main():
    game_setup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wof_round()
        else:
            print('Final Round')
            wof_final_round()

if __name__ == "__main__":
    main()