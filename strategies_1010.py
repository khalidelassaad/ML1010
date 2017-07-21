from board_1010 import *

def _board_copy_with_move_made(board, move):
    B = Board()
    B.copy(board)
    B.make_move(move)
    B.clear10()
    return B

### STRATEGY FUNCTIONS
def MOVESCORE_points(board, move):
    score = 0
    B = Board()
    B.copy(board)
    B.make_move(move)
    score += len(move.shape.blocks) + B.clear10()
    return score

def _density_scan_assess(s1, s2, s3, s4):
    WEIGHTS = [-6,6,4,3,2,-1]
    if s1 and not s2 and not s3 and s4:#Diagonal: -4
        score = -WEIGHTS[0]
        return score
    if not s1 and s2 and s3 and not s4:#Diagonal: -4
        score = -WEIGHTS[0]
        return score
    if s1 and s2 and s3 and s4:#Full: +4
        score = WEIGHTS[1]
        return score
    if not s1 and not s2 and not s3 and not s4:#Empty: +1
        score = WEIGHTS[2]
        return score
    if (s1 + s2 + s3 + s4) == 2:#2 along an edge
        score = WEIGHTS[3]
        return score
    if (s1 + s2 + s3 + s4) == 3:#3 in a corner: 22
        score = WEIGHTS[4]
        return score
    if (s1 + s2 + s3 + s4) == 1:#1 in a corner: -2
        score = -WEIGHTS[5]
        return score
    return 0

def _density_score_of_new_board(result_board):
    # In the 2x2 scan, the spaces are as follows.
    #   s1  s2
    #   s3  s4
    score = 0
    for x in range(9):
        for y in range(9):
            s1 = result_board.grid[x+0][y+0]
            s2 = result_board.grid[x+0][y+1]
            s3 = result_board.grid[x+1][y+0]
            s4 = result_board.grid[x+1][y+1]
            score += _density_scan_assess(s1, s2, s3, s4)
    return score

def MOVESCORE_density(board, move):
    B = _board_copy_with_move_made(board,move)
    return _density_score_of_new_board(B)

def _blocks_around_shape(shape):
    return_set = set()
    for block in shape.blocks:
        return_set.add((block[0]  ,block[1]+1))
        return_set.add((block[0]  ,block[1]-1))
        return_set.add((block[0]+1,block[1]  ))
        return_set.add((block[0]-1,block[1]  ))
    for block in shape.blocks:
        if block in return_set:
            return_set.remove(block)
    return return_set

def _percentage_filled(board, move):
    W_OFF_BOARD = 0.7
    W_FILLED = 1
    spots = _blocks_around_shape(move.shape)
    num_spots = len(spots)
    num_filled = 0
    for spot in spots:
        r = move.row+spot[0]
        c = move.col+spot[1]
        if c < 0 or c > 9 or r < 0 or r > 9:
            num_filled += W_OFF_BOARD
        elif board.grid[r][c]:
            num_filled += W_FILLED
    return num_filled/num_spots

def MOVESCORE_fit(board, move):
    score = _percentage_filled(board,move)*100
    return int(score)

def _is_cavity(board, x, y):
    main  = False
    up    = False
    down  = False
    left  = False
    right = False
    if board.grid[x][y] == 0:
        main = True
    if x == 9:
        down = True
    elif x == 0:
        up = True
    else:
        if board.grid[x+1][y]:
            down = True
        if board.grid[x-1][y]:
            up = True
    if y == 9:
        right = True
    elif y == 0:
        left = True
    else:
        if board.grid[x][y+1]:
            right = True
        if board.grid[x][y-1]:
            left = True
    return main and up and down and left and right

def _count_cavities(board):
    count = 0
    for x in range(10):
        for y in range(10):
            if _is_cavity(board,x,y):
                count += 1
    return count

def MOVESCORE_cavity(board, move):
    old_cavities = _count_cavities(board)
    B = _board_copy_with_move_made(board, move)
    new_cavities = _count_cavities(B)
    return old_cavities - new_cavities

def _is_fragment(board, x, y):
    main  = False
    up    = False
    down  = False
    left  = False
    right = False
    if board.grid[x][y] == 1:
        main = True
    if x == 9:
        down = True
    elif x == 0:
        up = True
    else:
        if board.grid[x+1][y] == 0:
            down = True
        if board.grid[x-1][y] == 0:
            up = True
    if y == 9:
        right = True
    elif y == 0:
        left = True
    else:
        if board.grid[x][y+1] == 0:
            right = True
        if board.grid[x][y-1] == 0:
            left = True
    return main and up and down and left and right

def _count_fragments(board):
    count = 0
    for x in range(10):
        for y in range(10):
            if _is_fragment(board,x,y):
                count += 1
    return count

def MOVESCORE_fragment(board, move):
    old_fragments = _count_fragments(board)
    B = _board_copy_with_move_made(board, move)
    new_fragments = _count_fragments(B)
    return old_fragments - new_fragments

def _row_changes(grid, row):
    changes = 0
    current = grid[row][0]
    for x in range(1,10):
        if grid[row][x] != current:
            current = grid[row][x]
            changes += 1
    return changes

def _col_changes(grid, col):
    changes = 0
    current = grid[0][col]
    for x in range(1,10):
        if grid[x][col] != current:
            current = grid[x][col]
            changes += 1
    return changes

def _switches_score(grid):
    r_score = 0
    c_score = 0
    for x in range(10):
        r_score += _row_changes(grid, x)
    for x in range(10):
        c_score += _col_changes(grid, x)
    return c_score * r_score

def MOVESCORE_switches(board, move):
    B = _board_copy_with_move_made(board, move)
    return _switches_score(B.grid)


STRATEGIES = [
MOVESCORE_points,
MOVESCORE_density,
MOVESCORE_fit,
MOVESCORE_cavity,
MOVESCORE_fragment,
MOVESCORE_switches]