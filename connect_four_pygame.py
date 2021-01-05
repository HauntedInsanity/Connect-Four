import sys
import pygame

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

pygame.init()

size = width, height = 1260, 1260

# Get a size equivalent to the display's size
# monitor_size = pygame.display.Info()
# size = width, height = monitor_size.current_w, monitor_size.current_h - 50

screen = pygame.display.set_mode(size)

# Setting up font
pygame.font.init()
font = pygame.font.SysFont('calibri', int(width / 10) - 10)


# Creates a list of columns x rows size to hold pieces
def create_board(columns, rows):
    # Dynamically create a 2d list with the size of columns and rows
    board = []

    # Each row is a list in board, inside of the row is the amount of columns
    for r in range(rows):
        # Create a new list
        row = []
        # Add columns amount of spaces to the row
        for c in range(columns):
            row.append(" ")
        # Add the newly created row to the board
        board.append(row)
    return board


# Takes a board list as a parameter and prints it in a way
# that makes it look more like an actual connect four game
def print_board(board):
    print()
    for r in range(0, len(board)):
        # Print the column numbers along the top
        if r == 0:
            column_num = " "
            for c in range(len(board[r])):
                column_num += "{:^3} ".format(str(c + 1))
            print(column_num)

        # String to hold the visualization of the row
        row_visual = "| "

        for c in range(0, len(board[r])):
            row_visual += board[r][c] + " | "

        print(row_visual)

        # Print the column numbers along the bottom
        if r == len(board) - 1:
            column_num = " "
            for c in range(len(board[r])):
                column_num += "{:^3} ".format(str(c + 1))
            print(column_num)


def render_text(text, color, r_divider):
    # Clear whatever exists at that spot currently
    pygame.draw.rect(screen, BLACK, (0, 0, width, r_divider))
    label = font.render(text, 1, color)
    # Center the text to the middle portion at the top of the screen
    label_rect = label.get_rect(center=(width / 2, r_divider / 2 + 10))
    screen.blit(label, label_rect)
    pygame.display.update()


def render_board(board, color, turn, next_turn, turn_color, next_turn_color):
    column_count = len(board[0])
    # Adding a one for extra space to show the piece that is being placed
    row_count = len(board) + 1

    # Get the total number of space available to equally space out the rows and columns
    c_divider = int(width / column_count)
    r_divider = int(height / row_count)

    # height / 140 is an arbitrary value.
    radius = int(r_divider / 2 - height / 140)

    # Iterate through rows and columns (but not the top "row" since it is being used later)
    for r in range(row_count - 1):
        for c in range(column_count):
            # Draw a "rectangle" on the screen
            pygame.draw.rect(screen, color, (c * c_divider, r * r_divider + r_divider, c_divider, r_divider))

            # Inside of the "rectangle", draw a circle depending on what the list contains at that position
            if board[r][c] == turn:
                pygame.draw.circle(screen, turn_color,
                                   (int(c * c_divider + c_divider / 2),
                                    int(r * r_divider + r_divider + r_divider / 2)), radius)
            elif board[r][c] == next_turn:
                pygame.draw.circle(screen, next_turn_color,
                                   (int(c * c_divider + c_divider / 2),
                                    int(r * r_divider + r_divider + r_divider / 2)), radius)
            else:
                pygame.draw.circle(screen, BLACK,
                                   (int(c * c_divider + c_divider / 2),
                                    int(r * r_divider + r_divider + r_divider / 2)), radius)
    pygame.display.update()


# Gets valid user input and respond on the board
def play(board, board_color, turn, next_turn, turn_color, next_turn_color, needed_to_win):
    render_board(board, board_color, turn, next_turn, turn_color, next_turn_color)
    placement = -1
    placed_row = -1

    column_count = len(board[0])
    row_count = len(board) + 1
    c_divider = int(width / column_count)
    r_divider = int(height / row_count)

    while placement == -1:
        for event in pygame.event.get():
            # The window's X button is clicked
            if event.type == pygame.QUIT:
                sys.exit()
            # The mouse is moved
            if event.type == pygame.MOUSEMOTION:
                # Remove the existing circles
                pygame.draw.rect(screen, BLACK, (0, 0, width + r_divider, r_divider))
                mouse_x = event.pos[0]
                placement_check = int(mouse_x // c_divider)
                # If the board is smaller than the screen size,
                # the piece that follows the mouse may move outside of the valid spots for the board
                if placement_check >= len(board[0]):
                    continue

                # Draw a new circle
                pygame.draw.circle(screen, turn_color, (mouse_x, int(r_divider / 2)), int(r_divider / 2 - height / 140))

                pygame.display.update()
            # The mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse's x position on the screen
                mouse_x = event.pos[0]
                # Get the placement in the list by doing floor division
                placement = int(mouse_x // c_divider)

                # If the board is smaller than the screen size,
                # the user can click on a placement that is outside of the list causing an index error.
                if placement >= len(board[0]) or board[0][placement] != " ":
                    # Continue the while loop by changing placement back to -1
                    placement = -1
                    continue

                print(placement)
                # Change the color of the helper piece
                pygame.draw.rect(screen, BLACK, (0, 0, width + r_divider, r_divider))
                pygame.draw.circle(screen, next_turn_color, (mouse_x, int(r_divider / 2)),
                                   int(r_divider / 2 - height / 140))

                pygame.display.update()

    # Once the above loop is done, that means a piece can be placed

    # Place a piece in the bottom most row under the given column number
    for r in range(len(board) - 1, -1, -1):
        if board[r][placement] == " ":
            board[r][placement] = turn
            # Remember which row the piece was placed at
            placed_row = r
            break
        if r == 0 and board[r][placement] != " ":
            print("There is no space in this column!\n")
            # Recursive restart
            play(board, board_color, turn, next_turn, turn_color, next_turn_color, needed_to_win)

    render_board(board, board_color, turn, next_turn, turn_color, next_turn_color)

    # Create lists containing the pieces in different formations, to be used to check for wins in the end.
    '''
    *
     *
      *
    '''
    # Make a list of every piece to the top left and bottom right of the current piece
    decreasing = [turn]

    # Get top left pieces
    piece_r = placed_row - 1
    piece_c = placement - 1
    while piece_r > -1 and piece_c > -1:
        decreasing.insert(0, board[piece_r][piece_c])
        piece_r -= 1
        piece_c -= 1

    # Get bottom right pieces
    piece_r = placed_row + 1
    piece_c = placement + 1
    while piece_r < len(board) and piece_c < len(board[0]):
        decreasing.append(board[piece_r][piece_c])
        piece_r += 1
        piece_c += 1
    # print("Decreasing:", "".join(decreasing))

    '''
      *
     *
    *
    '''
    # Make a list of every piece to the top right and bottom left of the current piece
    increasing = [turn]

    # Get top right pieces
    piece_r = placed_row - 1
    piece_c = placement + 1
    while piece_r > -1 and piece_c < len(board[0]):
        increasing.append(board[piece_r][piece_c])
        piece_r -= 1
        piece_c += 1

    # Get bottom left pieces
    piece_r = placed_row + 1
    piece_c = placement - 1
    while piece_r < len(board) and piece_c > -1:
        increasing.insert(0, board[piece_r][piece_c])
        piece_r += 1
        piece_c -= 1
    # print("Increasing:", "".join(increasing))

    '''
    
    ***
    
    '''
    # Make a list of every piece to the left and right of the current piece
    horizontal = [turn]

    # Get left pieces
    piece_r = placed_row
    piece_c = placement - 1
    while piece_c > -1:
        horizontal.insert(0, board[piece_r][piece_c])
        piece_c -= 1

    # Get right pieces
    piece_r = placed_row
    piece_c = placement + 1
    while piece_c < len(board[0]):
        horizontal.append(board[piece_r][piece_c])
        piece_c += 1
    # print("Horizontal:", "".join(horizontal))

    '''
     *
     *
     *
    '''
    # Make a list of every piece above and below the current piece
    vertical = [turn]

    # Get above pieces
    piece_r = placed_row - 1
    piece_c = placement
    while piece_r > -1:
        vertical.insert(0, board[piece_r][piece_c])
        piece_r -= 1

    # Get bottom pieces
    piece_r = placed_row + 1
    piece_c = placement
    while piece_r < len(board):
        vertical.append(board[piece_r][piece_c])
        piece_r += 1
    # print("Vertical:", "".join(vertical))

    # Check for wins
    win = False
    if turn * needed_to_win in "".join(horizontal):
        if not win:
            print_board(board)
        print(turn, "gets a horizontal win!")
        render_text((turn + " gets a horizontal win!"), turn_color, r_divider)
        win = True
    if turn * needed_to_win in "".join(vertical):
        if not win:
            print_board(board)
        print(turn, "gets a vertical win!")
        render_text((turn + " gets a vertical win!"), turn_color, r_divider)
        win = True
    if turn * needed_to_win in "".join(increasing):
        if not win:
            print_board(board)
        print(turn, "gets an increasing diagonal win!")
        render_text((turn + " gets a diagonal win!"), turn_color, r_divider)
        win = True
    if turn * needed_to_win in "".join(decreasing):
        if not win:
            print_board(board)
        print(turn, "gets a decreasing diagonal win!")
        render_text((turn + " gets a diagonal win!"), turn_color, r_divider)
        win = True

    # Return after printing each type of win
    if win:
        return

    # The tie check should happen after a check for wins
    # since the board could be completely full as a player wins

    # Check for a tie if the piece that was just placed was within the top row
    if placed_row == 0:
        # Assume the top row is filled until proven otherwise
        top_filled = True
        # Iterate through the top row
        for i in range(len(board[0])):
            # If there is an empty space, then a tie has not happened yet,
            # and we can continue with the game
            if board[0][i] == " ":
                top_filled = False
                break
        # If top_filled remains True after a check was made, then a tie has occurred.
        if top_filled:
            print_board(board)
            print("The game ends in a tie!")
            render_text("The game ends in a tie!", turn_color, r_divider)
            return

    print_board(board)
    # Swap the player's turns
    play(board, board_color, next_turn, turn, next_turn_color, turn_color, needed_to_win)


# A standard Connect Four board is 7x6 (7 horizontal and 6 vertical)
standard = create_board(7, 6)
print_board(standard)
play(standard, BLUE, "X", "O", RED, YELLOW, 4)
# Waits three seconds before closing
pygame.time.wait(3000)

# Testing limits
# large = create_board(50, 50)
# print_board(large)
# play(large, BLUE, "O", "X", RED, YELLOW, 2)

