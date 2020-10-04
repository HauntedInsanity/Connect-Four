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
    for r in range(0, len(board)):
        cell_space = 3
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


# Gets valid user input and respond on the board
def play(board, turn, needed_to_win):
    placement = input(turn + "'s turn. Please enter a column number: ")
    placed_row = -1
    # Check if the placement is numeric and within the board's size
    if placement.isnumeric() and 0 < int(placement) <= len(board[0]):
        # print("Nice.")
        pass
    else:
        print("That is not a valid placement!")
        # Recursive restart
        play(board, turn, needed_to_win)

    placement = int(placement) - 1
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
            play(board, turn, needed_to_win)

    # Check for a win
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

    # Check for wins within the lists
    if turn * needed_to_win in "".join(horizontal):
        print(turn, "gets a horizontal win!")
        return
    elif turn * needed_to_win in "".join(vertical):
        print(turn, "gets a vertical win!")
        return
    elif turn * needed_to_win in "".join(increasing):
        print(turn, "gets an increasing diagonal win!")
        return
    elif turn * needed_to_win in "".join(decreasing):
        print(turn, "gets a decreasing diagonal win!")
        return

    print_board(board)
    if turn == "X":
        play(board, "O", needed_to_win)
    else:
        play(board, "X", needed_to_win)


# A standard Connect Four board is 6x7 (6 vertical and 7 horizontal)
standard = create_board(7, 6)
print_board(standard)
play(standard, "X", 4)

# Testing limits
# large = create_board(999, 999)
# print_board(large)
# play(large, "O", 2)
