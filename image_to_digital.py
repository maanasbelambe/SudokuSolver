import image_process
import sudoku_gui
import cv2
import numpy as np
import pytesseract

image_filename = "sudoku_board.jpg" #capture_image()
image = cv2.imread(image_filename)
sudoku_board = image_process.preprocess_find_board(image)

def find_digit(cell):
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    denoised = cv2.medianBlur(thresholded, 3)
    
    digit = pytesseract.image_to_string(denoised, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
    digit = digit.strip()
    return int(digit) if digit.isdigit() else 0

cell_size = sudoku_board.shape[0] // 9
board_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

for i in range(9):
    for j in range(9):
        cell = sudoku_board[i * cell_size : (i + 1) * cell_size, j * cell_size : (j + 1) * cell_size]
        num = find_digit(cell)
        board_array[i][j] = num

print(board_array)

game = sudoku_gui.Game(board_array)
game.run()

#cv2.waitKey(0)
#cv2.destroyAllWindows()