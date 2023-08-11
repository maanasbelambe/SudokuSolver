import pygame
import time
import sudoku_text

BOARD_SIZE = 9
CELL_SIZE = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

class Tile:
    def __init__(self, value, row, col):
        self.font = pygame.font.Font(None, 30)
        self.value = value
        self.row = row
        self.col = col
        self.rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.text = self.font.render(str(value), True, BLACK)
        self.text_rect = self.text.get_rect(center = self.rect.center)
        self.color = WHITE
    
    def set_value(self, value):
        self.value = value
        self.text = self.font.render(str(value), True, BLACK)
        self.text_rect = self.text.get_rect(center = self.rect.center)
    
    def set_color(self, color):
        self.color = color
    
class Board:
    def __init__(self, board_array):
        self.board = board_array
        self.solved_board = [row[:] for row in self.board]
        sudoku_text.solve(self.solved_board)
        
    def draw_board(self, screen):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell_value = self.board[i][j]
                tile = Tile(cell_value, i, j)
                pygame.draw.rect(screen, tile.color, tile.rect)

                if cell_value != 0:
                    screen.blit(tile.text, tile.text_rect)
        
        self.draw_grid(screen)
        pygame.display.update()

    def draw_grid(self, screen):
        for i in range(BOARD_SIZE + 1):
            start_pos = (i * CELL_SIZE, 0)
            end_pos = (i * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
            pygame.draw.line(screen, BLACK, start_pos, end_pos)

            start_pos = (0, i * CELL_SIZE)
            end_pos = (BOARD_SIZE * CELL_SIZE, i * CELL_SIZE)
            pygame.draw.line(screen, BLACK, start_pos, end_pos)
        
        pygame.display.update()

    def update_board(self, screen, tile):
        pygame.draw.rect(screen, tile.color, tile.rect)
        if tile.value != 0:
            screen.blit(tile.text, tile.text_rect)
        self.draw_grid(screen)
        pygame.display.update()

    def draw_solve_button(self, screen):
        button_rect = pygame.Rect(10, BOARD_SIZE * CELL_SIZE + 10, BOARD_SIZE * CELL_SIZE - 20, 60)
        pygame.draw.rect(screen, WHITE, button_rect)

        button_font = pygame.font.Font(None, 50)
        button_text = button_font.render("Solve", True, BLACK)
        button_text_rect = button_text.get_rect(center = button_rect.center)
        screen.blit(button_text, button_text_rect)

        pygame.display.update()

    def solve(self, screen):
        if (sudoku_text.find_empty(self.board) == None):
            return True
        row, col = sudoku_text.find_empty(self.board)
        for i in range(1, 10):
            if sudoku_text.check_valid(self.board, row, col, i):
                self.board[row][col] = i
                self.draw_board(screen)
                pygame.display.update()
                time.sleep(0.15)
                if self.solve(screen):
                    return True
                self.board[row][col] = 0
        return False

class Game:
    def __init__(self, board_array):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE * CELL_SIZE + 1, BOARD_SIZE * CELL_SIZE + 81))
        pygame.display.set_caption("Sudoku Solver")
        self.board = Board(board_array)

    def run(self):
        self.board.draw_board(self.screen)
        self.board.draw_solve_button(self.screen)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    solve_button_rect = pygame.Rect(10, BOARD_SIZE * CELL_SIZE + 10, BOARD_SIZE * CELL_SIZE - 20, 60)
                    if solve_button_rect.collidepoint(pos):
                        self.board.solve(self.screen)
                    else:
                        current_tile = self.get_tile(pos)
                        if current_tile:
                            self.update_board(current_tile)

            self.board.draw_grid(self.screen)
        pygame.quit()

    def get_tile(self, pos):
        row = pos[1] // CELL_SIZE
        col = pos[0] // CELL_SIZE
        if (row < BOARD_SIZE and col < BOARD_SIZE):
            return Tile(self.board.board[row][col], row, col)
        return None
    
    def update_board(self, tile):
        if tile.value == 0:
            tile.set_color(YELLOW)
            self.board.update_board(self.screen, tile)
            new_value = self.get_user_input()
            if new_value != self.board.solved_board[tile.row][tile.col] and new_value != 0:
                tile.set_color(RED)
                tile.set_value(new_value)
                self.board.update_board(self.screen, tile)
                time.sleep(2)
                new_value = 0
            tile.set_color(WHITE)
            tile.set_value(new_value)
            self.board.board[tile.row][tile.col] = new_value
            self.board.update_board(self.screen, tile)

    def get_user_input(self):
        self.board.draw_grid(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return 1
                    elif event.key == pygame.K_2:
                        return 2
                    elif event.key == pygame.K_3:
                        return 3
                    elif event.key == pygame.K_4:
                        return 4
                    elif event.key == pygame.K_5:
                        return 5
                    elif event.key == pygame.K_6:
                        return 6
                    elif event.key == pygame.K_7:
                        return 7
                    elif event.key == pygame.K_8:
                        return 8
                    elif event.key == pygame.K_9:
                        return 9
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return 0

#board_array = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 0]]

#game = Game(board_array)
#game.run()