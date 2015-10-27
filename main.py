import random
from enum import Enum
from colorama import Fore

__author__ = 'latc0'

'''Classes'''


class Ship(object):
    def __init__(self):
        self.ship_length = 0
        self.location = 0
        self.orient = 'r'

    def set_length(self, num):
        self.ship_length = num

    def get_length(self):
        return self.ship_length

    def set_loc(self, loc):
        self.location = loc

    def get_loc(self):
        return self.location

    def set_orient(self, orient):
        self.orient = orient

    def get_orient(self):
        return self.orient


class ShipType(Enum):
    ai = 1
    player = 2


'''Globals'''
aiShips = [Ship() for a in range(5)]
aiBoard = [int for b in range(100)]

playerShips = [Ship() for c in range(5)]
playerBoard = [int for d in range(100)]

placed = False
gameover = False

'''Various getters'''


def get_board(ship_type):
    if ship_type == ShipType.player:
        return playerBoard
    else:
        return aiBoard


def get_ship(ship_type):
    if ship_type == ShipType.ai:
        return aiShips
    else:
        return playerShips


def get_length(ship_num):
    # Return length of ship
    if ship_num == 1:
        return 2
    elif ship_num == 2:
        return 3
    else:
        return ship_num


def get_user_opp(ship_type):
    if ship_type == ShipType.ai:
        return 'You'
    else:
        return 'Me'


def get_next_loc(orient, index, start_loc):
    if orient == 'u':
        return start_loc - (index * 10)
    elif orient == 'd':
        return start_loc + (index * 10)
    elif orient == 'l':
        return start_loc - index
    elif orient == 'r':
        return start_loc + index
    else:
        return 1337


def get_index_from_loc(location):
    """
        Returns -1 for invalid location
        or -2 if input is 'o'
    """

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    length = len(location)
    if length < 1 or length > 3:
        return -1
    letter = location[0]
    if letter == 'o':
        return -2
    if length is 1:
        return -1
    if letter.isupper():
        letter = letter.lower()

    if length == 3:
        if location[1] == '1' and location[2] == '0':
            number = 10
        else:
            return -1
    else:
        try:
            number = int(location[1])
            if number == 0:
                return -1
        except ValueError:
            return -1

    for i in xrange(0, 10):
        if letter == letters[i]:
            start_loc_index = i + ((number - 1) * 10)
            return start_loc_index
    return -1


'''Void'''


def show_board(ship_type, show_player_shots):
    board = get_board(ship_type)
    for i in xrange(0, 100):
        if i % 10 == 0:
            print ''
            num = (i / 10) + 1
            if num is not 10:
                print Fore.RESET + str(num), ' |',
            else:
                print Fore.RESET + str(num), '|',
        if board[i] == 9:
            print (Fore.GREEN + 'H'),
        elif board[i] == 8:
            print (Fore.RED + 'M'),
        elif board[i] != 0 and not show_player_shots:
            print(Fore.BLUE + str(board[i])),
        else:
            print (Fore.RESET + str(0)),
    print (Fore.RESET + '')
    print '     -------------------'
    print '     A B C D E F G H I J'


def fill_with_zeroes():
    for i in xrange(0, 100):
        aiBoard[i] = 0
        playerBoard[i] = 0


def create_ship(ship_num, loc, ship_type, orient):
    board = get_board(ship_type)
    ship_length = get_length(ship_num)
    for i in xrange(0, ship_length):
        board[get_next_loc(orient, i, loc)] = ship_num


def show_stats():
    for k in xrange(0, 2):
        if k is 0:
            board = playerBoard
            print 'AI stats',
        else:
            board = aiBoard
            print 'Player stats',
        hits = 0
        miss = 0
        for i in xrange(0, 100):
            val = board[i]
            if val is 8:
                miss += 1
            if val is 9:
                hits += 1
        count = hits + miss
        acc = (float(hits) / float(count)) * 100
        print ': hits:', hits, ' misses:', miss, ' accuracy:', "%.2f" % acc, '%'


def create_ai_ships():
    random.seed()
    i = 1
    orient = 'r'
    while i <= 5:
        index = random.randint(0, 99)
        if can_place_ship(index, i, orient):
            create_ship(i, index, ShipType.ai, orient)
            i += 1
        else:
            if orient == 'l':
                orient = 'r'
            else:
                orient = 'l'


def create_player_ships():
    ship_nums = ["first", "second", "third", "fourth", "fifth"]
    i = 1
    while i <= 5:
        speech = "Enter location of the " + ship_nums[i - 1] + " ship (e.g. B4): "
        the_ship_loc = raw_input(Fore.RESET + speech)
        start_loc_index = get_index_from_loc(the_ship_loc)

        if start_loc_index == -1:
            print (Fore.RED + 'Invalid')
        elif start_loc_index == -2:
            print (Fore.RED + 'No point now')
        else:
            orient = raw_input(Fore.RESET + "Which orientation? (u, d, l, r)")
            if orient_is_valid(orient) and can_place_ship(start_loc_index, i, orient):
                create_ship(i, start_loc_index, ShipType.player, orient)
                i += 1
            else:
                print (Fore.RED + 'Invalid')


'''Booleans'''


def can_be_placed(ship_length, start_loc, orient):
    for i in xrange(0, ship_length):
        if playerBoard[get_next_loc(orient, i, start_loc)] is not 0:
            return False
    return True


def can_place_ship(start_loc, ship_num, orient):
    ship_length = get_length(ship_num)
    orient = str(orient).lower()
    if can_be_placed(ship_length, start_loc, orient):
        if orient == 'u':
            above = start_loc - ((ship_length - 1) * 10)
            if above >= 0:
                return True
            else:
                return False
        elif orient == 'd':
            below = start_loc + ((ship_length - 1) * 10)
            if below < 100:
                return True
            else:
                return False
        elif orient == 'l':
            start = start_loc - (start_loc % 10)
            if (start_loc - (ship_length - 1)) >= start:
                return True
            else:
                return False
        elif orient == 'r':
            end = (start_loc - (start_loc % 10)) + 9
            if (start_loc + (ship_length - 1)) <= end:
                return True
            else:
                return False
    else:
        return False


def is_ship_still_there(ship_num, ship_type):
    board = get_board(ship_type)
    for i in xrange(0, 100):
        if board[i] == ship_num:
            return True
    return False


def all_ships_gone(ship_type):
    board = get_board(ship_type)
    for i in xrange(0, 100):
        val = board[i]
        if val is not 9 and val is not 8 and val is not 0:
            return False
    return True


def orient_is_valid(orient):
    poss = ['u', 'd', 'l', 'r']
    for i in xrange(0, 4):
        if orient == poss[i]:
            return True
    return False


'''Main'''


def place_guess(index, ship_type_opp):
    # need to give opposite ship type so we can bomb opponent
    board = get_board(ship_type_opp)
    user = get_user_opp(ship_type_opp)
    if board[index] == 0:
        print user, ': Miss :('
        board[index] = 8
    elif board[index] is 9 or board[index] is 8:
        print 'Already targeted'
    else:
        print user, ': Hit!'
        ship_num = board[index]
        board[index] = 9
        if not is_ship_still_there(ship_num, ship_type_opp):
            print user, ': Ship was destroyed!'
            if all_ships_gone(ship_type_opp):
                if user == 'Me':
                    print 'I won!'
                else:
                    print 'You won!'
                print '\nYour shots'
                show_board(ShipType.ai, True)
                print '\nMy shots'
                show_board(ShipType.player, False)
                show_stats()
                global gameover
                gameover = True


def ai_turn():
    bomb_loc = random.randint(0, 99)
    while playerBoard[bomb_loc] == 9 or playerBoard[bomb_loc] == 8:
        bomb_loc = random.randint(0, 99)
    place_guess(bomb_loc, ShipType.player)


def player_turn():
    loc = raw_input("\nEnter location to bomb: ")
    index = get_index_from_loc(loc)
    if index is -1:
        print 'Invalid'
    elif index is -2:
        show_board(ShipType.ai, True)
        player_turn()
    else:
        place_guess(index, ShipType.ai)


def play_game():
    global gameover
    while not gameover:
        player_turn()
        if not gameover:
            ai_turn()


def setup_game():
    fill_with_zeroes()
    create_ai_ships()
    create_player_ships()
    show_board(ShipType.player, False)
    print '\nBoards are setup, let the games begin!'
    print 'Press \'o\' at any time to see your hits/misses'
    play_game()


setup_game()
