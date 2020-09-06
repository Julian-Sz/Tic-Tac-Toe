import random
import copy


def print_X_part(row):
    x = "◼◼◻◼◼◻◻◼◻◻◼◼◻◼◼"
    print(x[row*5:(row+1)*5], end="")


def print_empty_part(row):
    e = "◻◻◻◻◻◻◻◻◻◻◻◻◻◻◻"
    print(e[row*5:(row+1)*5], end="")


def print_O_part(row):
    o = "◻◼◼◼◻◼◻◻◻◼◻◼◼◼◻"
    print(o[row*5:(row+1)*5], end="")


def print_gameboard(gameboard):
    for row in gameboard:
        for printrow in range(0, 3):
            for point in row:
                if point == 0:
                    print_empty_part(printrow)
                elif point == 1:
                    print_X_part(printrow)
                elif point == 2:
                    print_O_part(printrow)
                else:
                    print("ERROR! Falscher Wert im Spielbrett-Array!")
                print("    ", end="")
            print("")
        print("")


def check_for_3(gameboard):
    for row in gameboard:
        if row == [1, 1, 1] or row == [2, 2, 2]:
            return True, row[0]
    for i in range(0, 3):
        if gameboard[0][i] == gameboard[1][i] == gameboard[2][i] != 0:
            return True, gameboard[0][i]
    if gameboard[0][0] == gameboard[1][1] == gameboard[2][2] != 0:
        return True, gameboard[0][0]
    elif gameboard[2][0] == gameboard[1][1] == gameboard[0][2] != 0:
        return True, gameboard[2][0]
    return False, 0


def change_gameboard(gameboard, field, player):
    switcher = {
        1: [0, 0],
        2: [0, 1],
        3: [0, 2],
        4: [1, 0],
        5: [1, 1],
        6: [1, 2],
        7: [2, 0],
        8: [2, 1],
        9: [2, 2]
    }
    try:
        if gameboard[switcher.get(field)[0]][switcher.get(field)[1]] == 0:
            gameboard[switcher.get(field)[0]][switcher.get(field)[1]] = player
            return gameboard
        else:
            return False
    except:
        return False


def check_one_left(gameboard, player):
    new_board = copy.deepcopy(gameboard)
    row = 0
    element = 0
    while row < 3:
        while element < 3:
            if gameboard[row][element] == 0:
                new_board[row][element] = player
                if check_for_3(new_board)[0] is True:
                    return new_board, True
                else:
                    new_board = copy.deepcopy(gameboard)
            element += 1
        row += 1
        element = 0
    return gameboard, False


def make_duo(gameboard):
    row = 0
    element = 0
    possibilities = []
    new_gameboard = copy.deepcopy(gameboard)
    while row < 3:
        while element < 3:
            if new_gameboard[row][element] == 0:
                new_gameboard[row][element] = 2
            if check_one_left(new_gameboard, 2)[1] is True:
                possibilities.append([row, element])
            new_gameboard = copy.deepcopy(gameboard)
            element += 1
        element = 0
        row += 1
    if possibilities == []:
        return gameboard, False
    possibility_pos = random.randint(0, (len(possibilities) - 1))
    possibility = possibilities[possibility_pos]
    new_gameboard[possibility[0]][possibility[1]] = 2
    return new_gameboard, True


def make_random_move(gameboard):
    while(True):
        new_board = change_gameboard(gameboard, random.randint(1, 9), 2)
        if new_board is False:
            continue
        else:
            return new_board


def check_full_gameboard(gameboard):
    for row in gameboard:
        for element in row:
            if element != 0:
                continue
            elif element == 0:
                return False
    return True



def AI_move(gameboard, difficulty):
    #attempts_to_3 = 0
    #possibilities = []
    if check_full_gameboard(gameboard):
        return False
    if check_one_left(gameboard, 2)[1] is True:
        return check_one_left(gameboard, 2)[0]
    elif make_duo(gameboard)[1] is True:
        return make_duo(gameboard)[0]
    else:
        return make_random_move(gameboard)


gameboard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
#if check_for_3(gameboard)[0] == True:
#print("Gewonnen hat Spieler " + str(check_for_3(gameboard)[1]))
#elif check_for_3(gameboard)[0] == False: print("no winner")

running = True
while(running):
    print("---TicTacToe by Julian Szigethy---")
    print("Moin! Bitte wähle die Schwierigkeit aus:")
    print("(1) Einfach")
    print("(2) Normal")
    print("(3) Unmöglich")
    difficulty = int(input())
    print("Das Spielfeld gibst du ein, indem du eine Zahl von 1-9 eingibst.")
    print("Du bist Spieler X und spielst gegen den Bot O.")
    print("1  2  3\n4  5  6\n7  8  9")
    input("Verstanden? Drücke ENTER zum Starten!")
    game_running = True
    current_player = 1                  #Spieler 1 ist echt, Spieler 2 ist der Bot
    while(game_running):
        if current_player == 1:
            print_gameboard(gameboard)
            print("Du bist am Zug!")
            eingabeschleife = True
            while(eingabeschleife):
                field_input = int(input("Gib das Feld ein: "))
                if change_gameboard(copy.deepcopy(gameboard), field_input, current_player) is False:
                    print("Falsche Eingabe! Vielleicht ist das Feld belegt?")
                else:
                    gameboard = change_gameboard(gameboard, field_input, current_player)
                    eingabeschleife = False
            current_player = 2
        elif current_player == 2:
            print("Der Bot ist am Zug...")
            gameboard = AI_move(gameboard, difficulty)
            current_player = 1
        if check_for_3(gameboard)[0] is True:
            game_running = False
        elif check_full_gameboard(gameboard) is True:
            game_running = False
    if check_for_3(gameboard)[1] == 1:
        print("Du hast gewonnen!")
    elif check_for_3(gameboard)[1] == 2:
        print("Du hast verloren!")
    elif check_full_gameboard(gameboard) is True:
        print("Unentschieden!")
    input("")
