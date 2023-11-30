import numpy as np
import math
import pygame
import sys

SHAPE = (204, 204, 255)
BACKGROUND = (76, 0, 153)

# the colours of players are set here, if we want to enlarge the number of players, we add a new colour and then copy the algorithm marked at the end of the file
# PLAYER_1 = (255, 0, 0)
PLAYER_1 = (255, 102, 178)
PLAYER_2 = (102, 102, 255)

# initializing the board size as a tuple
board_size: tuple() = (6,7)

ROW_COUNT = board_size[0]
COLUMN_COUNT = board_size[1]


# creating a board with custom size
def create_board(board_size: tuple()):
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


# placing a chip in a location on board, piece is a number of chip
def drop_piece(board, row, col, piece):
    board[row][col] = piece


# check whether the chip can be placed in this column
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


# return next available row number
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


# check whether the player won a game and stops it
def winning_move(board, piece):
    # check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


# displays a board
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, SHAPE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BACKGROUND, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, PLAYER_1, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, PLAYER_2, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


# creating a board with custom size
board = create_board(board_size=board_size)
print_board(board)
# the game is on
game_over = False

# initialize the turn number
turn = 0

# initalize pygame
pygame.init()

# define our screen size
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

# defines the size of a chip
RADIUS = int(SQUARESIZE / 2 - 10)

screen = pygame.display.set_mode(size)
# calling function draw_board again
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("helvetica", 60)

# while game is on display whose turn it is, at the beginning of the turn the player's turn is displayed before the mouse is moved
while not game_over:
    turn_text = myfont.render(f"Player {turn + 1}'s turn", 1, (255, 255, 255))
    text_x = 40
    text_y = 10
    screen.blit(turn_text, (text_x, text_y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # if the mouse is moved displaying the movement of a chip
        if event.type == pygame.MOUSEMOTION:

            pygame.draw.rect(screen, BACKGROUND, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PLAYER_1, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, PLAYER_2, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        # if the mouse is clicked - placing a chip in the nearest available spot
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BACKGROUND, (0, 0, width, SQUARESIZE))
            # the following process should be repeated for every extra player added to the game
            # ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 has won!", 1, PLAYER_1)
                        screen.blit(label, (40, 10))
                        game_over = True


            # ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))
                # in case there are more than 2 players last argument in drop_piece func should be increased (3,4,etc instead of 2)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 has won!", 1, PLAYER_2)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)
            #switching a turn to the next player

            turn += 1
            turn = turn % 2 #in case of more players the turn count should be changed accordingly (turn % 3 or another int)

            if game_over:
                pygame.time.wait(3000)