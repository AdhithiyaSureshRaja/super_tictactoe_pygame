import pygame
import sys

# ---------------- Pygame Initialization ---------------- #
pygame.init()
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Tic-Tac-Toe (Ultimate Tic-Tac-Toe)")
clock = pygame.time.Clock()

# Colors
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
RED = (200, 50, 50)
BLUE = (50, 50, 200)
HIGHLIGHT = (50, 200, 50, 100)

# ---------------- Game Variables ---------------- #
ROWS, COLS = 3, 3  # Big board
CELL_SIZE = WIDTH // (COLS * 3)  # Each small cell
small_board_size = 3
big_board = [[[0 for _ in range(small_board_size)] for _ in range(small_board_size)] for _ in range(ROWS*COLS)]
big_winner = [[0 for _ in range(COLS)] for _ in range(ROWS)]
current_player = 1  # 1 = RED, 2 = BLUE
next_board = None  # (row, col) of the small board to play in

# ---------------- Functions ---------------- #
def draw_board():
    screen.fill(WHITE)
    # Draw small boards
    for br in range(3):
        for bc in range(3):
            # Draw thick lines for big board
            pygame.draw.rect(screen, BLACK, (bc*CELL_SIZE*3, br*CELL_SIZE*3, CELL_SIZE*3, CELL_SIZE*3), 6)
            # Draw small grid
            for r in range(1, 3):
                pygame.draw.line(screen, BLACK,
                                 (bc*CELL_SIZE*3, br*CELL_SIZE*3 + r*CELL_SIZE),
                                 (bc*CELL_SIZE*3 + 3*CELL_SIZE, br*CELL_SIZE*3 + r*CELL_SIZE), 2)
                pygame.draw.line(screen, BLACK,
                                 (bc*CELL_SIZE*3 + r*CELL_SIZE, br*CELL_SIZE*3),
                                 (bc*CELL_SIZE*3 + r*CELL_SIZE, br*CELL_SIZE*3 + 3*CELL_SIZE), 2)
            # Draw moves
            small_index = br*3 + bc
            for sr in range(3):
                for sc in range(3):
                    val = big_board[small_index][sr][sc]
                    if val != 0:
                        center_x = bc*3*CELL_SIZE + sc*CELL_SIZE + CELL_SIZE//2
                        center_y = br*3*CELL_SIZE + sr*CELL_SIZE + CELL_SIZE//2
                        if val == 1:
                            pygame.draw.line(screen, RED, (center_x-20, center_y-20), (center_x+20, center_y+20), 5)
                            pygame.draw.line(screen, RED, (center_x+20, center_y-20), (center_x-20, center_y+20), 5)
                        else:
                            pygame.draw.circle(screen, BLUE, (center_x, center_y), 25, 5)

def get_board_cell(pos):
    x, y = pos
    big_col = x // (CELL_SIZE*3)
    big_row = y // (CELL_SIZE*3)
    small_x = x % (CELL_SIZE*3)
    small_y = y % (CELL_SIZE*3)
    small_col = small_x // CELL_SIZE
    small_row = small_y // CELL_SIZE
    return big_row, big_col, small_row, small_col

def check_small_winner(board):
    # Check rows, columns, diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    return 0

def check_big_winner():
    for i in range(3):
        if big_winner[i][0] == big_winner[i][1] == big_winner[i][2] != 0:
            return big_winner[i][0]
        if big_winner[0][i] == big_winner[1][i] == big_winner[2][i] != 0:
            return big_winner[0][i]
    if big_winner[0][0] == big_winner[1][1] == big_winner[2][2] != 0:
        return big_winner[0][0]
    if big_winner[0][2] == big_winner[1][1] == big_winner[2][0] != 0:
        return big_winner[0][2]
    return 0

def reset_game():
    global big_board, big_winner, current_player, next_board
    big_board = [[[0 for _ in range(3)] for _ in range(3)] for _ in range(9)]
    big_winner = [[0 for _ in range(3)] for _ in range(3)]
    current_player = 1
    next_board = None

# ---------------- Main Loop ---------------- #
running = True
game_over = False
while running:
    draw_board()
    if game_over:
        font = pygame.font.Font(None, 60)
        text = font.render(f"Player {winner} Wins! Press R to Restart", True, BLACK)
        screen.blit(text, (WIDTH//10, HEIGHT//2 - 30))
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            br, bc, sr, sc = get_board_cell(pygame.mouse.get_pos())
            small_index = br*3 + bc
            # Check if move allowed
            if (next_board is None or next_board == (br, bc)) and big_board[small_index][sr][sc] == 0 and big_winner[br][bc] == 0:
                big_board[small_index][sr][sc] = current_player
                # Check small winner
                w = check_small_winner(big_board[small_index])
                if w != 0:
                    big_winner[br][bc] = w
                # Check big winner
                winner = check_big_winner()
                if winner != 0:
                    game_over = True
                # Next board
                next_board = (sr, sc) if big_winner[sr][sc] == 0 else None
                current_player = 2 if current_player == 1 else 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
                game_over = False

    clock.tick(30)

pygame.quit()
sys.exit()
