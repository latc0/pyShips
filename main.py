import random
from enum import Enum

__author__ = 'latc0'


# 10x10 board
# ship1: length 2
# ships 2,3: length 3
# ship4: length 4
# ship5: length 5

class Ship(object):
    def __init__(self):
        self.ship_length = 0
        self.location = 0

    def set_length(self, num):
        self.ship_length = num

    def get_length(self):
        return self.ship_length

    def set_loc(self, loc):
        self.location = loc

    def get_loc(self):
        return self.location


aiShips = [Ship() for a in range(5)]
aiBoard = [int for b in range(100)]

playerShips = [Ship() for c in range(5)]
playerBoard = [int for d in range(100)]

placed = False
gameover = False


class ShipType(Enum):
    ai = 1
    player = 2


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


def go_right(ship_num, ship_type):
    ship = get_ship(ship_type)[ship_num - 1]
    board = get_board(ship_type)

    ship_length = ship.get_length()
    loc = ship.get_loc()
    end_of_row = (loc - (loc % 10)) + 9
    ship_end = loc + (ship_length - 1)

    if ship_end <= end_of_row:
        ok = True
        # check that there aren't other ships in the way
        for k in xrange(0, ship_length):
            if board[loc + k] != 0:
                ok = False
                break
        if ok is True:
            for k in xrange(0, ship_length):
                board[loc + k] = ship_num
            global placed
            placed = True
        else:
            go_left(ship_num, ship_type)
    else:
        go_left(ship_num, ship_type)


def go_left(ship_num, ship_type):
    ship = get_ship(ship_type)[ship_num - 1]
    board = get_board(ship_type)

    ship_length = ship.get_length()
    loc = ship.get_loc()
    start_of_row = loc - (loc % 10)
    if (loc - (ship_length - 1)) >= start_of_row:
        ok = True
        # check that there aren't other ships in the way
        for k in xrange(0, ship_length):
            if board[loc - k] != 0:
                ok = False
                break
        if ok:
            for k in xrange(0, ship_length):
                board[loc - k] = ship_num
            global placed
            placed = True
        else:
            go_down(ship_num, ship_type)
    else:
        go_down(ship_num, ship_type)


def go_down(ship_num, ship_type):
    ship = get_ship(ship_type)[ship_num - 1]
    board = get_board(ship_type)

    ship_length = ship.get_length()
    loc = ship.get_loc()
    loc_below = loc + ((ship_length - 1) * 10)  # get column <ship_length> rows below
    if loc_below < 100:
        ok = True
        # check that there aren't other ships in the way
        for k in xrange(0, ship_length):
            if board[loc + (10 * k)] != 0:
                ok = False
                break
        if ok:
            for k in xrange(0, ship_length):
                board[loc + (10 * k)] = ship_num
            global placed
            placed = True
        else:
            go_up(ship_num, ship_type)
    else:
        go_up(ship_num, ship_type)


def go_up(ship_num, ship_type):
    ship = get_ship(ship_type)[ship_num - 1]
    board = get_board(ship_type)

    ship_length = ship.get_length()
    loc = ship.get_loc()
    loc_above = loc - ((ship_length - 1) * 10)
    if loc_above >= 0:
        ok = True
        # check that there aren't other ships in the way
        for k in xrange(0, ship_length):
            if board[loc - (10 * k)] != 0:
                ok = False
                break
        if ok:
            for k in xrange(0, ship_length):
                board[loc - (10 * k)] = ship_num
            global placed
            placed = True
        else:
            ship.set_loc(random.randint(0, 99))
    else:
        ship.set_loc(random.randint(0, 99))


def show_board(ship_type):
    board = get_board(ship_type)
    for i in xrange(0, 100):
        if i % 10 == 0:
            print ''
            num = (i / 10) + 1
            if num is not 10:
                print num, ' |',
            else:
                print num, '|',
        if board[i] == 9:
            print 'H',
        elif board[i] == 8:
            print 'M',
        else:
            print(board[i]),
    print ''
    print '     -------------------'
    print '     A B C D E F G H I J'


def position_ships(ship_type):
    global placed
    placed = False
    for i in xrange(1, 6):
        while not placed:
            if i % 2 == 0:
                go_right(i, ship_type)
            else:
                go_left(i, ship_type)
        placed = False


def fill_with_zeroes(ship_type):
    board = get_board(ship_type)
    for i in xrange(0, 100):
        board[i] = 0


def create_ship(ship_num, loc, ship_type):
    ship = Ship()
    if ship_num == 1:
        ship.set_length(2)
    elif ship_num == 2:
        ship.set_length(3)
    else:
        ship.set_length(ship_num)

    ship.set_loc(loc)

    index = ship_num - 1
    get_ship(ship_type)[index] = ship


def show_player_shots():
    for i in xrange(0, 100):
        if i % 10 == 0:
            print ''
            num = (i / 10) + 1
            if num is not 10:
                print num, ' |',
            else:
                print num, '|',
        if aiBoard[i] == 9:
            print 'H',
        elif aiBoard[i] == 8:
            print 'M',
        else:
            print 0,
    print ''
    print '     -------------------'
    print '     A B C D E F G H I J'


def show_stats():
    for k in xrange(0, 2):
        if k is 0:
            board = aiBoard
            print 'AI stats',
        else:
            board = playerBoard
            print 'Player stats',
        hits = 0
        miss = 0
        for i in xrange(0, 100):
            val = board[i]
            if val is 9:
                miss += 1
            if val is 9:
                hits += 1
        count = hits + miss
        acc = (float(hits) / float(count)) * 100
        print ': shots: ', count, ' hits: ', hits, ' misses: ', miss, ' accuracy: ', acc, '%'


"""
    AI functions
"""


def create_ai_ships():
    random.seed()
    for i in xrange(1, 6):
        create_ship(i, random.randint(0, 99), ShipType.ai)


def create_ai_board():
    create_ai_ships()
    fill_with_zeroes(ShipType.ai)
    position_ships(ShipType.ai)


"""
    Player functions
"""


def create_player_ships():
    # A - J, 0 - 9
    ship_nums = ["first", "second", "third", "fourth", "fifth"]
    i = 0
    while i < 5:
        speech = "Enter location of the " + ship_nums[i] + " ship (A-J, 1-10, e.g. B4): "
        the_ship_loc = raw_input(speech)
        start_loc_index = get_index_from_loc(the_ship_loc)
        if start_loc_index != -1 and start_loc_index != -2:
            k = i + 1
            create_ship(k, start_loc_index, ShipType.player)
            i += 1
        else:
            print 'Invalid'


def create_player_board():
    create_player_ships()
    fill_with_zeroes(ShipType.player)
    position_ships(ShipType.player)
    show_board(ShipType.player)


"""
    Main
"""


# 9 for hit, 8 for miss

def get_index_from_loc(location):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    length = len(location)
    if length < 1 or length > 3:
        return -1
    letter = location[0]
    if letter == 'o':
        show_player_shots()
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


def get_user_opp(ship_type):
    if ship_type == ShipType.ai:
        return 'You'
    else:
        return 'Me'


def place_guess(index, ship_type_opp):
    # need to give opposite ship type so we can bomb opponent
    board = get_board(ship_type_opp)
    user = get_user_opp(ship_type_opp)
    if index is not -1 and index is not -2:
        if board[index] == 0:
            print user, ': Miss :('
            board[index] = 8
        elif board[index] is 9 or board[index] is 8:
            print user, ': Already targeted'
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
                    print 'Your shots'
                    show_player_shots()
                    show_stats()
                global gameover
                gameover = True

        # if ai turn, show ai's hits/misses on player board
        if ship_type_opp == ShipType.player:
            print 'Your board'
            show_board(ShipType.player)

    else:
        if index is not -2:
            print user, ': Invalid location'
        if ship_type_opp == ShipType.ai:
            # Get another turn
            player_turn()
        else:
            ai_turn()


def ai_turn():
    bomb_loc = random.randint(0, 99)
    place_guess(bomb_loc, ShipType.player)


def player_turn():
    loc = raw_input("\nEnter location to bomb: ")
    index = get_index_from_loc(loc)
    place_guess(index, ShipType.ai)


def play_game():
    global gameover
    if not gameover:
        player_turn()
    if not gameover:
        ai_turn()


def setup_game():
    create_player_board()
    create_ai_board()
    print '\nBoards are setup, let the games begin!'
    print 'Press \'o\' at any time to see your hits/misses'
    global gameover
    while not gameover:
        play_game()
    gameover = False
    print 'End'


setup_game()
