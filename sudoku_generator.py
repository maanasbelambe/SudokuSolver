from constraint import Problem, AllDifferentConstraint
import random

BOARD_POSITIONS = list(range(0, 81))
BOARD_SIZE = 9

#controls difficulty of board, keep below 81
ROUNDS_TO_REMOVE = 81

def is_valid(board, row, col, num):
    for i in range(BOARD_SIZE):
        if i == row:
            continue
        if board[i][col] == num:
            return False 
    for i in range(BOARD_SIZE):
        if i == col:
            continue
        if board[row][i] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(BOARD_SIZE // 3):
        for j in range(BOARD_SIZE // 3):
            if i == row and j == col:
                continue
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def pos_to_coord(position):
    row = position // 9
    col = position % 9
    return row, col

def get_valid_numbers(board, row, col):
    valid_numbers = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            valid_numbers.append(num)
    return valid_numbers

def is_solvable(board, row, col, num):
    board_copy = [row[:] for row in board]
    board_copy[row][col] = num
    if solve(board_copy):
        return True
    return False

def solve(board):
    if (find_empty(board) == None):
        return True
    row, col = find_empty(board)
    for i in range(1, 10):
        if is_valid(board, row, col, i):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def find_empty(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                return i, j
    return None

#generates a full valid sudoku board
def generate_board():
    board = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    remaining = [pos for pos in BOARD_POSITIONS]
    while len(remaining) > 0:
        position = random.choice(remaining)
        row, col = pos_to_coord(position)
        valid_numbers = get_valid_numbers(board, row, col)
        if len(valid_numbers) == 0: 
            print("Failed to generate")
            return False
        num = random.choice(valid_numbers)
        if (is_solvable(board, row, col, num)):
            board[row][col] = num
            remaining.remove(position)
    return board

def is_unique(board):
    problem = Problem()

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] != 0:
                problem.addVariable((i, j), [board[i][j]])
            else:
                problem.addVariable((i, j), range(1, 10))

    #ensures all positions in row and column are unique
    for i in range(BOARD_SIZE):
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for i in range(9)])
        problem.addConstraint(AllDifferentConstraint(), [(i, j) for j in range(9)])

    #ensures all positions in 3x3 subgrids are unique
    for i in range(0, BOARD_SIZE, 3):
        for j in range(0, BOARD_SIZE, 3):
            problem.addConstraint(AllDifferentConstraint(), [(i + x, j + y) for x in range(3) for y in range(3)])

    solutions = problem.getSolutions()

    return len(solutions) == 1

#removes positions from the board so that there is still a unique solution
def remove_numbers(board, rounds):
    board_copy = [row[:] for row in board]
    remaining = [pos for pos in BOARD_POSITIONS]

    for cell in range(rounds):
        position = random.choice(remaining)
        remaining.remove(position)
        row, col = pos_to_coord(position)

        original_value = board_copy[row][col]
        board_copy[row][col] = 0

        if not is_unique(board_copy):
            board_copy[row][col] = original_value

    return board_copy

board = generate_board()
print(board)
print(is_unique(board))
unsolved_board = remove_numbers(board, ROUNDS_TO_REMOVE)
print(is_unique(unsolved_board))
print(unsolved_board)