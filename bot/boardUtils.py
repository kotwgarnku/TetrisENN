"""These heuristics attempt to assess how favourable a given board is.
The board should already have the dummy 23rd row stripped out.
When the heuristic says "block" it means one individual cell of a stone.

How you weight the different heuristics is up to you.
Most are designed to indicate bad things, and so should have negative weights.
"""

from collections import namedtuple

Move = namedtuple('Move', ['x_pos', 'rotation', 'result'])


def get_possible_moves(stone, board):
    moves = []
    stone = stone
    for r in range(get_possible_rotations_count(stone)):
        for x in range(max_x_pos_for_stone(stone) + 1):
            y = intersection_point(x, stone, board)
            board = board_with_stone(board, x, y, stone)
            moves.append(Move(x, r, board))
        stone = rotate_clockwise(stone)
    return moves


def best_move(stone, board):
    return max(get_possible_moves(stone, board), key=lambda m: utility(m.result))


def utility(board):
    heuristics = {
        num_holes: -496,
        num_blocks_above_holes: 897,
        num_gaps: -19,
        max_height: -910,
        avg_height: -747,
        num_blocks: 174,
    }
    return sum([fun(board) * weight for (fun, weight) in heuristics.items()])


def get_possible_rotations_count(stone):
    stones = [stone]
    while True:
        stone = rotate_clockwise(stone)
        if stone in stones:
            return len(stones)
        stones.append(stone)


def rotate_clockwise(shape):
    return [ [ shape[y][x]
               for y in range(len(shape)) ]
             for x in range(len(shape[0]) - 1, -1, -1) ]


def max_x_pos_for_stone(stone):
    """The furthest position you can move stone to the right"""
    # 10 is a column number from the game
    return 10 - len(stone[0])


def intersection_point(x, stone, board):
    """Find the y coordinate closest to the top where stone will collide"""
    y = 0
    while not check_collision(board, stone, (x, y)):
        y += 1
    return y - 1


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False


def board_with_stone(board, x, y, stone):
    """Return new board with stone included"""
    return join_matrices(board, stone, (x, y))


def join_matrices(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1	][cx+off_x] += val
    return mat1


def _is_block(cell):
    return cell != 0

def _is_empty(cell):
    return cell == 0

def _holes_in_board(board):
    """A hole is defined as an empty space below a block.
    The block doesn't have to be directly above the hole for it to count.
    This function identifies any holes and returns them as a [(x,y)]
    """
    holes = []
    block_in_col = False
    for x in range(len(board[0])):
        for y in range(len(board)):
            if block_in_col and _is_empty(board[y][x]):
                holes.append((x, y))
            elif _is_block(board[y][x]):
                block_in_col = True
        block_in_col = False
    return holes

def num_holes(board):
    """Number of holes that exist on the board."""
    return len(_holes_in_board(board))

def num_blocks_above_holes(board):
    """Number of blocks that are placed above holes. Note that the block
    doesn't have to be directly above the hole, a stack of three blocks on
    top of a single hole will give a result of 3."""
    c = 0
    for hole_x, hole_y in _holes_in_board(board):
        for y in range(hole_y-1, 0, -1):
            if _is_block(board[y][hole_x]):
                c += 1
            else:
                break
    return c

def num_gaps(board):
    """Like holes, but horizontal. Discourages waiting for the magic I-beam piece.
    Need to find block-gap-block sequences. A wall can substitute for a block."""
    gaps = []
    sequence = 0 # 0 = no progress, 1 = found block, 2 = found block-gap, 3 = found block-gap-block (not used)
    board_copy = []

    # Make walls into blocks for simplicity
    for y in range(len(board)):
        board_copy.append([1] + board[y] + [1])

    # Detect gaps
    for y in range(len(board_copy)):
        for x in range(len(board_copy[0])):
            if sequence == 0 and _is_block(board_copy[y][x]):
                sequence = 1
            elif sequence == 1 and _is_empty(board_copy[y][x]):
                sequence = 2
            elif sequence == 2:
                if _is_block(board_copy[y][x]):
                    gaps.append(board_copy[y][x-1])
                    sequence = 1
                else:
                    sequence = 0

    return len(gaps)

def max_height(board):
    """Height of the highest block on the board"""
    for idx, row in enumerate(board):
        for cell in row:
            if _is_block(cell):
                return len(board) - idx-1

def avg_height(board):
    """Average height of blocks on the board"""
    total_height = 0
    for height, row in enumerate(reversed(board[1:])):
        for cell in row:
            if _is_block(cell):
                total_height += height
    return total_height / num_blocks(board)

def num_blocks(board):
    """Number of blocks that exist on the board."""
    c = 0
    for row in board:
        for cell in row:
            if _is_block(cell):
                c += 1
    return c

def get_stone_number(stone):
    # Long stone horizontal and vertical
    if stone == [[6, 6, 6, 6]]:
        return 10
    elif stone == [[6], [6], [6], [6]]:
        return 11

    # 'z' stone horizontal and vertical
    elif stone == [[3, 3, 0], [0, 3, 3]]:
        return 20
    elif stone == [[0, 3], [3, 3], [3, 0]]:
        return 21

    # mirrored 'z' stone horizontal and vertical
    elif stone == [[0, 2, 2], [2, 2, 0]]:
        return 30
    elif stone == [[2, 0], [2, 2], [0, 2]]:
        return 31

    # L stone horizontal and vertical
    elif stone == [[0, 0, 5], [5, 5, 5]]:
        return 40
    elif stone == [[5, 5], [0, 5], [0, 5]]:
        return 41
    elif stone == [[5, 5, 5], [5, 0, 0]]:
        return 42
    elif stone == [[5, 0], [5, 0], [5, 5]]:
        return 43


    # mirrored 'L' stone horizontal and clockwise rotations
    elif stone == [[4, 4], [4, 0], [4, 0]]:
        return 51
    elif stone == [[4, 0, 0], [4, 4, 4]]:
        return 52
    elif stone == [[0, 4], [0, 4], [4, 4]]:
        return 53
    elif stone == [[4, 4, 4], [0, 0, 4]]:
        return 54

    # square block:
    elif stone == [[7, 7], [7, 7]]:
        return 60

    # T block
    elif stone == [[1, 1, 1], [0, 1, 0]]:
        return 70
    elif stone == [[1, 0], [1, 1], [1, 0]]:
        return 71
    elif stone == [[0, 1, 0], [1, 1, 1]]:
        return 72
    elif stone == [[0, 1], [1, 1], [0, 1]]:
        return 73
    else:
        raise Exception("Unsuported stone: " + str(stone))

