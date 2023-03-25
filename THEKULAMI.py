import random

# Define global game state variables
blocks = [[(0, 0), (0, 1), (1, 0), (1, 1)],
          [(0, 2), (1, 2), (2, 2)],
          [(0, 3), (0, 4)],
          [(0, 5), (0, 6), (0, 7)],
          [(1, 3), (2, 3)],
          [(1, 4), (1, 5), (2, 4), (2, 5)],
          [(1, 6), (1, 7), (2, 6), (2, 7), (3, 6), (3, 7)],
          [(2, 0), (2, 1), (3, 0), (3, 1)],
          [(3, 2), (3, 3), (3, 4), (4, 2), (4, 3), (4, 4)],
          [(3, 5), (4, 5)],
          [(4, 0), (4, 1), (5, 0), (5, 1), (6, 0), (6, 1)],
          [(4, 6), (4, 7), (5, 6), (5, 7)],
          [(5, 2), (6, 2)],
          [(5, 3), (6, 3), (7, 3)],
          [(5, 4), (5, 5), (6, 4), (6, 5), (7, 4), (7, 5)],
          [(6, 6), (6, 7), (7, 6), (7, 7)],
          [(7, 0), (7, 1), (7, 2)]]

board_printout = ["+ - - - + - + - - - + - - - - - +",
                  "| 0   0 | 0 | 0   0 | 0   0   0 |",
                  "|       |   + - + - + - + - - - +",
                  "| 0   0 | 0 | 0 | 0   0 | 0   0 |",
                  "+ - - - +   |   |       |       |",
                  "| 0   0 | 0 | 0 | 0   0 | 0   0 |",
                  "|       + - + - + - + - +       |",
                  "| 0   0 | 0   0   0 | 0 | 0   0 |",
                  "+ - - - +           |   + - - - +",
                  "| 0   0 | 0   0   0 | 0 | 0   0 |",
                  "|       + - + - + - + - +       |",
                  "| 0   0 | 0 | 0 | 0   0 | 0   0 |",
                  "|       |   |   |       + - - - +",
                  "| 0   0 | 0 | 0 | 0   0 | 0   0 |",
                  "+ - - - + - +   |       |       |",
                  "| 0   0   0 | 0 | 0   0 | 0   0 |",
                  "+ - - - - - + - + - - - + - - - +"]

board_state = [[0 for i in range(8)] for j in range(8)]
player = 0
last_move = [(-1, -1), (-1, -1)]
turn_count = 0


def print_board():
    cnt = 0
    for board_printout_i in board_printout:
        for board_printout_ij in board_printout_i:
            if board_printout_ij.isdigit():
                print("{}".format(board_state[cnt//8][cnt % 8]), end='')
                cnt += 1
            else:
                print(board_printout_ij, end="")
        print()


def is_same_tile(coord1, coord2):
    return get_tile(coord1) == get_tile(coord2)


def get_tile(coord):
    if coord[0] == -1 and coord[1] == -1:
        return -1
    for idx, block in enumerate(blocks):
        for holes in block:
            if holes[0] == coord[0] and holes[1] == coord[1]:
                return idx


def get_valid_coords(player):
    valid_coords = []
    for i in range(8):
        for j in range(8):
            isvalid, _ = isvalid_move((i, j), player)
            if isvalid:
                valid_coords.append((i, j))
    return valid_coords


def isvalid_move(coord, player):
    if board_state[coord[0]][coord[1]] != 0:
        return False, 'invalid move: already occupied'
    elif last_move[1-player] != (-1, -1) and coord[0] != last_move[1-player][0] and coord[1] != last_move[1-player][1]:
        return False, 'invalid move: must be on same row or col'
    elif is_same_tile(coord, last_move[1-player]):
        return False, 'invalid move: must not be on the same tile on which opponent has just placed their marble'
    elif is_same_tile(coord, last_move[player]):
        return False, 'invalid move: must not be on the same tile on which you just placed your marble'
    else:
        return True, None

# Get the final scores of the game, player who has most marbles on a tile wins all the tile holes


def get_score():
    scores = [0, 0]
    for block in blocks:
        cnt = [0, 0]
        for holes in block:
            player = board_state[holes[0]][holes[1]]
            if player != 0:
                cnt[player-1] += 1
        if cnt[0] > cnt[1]:
            scores[0] += len(block)
        if cnt[1] > cnt[0]:
            scores[1] += len(block)
    return scores


# Define the main game loop
while True:
    # Check game end
    # Run out of marble
    if turn_count == 56:
        print('game end: run out of marble')
        break
    # Can a player plays a valid move
    valid_coords = get_valid_coords(player)
    if len(valid_coords) == 0:
        print('game end: no valid move for player')
        break

    # Display new round info
    print(get_score())
    print_board()
    print('Player', player + 1, 'turn.')

    # # Get the player's move input
    # row = int(input('Enter row: '))
    # col = int(input('Enter column: '))

    # Random the player output
    r = random.randint(0, len(valid_coords)-1)
    row, col = valid_coords[r]

    # Check if the move is valid
    isvalid, error = isvalid_move((row, col), player)

    if isvalid:
        board_state[row][col] = player + 1
        last_move[player] = (row, col)
        player = 1 - player
        turn_count += 1
    else:
        print(error)
