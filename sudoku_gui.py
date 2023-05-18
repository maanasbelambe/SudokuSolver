import pygame
import time
import sudoku_text

BOARD_SIZE = 9
CELL_SIZE = 50

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Board:
    def __init__(self):
        self.board = [[0, 0, 0, 2, 6, 0, 7, 0, 1],
                      [6, 8, 0, 0, 7, 0, 0, 9, 0],
                      [1, 9, 0, 0, 0, 4, 5, 0, 0],
                      [8, 2, 0, 1, 0, 0, 0, 4, 0],
                      [0, 0, 4, 6, 0, 2, 9, 0, 0],
                      [0, 5, 0, 0, 0, 3, 0, 2, 8],
                      [0, 0, 9, 3, 0, 0, 0, 7, 4],
                      [0, 4, 0, 0, 5, 0, 0, 3, 6],
                      [7, 0, 3, 0, 1, 8, 0, 0, 0]]
        
    def draw_board(self, screen):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell_value = self.board[i][j]
                cell_rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, cell_rect)

                if cell_value != 0:
                    cell_font = pygame.font.Font(None, 30)
                    cell_text = cell_font.render(str(cell_value), True, BLACK)
                    cell_text_rect = cell_text.get_rect(center = cell_rect.center)
                    screen.blit(cell_text, cell_text_rect)

        for i in range(BOARD_SIZE + 1):
            start_pos = (i * CELL_SIZE, 0)
            end_pos = (i * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
            pygame.draw.line(screen, BLACK, start_pos, end_pos)

            start_pos = (0, i * CELL_SIZE)
            end_pos = (BOARD_SIZE * CELL_SIZE, i * CELL_SIZE)
            pygame.draw.line(screen, BLACK, start_pos, end_pos)

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
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((BOARD_SIZE * CELL_SIZE + 1, BOARD_SIZE * CELL_SIZE + 81))
        pygame.display.set_caption("Sudoku Solver")
        self.board = Board()

    def run(self):
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
            
            self.board.draw_board(self.screen)
            self.board.draw_solve_button(self.screen)

        pygame.quit()


game = Game()
game.run()
    