BOARD_SIZE = 9

def find_empty(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 0:
                return i, j
    return None

def check_valid(board, row, col, num):
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

def solve(board):
    if (find_empty(board) == None):
        return True
    row, col = find_empty(board)
    for i in range(1, 10):
        if check_valid(board, row, col, i):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False

def print_board(board):
    row_count = 0
    col_count = 0
    for i in board:
        row_count += 1
        for j in i:
            col_count += 1
            if j == 0:
                print("_", end = " ")
            else:
                print(str(j), end = " ")
            if col_count % 3 == 0:
                print("  ", end = " ")
        print("\n")
        if row_count % 3 == 0:
            print("\n")

board = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
         [6, 8, 0, 0, 7, 0, 0, 9, 0],
         [1, 9, 0, 0, 0, 4, 5, 0, 0],
         [8, 2, 0, 1, 0, 0, 0, 4, 0],
         [0, 0, 4, 6, 0, 2, 9, 0, 0],
         [0, 5, 0, 0, 0, 3, 0, 2, 8],
         [0, 0, 9, 3, 0, 0, 0, 7, 4],
         [0, 4, 0, 0, 5, 0, 0, 3, 6],
         [7, 0, 3, 0, 1, 8, 0, 0, 0]]

#print_board(board)
#solve(board)
#print_board(board)