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
    copied_board = copy.deepcopy(gameboard)
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
        if copied_board[switcher.get(field)[0]][switcher.get(field)[1]] == 0:
            copied_board[switcher.get(field)[0]][switcher.get(field)[1]] = player
            return True, copied_board
        else:
            return False, copied_board[switcher.get(field)[0]][switcher.get(field)[1]]
    except:
        return False, gameboard


def check_one_left(gameboard, checked_player):
    new_board = copy.deepcopy(gameboard)
    row = 0
    element = 0
    while row < 3:
        while element < 3:
            if gameboard[row][element] == 0:
                new_board[row][element] = checked_player
                if check_for_3(new_board)[0]:
                    if checked_player == 1:
                        new_board[row][element] = 2
                    return new_board, True
                else:
                    new_board = copy.deepcopy(gameboard)
            element += 1
        row += 1
        element = 0
    return gameboard, False


def make_duo(gameboard, forbidden_fields = []):
    row = 0
    element = 0
    possibilities = []
    new_gameboard = copy.deepcopy(gameboard)
    while row < 3:
        while element < 3:
            if forbidden_fields != []:
                if row in forbidden_fields[0] and element in forbidden_fields[1]:       #genutzt bei Strategieprüfung
                    continue
            if new_gameboard[row][element] == 0:
                new_gameboard[row][element] = 2
            if check_one_left(new_gameboard, 2)[1]:
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
    if check_full_gameboard(gameboard):
        return False
    while True:
        field = random.randint(1, 9)
        new_board = change_gameboard(copy.deepcopy(gameboard), field, 2)[1]
        if change_gameboard(gameboard, field, 2)[0] is False:
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


def check_for_strategies(gameboard):
    new_board = copy.deepcopy(gameboard)
    hot_fields = []
    forbidden_fields = []
    for mittelfelder in [[2, 4], [2, 6], [4, 8], [6, 8]]:
        for mittelfeld in mittelfelder:
            if change_gameboard(new_board, mittelfeld, 2)[0]:
                continue
            elif change_gameboard(new_board, mittelfeld, 2)[0] is False:
                if change_gameboard(new_board, mittelfeld, 2)[1] == 1:
                    hot_fields.append(mittelfeld)
        if len(hot_fields) == 2:
            feld_zu_belegen = hot_fields[0] + hot_fields[1] - 5
            if change_gameboard(new_board, feld_zu_belegen, 2)[0]:
                return change_gameboard(new_board, feld_zu_belegen, 2)[1], True
        hot_fields = []

    for eckfelder in [1, 3, 7, 9]:
        if change_gameboard(new_board, eckfelder, 2)[0] is False:   # wenn ein Eckfeld belegt ist
            if change_gameboard(new_board, 5, 2)[0]:    # wenn das Feld in der Mitte frei ist
                forbidden_fields = [[0, 2], [0, 2]]
                return change_gameboard(new_board, 5, 2)[1], True, forbidden_fields
    return gameboard, False, False


def AI_move(gameboard, difficulty):
    if difficulty == 0:
        raise ValueError("Falscher Schwierigkeitswert")
    if check_full_gameboard(gameboard):
        return False
    if check_one_left(gameboard, 2)[1]:
        return check_one_left(gameboard, 2)[0]
    elif check_one_left(gameboard, 1)[1]:
        if difficulty == 1 and random.randint(0, 12) < 2:
            return check_one_left(gameboard, 1)[0]
        elif difficulty == 2 and random.randint(0, 3) < 2:
            return check_one_left(gameboard, 1)[0]
        elif difficulty == 3:
            return check_one_left(gameboard, 1)[0]
    if difficulty == 3 and check_for_strategies(gameboard)[1]:
        return check_for_strategies(gameboard)[0]
    if check_for_strategies(gameboard)[2] is not False:
        forbidden_fields = check_for_strategies(gameboard)[2]
    else:
        forbidden_fields = []
    if make_duo(gameboard)[1]:
        return make_duo(gameboard, forbidden_fields)[0]
    else:
        return make_random_move(gameboard)


#gameboard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
#gameboard = AI_move(gameboard, 3)
#print_gameboard(gameboard)


running = True
while running:
    gameboard = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    print("---TicTacToe by Julian Szigethy---")
    print("Moin! Bitte wähle die Schwierigkeit aus:")
    print("(1) Einfach")
    print("(2) Normal")
    print("(3) Unmöglich")
    print("Schreibe \"esc\" zum Beenden!")
    eingabe = ""
    while True:
        eingabe = input("Schwierigkeit: ")
        if eingabe in ["1", "2", "3"]:
            break
        elif eingabe == "esc":
            raise TimeoutError("Das Spiel wurde beendet. Bis bald.")
    difficulty = int(eingabe)
    print("-----------------------------------------------")
    print("Das Spielfeld gibst du ein, indem du eine Zahl von 1-9 eingibst.")
    print("Du bist Spieler X und spielst gegen den Bot O.")
    print("1  2  3\n4  5  6\n7  8  9")
    input("Verstanden? Drücke ENTER zum Starten!")
    game_running = True
    current_player = 1                  # Spieler 1 ist echt, Spieler 2 ist der Bot
    while game_running:
        if current_player == 1:
            print_gameboard(gameboard)
            print("Du bist am Zug!")
            eingabeschleife = True
            while eingabeschleife:
                try:
                    field_input = int(input("Gib das Feld ein: "))
                    if change_gameboard(copy.deepcopy(gameboard), field_input, 1)[0] is False:
                        print("Falsche Eingabe! Vielleicht ist das Feld belegt?")
                    else:
                        gameboard = change_gameboard(gameboard, field_input, 1)[1]
                        eingabeschleife = False
                except ValueError:
                    print("Fehlerhafte Eingabe, probiere es nochmal!")
            current_player = 2
        elif current_player == 2:
            print("Der Bot ist am Zug...")
            gameboard = AI_move(gameboard, difficulty)
            current_player = 1
        if check_for_3(gameboard)[0]:
            game_running = False
        elif check_full_gameboard(gameboard):
            game_running = False
    if check_for_3(gameboard)[1] == 1:
        print_gameboard(gameboard)
        print("Du hast gewonnen!")
    elif check_for_3(gameboard)[1] == 2:
        print_gameboard(gameboard)
        print("Du hast verloren!")
    elif check_full_gameboard(gameboard):
        print_gameboard(gameboard)
        print("Unentschieden!")
    input("")
