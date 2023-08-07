# SudokuSolver

Plans:

1 - create backtracking algorithm that allows for solving of sudoku puzzles, text-based

2 - implement as a gui

3 - add ability to scan sudoku puzzle using camera

ideas:

add ability to generate sudoku puzzles

not priorities:
add ability to put potential solutions in corners
add directions screen


1. Start with a complete, valid board (filled with 81 numbers).
2. Make a list of all 81 cell positions and shuffle it randomly.
3. As long as the list is not empty, take the next position from the list and remove the number from the related cell.
4. Test uniqueness using a fast backtracking solver. My solver is - in theory - able to count all solutions, but for testing uniqueness, it will stop immediately when it finds more than one solution.
    - solver should return whether there is one solution or more than one solution
5. If the current board has still just one solution, goto step 3 and repeat.
6. If the current board has more than one solution, undo the last removal (step 3), and continue step 3 with the next position from the list
7. Stop when you have tested all 81 positions.

This gives you not only unique boards, but boards where you cannot remove any more numbers without destroying the uniqueness of the solution.

Of course, this is only the second half of the algorithm. The first half is to find a complete valid board first (randomly filled!) It works very similar, but "in the other direction":

1. Start with an empty board.
2. Add a random number at one of the free cells (the cell is chosen randomly, and the number is chosen randomly from the list of numbers valid for this cell according to the SuDoKu rules).
3. Use the backtracking solver to check if the current board has at least one valid solution. If not, undo step 2 and repeat with another number and cell. Note that this step might produce full valid boards on its own, but those are in no way random.
4. Repeat until the board is completely filled with numbers.