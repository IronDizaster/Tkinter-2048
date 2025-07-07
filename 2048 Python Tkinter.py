from tkinter import *
import random

# NO PYGAME
# NO DOWNLOADED LIBRARIES
# NO EXTRA ADDONS
# PURE PYTHON

root = Tk()
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900

BG_COLOR = 'gray'
BOARD_COLUMNS = 4
BOARD_ROWS = 4
BOARD_SQUARE_LENGTH = 125 # Pixels
ANIMATION_SPEED = 25 # Pixels per 10ms traveled
SPAWN_FRAMES = 15 # The more frames, the slower the speed (afterthought)
FONT = 'Arial'
font_size = BOARD_SQUARE_LENGTH // 4
LINE_WIDTH = 6
LINE_COLOR = '#474747'
BG_FILL = '#636363'
colors = {2: '#eee6db',
          4: '#ece0c8',
          8: '#efb27c',
          16: '#f39768',
          32: '#f27d62',
          64: '#f36142',
          128: '#eacf76',
          256: '#edcb67',
          512: '#ecc85a',
          1024: '#e7c257',
          2048: '#e8be4e'} # Colors for each number

canvas = Canvas(root, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, bg = BG_COLOR)
canvas.pack()

title = '2048'
can_move = True # When the game is won/lost or a player has initiated a move animation, this is set to False to prevent the player from doing actions
score = 0

def center_screen():
    screen_width = root.winfo_screenwidth()  # Width of the user screen
    screen_height = root.winfo_screenheight() # Height of the user screen

    # Starting X & Y window positions:
    x = (screen_width / 2) - (WINDOW_WIDTH / 2)
    y = (screen_height / 2) - (WINDOW_HEIGHT / 2)

    root.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
    tm = ' (IronDizaster ©)'
    root.title(title + tm)

def create_board(rows: int, cols: int, length: int) -> list[list[int]]:
    global font_size
    board_length = length * cols
    board_height = length * rows

    # offsets used to center the board so its centered
    x_offset = board_length / 2
    y_offset = board_height / 2

    y = WINDOW_HEIGHT / 2 - y_offset
    for i in range(rows):
        x = WINDOW_WIDTH / 2 - x_offset
        for j in range(cols):
            # TODO: have line width change with zoom level
            canvas.create_rectangle(x, y, x + length, y + length, width=LINE_WIDTH, tag='updatable', outline=LINE_COLOR, fill=BG_FILL)
            x += length
        y += length
    update_score(WINDOW_WIDTH / 2 - x_offset + font_size * 4, WINDOW_HEIGHT / 2 - y_offset - font_size)
    create_title(WINDOW_WIDTH / 2 + x_offset - font_size * 4, WINDOW_HEIGHT / 2 - y_offset - font_size * 1.5)
    return [[0] * cols for i in range(rows)]

def create_title(x, y):
    canvas.delete('title')
    canvas.create_text(x, y, text=f'2048', font=f'{FONT} {round(font_size * 1.5)} bold', tag='title', fill='white')
def update_score(x, y):
    global score
    canvas.delete('score')
    canvas.create_text(x, y, text=f'Score: {score}', font=f'{FONT} {font_size} bold', tag='score', fill='white')

def animate_square_movement(rows, cols, square_length):
    canvas.move('animatable', 10, 0)
    canvas.after(10, animate_square_movement)

def update_board(board: list[list[int]], length):
    global font_size
    rows = len(board)
    cols = len(board[0])

    board_length = length * cols
    board_height = length * rows

    # offsets used to center the board so its centered
    x_offset = board_length / 2
    y_offset = board_height / 2

    canvas.delete('updatable')
    y = WINDOW_HEIGHT / 2 - y_offset
    for i in range(rows):
        x = WINDOW_WIDTH / 2 - x_offset
        for j in range(cols):
            if board[i][j] == 0:
                canvas.create_rectangle(x, y, x + length, y + length, width=LINE_WIDTH, tag='updatable', outline=LINE_COLOR, fill=BG_FILL)
            else:
                canvas.create_rectangle(x, y, x + length, y + length, fill=colors[board[i][j]], width=LINE_WIDTH, tags='updatable', outline=LINE_COLOR)
                if board[i][j] > 4:
                    text_color = 'white'
                else:
                    text_color = '#3a3631'
                canvas.create_text(x + length / 2, y + length / 2, text=board[i][j], font=f'{FONT} {font_size} bold', tag='updatable', fill=text_color)
            x += length
        y += length
    update_score(WINDOW_WIDTH / 2 - x_offset + font_size * 4, WINDOW_HEIGHT / 2 - y_offset - font_size)

def validate_square(board: list[list[int]], spawn_row: int, spawn_col: int) -> bool:
    if board[spawn_row][spawn_col] != 0: # Space is not empty
        return False
    else:
        return True

def return_free_space(board: list[list[int]]) -> tuple:
    available_squares = [] # x, y coordinates (col, row)
    rows = len(board)
    cols = len(board[0])
    for i in range(rows):
        for j in range(cols):
            if board[i][j] == 0:
                available_squares.append((i, j))
    if len(available_squares) != 0:
        coord_tuple = random.choice(available_squares)
    else:
        coord_tuple = ()
    return coord_tuple


def create_square_on_board(board: list[list[int]], square_length: int):
    # 80% = 2
    # 20% = 4
    global can_move
    rows = len(board)
    cols = len(board[0])

    rng = random.randint(1, 10)
    if rng > 8:
        value = 4
    else:
        value = 2

    spawn_row = random.randint(0, rows - 1)
    spawn_col = random.randint(0, cols - 1)
    if validate_square(board, spawn_row, spawn_col) == False:
        # if square is invalid (i.e already has a number on it), make a list of all available spots in the grid and pick a random available square
        coord_tuple = return_free_space(board)
        if coord_tuple == (): return
        spawn_row = coord_tuple[0]
        spawn_col = coord_tuple[1]
    ##########################################

    board_length = square_length * cols
    board_height = square_length * rows
    x_offset = board_length / 2
    y_offset = board_height / 2

    x = WINDOW_WIDTH / 2 - x_offset + (square_length * spawn_col)
    y = WINDOW_HEIGHT / 2 - y_offset + (square_length * spawn_row)

    board[spawn_row][spawn_col] = value
    animations_on = True
    if animations_on:
        anim_length_increase = square_length / SPAWN_FRAMES / 2
        anim_length = anim_length_increase * SPAWN_FRAMES

        can_move = False # Disable moving while the animation is happening
        for i in range(SPAWN_FRAMES):
            canvas.create_rectangle(x + anim_length, 
                                    y + anim_length, 
                                    x - anim_length + square_length, 
                                    y - anim_length + square_length, 
                                    tag='animation',
                                    width=LINE_WIDTH,
                                    outline=LINE_COLOR,
                                    fill=colors[board[spawn_row][spawn_col]])
            canvas.create_text(x + square_length / 2, y + square_length / 2, text=value, font=f'{FONT} {round(font_size - anim_length / 3)} bold', tag='animation', fill='#3a3631')
            canvas.after(10)
            canvas.update()
            anim_length -= anim_length_increase
            canvas.delete('animation')
        can_move = True # Animation is finished - the player can move now

    canvas.create_rectangle(x, y, x + square_length, y + square_length, fill=colors[board[spawn_row][spawn_col]], width=LINE_WIDTH, outline=LINE_COLOR, tag='updatable')
    canvas.create_text(x + square_length / 2, y + square_length / 2, text=value, font=f'{FONT} {font_size} bold', tag='updatable', fill='#3a3631')

board = create_board(BOARD_ROWS, BOARD_COLUMNS, BOARD_SQUARE_LENGTH)

# Function to bypass not being able to bind functions with arguments in tkinter
def create_square_on_click(event):
    global board
    global BOARD_SQUARE_LENGTH
    create_square_on_board(board, BOARD_SQUARE_LENGTH)

def move_index(element_list: list, index_1: int, index_2: int):
    '''
    Moves element at index_1 to index_2
    '''
    element_list.insert(index_2, element_list.pop(index_1))

def compare_boards(board_1: list[list[int]], board_2: list[list[int]]) -> bool:
    '''
    Returns True or False depending on whether 2 boards are equal to each other.
    This function is used to determine whether squares have been moved or not.
    Board_1 and board_2 must have elements of the same length.
    '''
    rows = len(board_1)
    cols = len(board_1[0])
    for i in range(rows):
        for j in range(cols):
            if board_1[i][j] != board_2[i][j]:
                return False
    return True
    
def deepcopy_2D_list(twoD_list: list[list[int]]) -> list[list[int]]:
    '''
    Creates a deep copy of a 2D list (changing a value of the original 2D list will not change the value of the 
    returned list from this function).
    Used primarily for the compare_boards function.
    '''
    new_list = []
    rows = len(twoD_list)
    cols = len(twoD_list[0])
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(twoD_list[i][j])
        new_list.append(row)
    return new_list

def return_columns(board: list[list[int]]) -> list[list[int]]:
    global BOARD_SQUARE_LENGTH
    board_with_columns_to_rows = []
    rows = len(board)
    cols = len(board[0])
    for i in range(cols):
        column = []
        for j in range(rows):
            column.append(board[j][i])
        board_with_columns_to_rows.append(column)
    return board_with_columns_to_rows

def create_animatable_tile(x: float, y: float, num: int) -> tuple:
    global BOARD_SQUARE_LENGTH
    rect = canvas.create_rectangle(x, y, x + BOARD_SQUARE_LENGTH, y + BOARD_SQUARE_LENGTH, fill=colors[num], tag='phantom', width=LINE_WIDTH, outline=LINE_COLOR)
    text_color = '#3a3631' if num <= 4 else 'white'
    text = canvas.create_text(x + BOARD_SQUARE_LENGTH / 2, y + BOARD_SQUARE_LENGTH / 2, text = num, font = f'{FONT} {font_size} bold', fill=text_color, tag='phantom')
    return (rect, text)

def update_tile_coords(tile: list[float, float, int, int, int, float, float]):
    '''
    Updates tile x and y coordinates when animating tile movement
    '''
    tile_id = tile[2]
    tile[0] = canvas.coords(tile_id)[0]
    tile[1] = canvas.coords(tile_id)[1]

def move_phantom_tile(tile: list[float, float, int, int, int, float, float], direction: str):
    '''
    Moves the specified tile by 'ANIMATION_SPEED' pixels to the specified directions until it reaches its desired location
    '''
    tile_x = tile[0]
    tile_y = tile[1]
    tile_id = tile[2]
    tile_text_id = tile[3]
    end_x = tile[5]
    end_y = tile[6]
    if direction == 'left':
        if tile_x - ANIMATION_SPEED > end_x:
            canvas.move(tile_id, -ANIMATION_SPEED, 0)
            canvas.move(tile_text_id, -ANIMATION_SPEED, 0)
        else:
            if -(abs(tile_x - end_x)) != 0:
                canvas.move(tile_id, -(abs(tile_x - end_x)), 0)
                canvas.move(tile_text_id, -(abs(tile_x - end_x)), 0)
                create_animatable_tile(end_x, end_y, tile[4])
    
    elif direction == 'right':
        if tile_x + ANIMATION_SPEED < end_x:
            canvas.move(tile_id, ANIMATION_SPEED, 0)
            canvas.move(tile_text_id, ANIMATION_SPEED, 0)
        else:
            if (abs(tile_x - end_x)) != 0:
                canvas.move(tile_id, (abs(tile_x - end_x)), 0)
                canvas.move(tile_text_id, (abs(tile_x - end_x)), 0)
                create_animatable_tile(end_x, end_y, tile[4])

    elif direction == 'down':
        if tile_y + ANIMATION_SPEED < end_y:
            canvas.move(tile_id, 0, ANIMATION_SPEED)
            canvas.move(tile_text_id, 0, ANIMATION_SPEED)
        else:
            if (abs(tile_y - end_y)) != 0:
                canvas.move(tile_id, 0, (abs(tile_y - end_y)))
                canvas.move(tile_text_id, 0, (abs(tile_y - end_y)))
                create_animatable_tile(end_x, end_y, tile[4])
    
    elif direction == 'up':
        if tile_y - ANIMATION_SPEED > end_y:
            canvas.move(tile_id, 0, -ANIMATION_SPEED)
            canvas.move(tile_text_id, 0, -ANIMATION_SPEED)
        else:
            if -(abs(tile_y - end_y)) != 0:
                canvas.move(tile_id, 0, -(abs(tile_y - end_y)))
                canvas.move(tile_text_id, 0, -(abs(tile_y - end_y)))
                create_animatable_tile(end_x, end_y, tile[4])
    update_tile_coords(tile)

def create_phantom_tiles(previous_board: list[list[int]], board: list[list[int]], direction: str):
    global BOARD_SQUARE_LENGTH
    global font_size
    '''
    Phantom tiles are used to animate the movement of tiles on the board.
    They are created by comparing the previous board state with the current board state and determining
    where each tile should end up after the move.

    Args:
        previous_board (list[list[int]]): The board state before the move.
        board (list[list[int]]): The board state after the move.
        direction (str): The direction of the move ('left', 'right', 'up', 'down').
    '''

# DETAILED EXPLANATION : 
    # Phantom tiles are created with the following information:
    #     - The starting x and y coordinates of the tile
    #     - The tile ID
    #     - The text ID of the tile
    #     - The value of the tile
    #     - The ending x and y coordinates of the tile
    #     This information is stored in a list of lists, where each inner list represents a tile.
    #     The format of each tile list is:
    #     [tile_x, tile_y, tile_id, tile_text_id, tile_value, end_x, end_y]
    #     This function creates the phantom tiles and animates their movement to their end positions.

    #     Merging tiles is also handled in this function by checking if two tiles have the same value 
    #     and are in the same row or column.
    #     If they do, the end position of the first tile is updated to be the end position of the second tile,
    #     and the value of the first tile is doubled. The second tile is then removed from the list of tiles.
    #     This allows for smooth animations when tiles merge during a move.

    #     To prevent multiple merges from happening in a single move, a flag is used to track whether a merge 
    #     has just occurred.
    #     If a merge has just occurred, the function will not merge any more tiles until the next move.

    #     Depending on the direction of the move, the function will iterate through the rows or columns of the board
    #     to create the phantom tiles. For left and right moves, it iterates through the rows,
    #     and for up and down moves, it iterates through the columns. 

    #     The animation of the phantom tiles is done by moving them in the specified direction
    #     by a fixed speed (ANIMATION_SPEED) until they reach their end positions using the move_phantom_tile function.
    rows = len(board)
    cols = len(board[0])

    board_length = BOARD_SQUARE_LENGTH * cols
    board_height = BOARD_SQUARE_LENGTH * rows
    canvas.delete('phantom')
    canvas.delete('updatable')
    create_board(BOARD_ROWS, BOARD_COLUMNS, BOARD_SQUARE_LENGTH)
    # offsets used to center the board
    x_offset = board_length / 2
    y_offset = board_height / 2

    tile_list = [] 
    # A tile is a single list, which contains this information about the tile:
    # [tile_x, tile_y, tile_id, tile_text_id, tile_value, end_x, end_y]
    # (used only in animations)
    # Mark start squares
    if direction == 'left' or direction == 'right':
        for i, row in enumerate(previous_board):
            for j, num in enumerate(row):
                if num != 0:
                    x = WINDOW_WIDTH / 2 - x_offset + (BOARD_SQUARE_LENGTH * j)
                    y = WINDOW_HEIGHT / 2 - y_offset + (BOARD_SQUARE_LENGTH * i)
                    #canvas.create_rectangle(x, y, x+BOARD_SQUARE_LENGTH, y+BOARD_SQUARE_LENGTH, fill='green')
                    tile = create_animatable_tile(x, y, num)
                    #canvas.after(200)
                    #canvas.update()
                    tile_list.append([x, y, tile[0], tile[1], num])

        # Mark end squares
        tile_idx = 0
        for i, row in enumerate(board):
            for j, num in enumerate(row):
                if num != 0:
                    x = WINDOW_WIDTH / 2 - x_offset + (BOARD_SQUARE_LENGTH * j)
                    y = WINDOW_HEIGHT / 2 - y_offset + (BOARD_SQUARE_LENGTH * i)
                    #canvas.create_rectangle(x, y, x+BOARD_SQUARE_LENGTH, y+BOARD_SQUARE_LENGTH, fill='orange')
                    tile_list[tile_idx].append(x)
                    tile_list[tile_idx].append(y)
                    #canvas.after(200)
                    #canvas.update()
                    tile_idx += 1
    elif direction == 'down' or direction == 'up':
        # go by columns instead of by rows
        for i in range(len(previous_board[0])):
            for j in range(len(previous_board)):
                    num = previous_board[j][i]
                    if num != 0:
                        x = WINDOW_WIDTH / 2 - x_offset + (BOARD_SQUARE_LENGTH * i)
                        y = WINDOW_HEIGHT / 2 - y_offset + (BOARD_SQUARE_LENGTH * j)
                        tile = create_animatable_tile(x, y, num)
                        #canvas.create_rectangle(x, y, x+BOARD_SQUARE_LENGTH, y+BOARD_SQUARE_LENGTH, fill='green')
                        #canvas.after(200)
                        #canvas.update()
                        tile_list.append([x, y, tile[0], tile[1], num])

        tile_idx = 0
        for i in range(len(board[0])):
            for j in range(len(board)):
                    num = board[j][i]
                    if num != 0:
                        x = WINDOW_WIDTH / 2 - x_offset + (BOARD_SQUARE_LENGTH * i)
                        y = WINDOW_HEIGHT / 2 - y_offset + (BOARD_SQUARE_LENGTH * j)
                        #canvas.create_rectangle(x, y, x+BOARD_SQUARE_LENGTH, y+BOARD_SQUARE_LENGTH, fill='orange')
                        tile_list[tile_idx].append(x)
                        tile_list[tile_idx].append(y)
                        #canvas.after(200)
                        #canvas.update()
                        tile_idx += 1
    move_objects(tile_list, direction)

def update_end_merge_points(tile_list: list[list[float, float, int, int, int, float, float]], direction: str):
    '''
    Updates end points of tiles when animating due to the changes that may occur when merging
    '''
    has_just_merged = False
    
    if direction == 'left':
        for i in range(1, len(tile_list)):
            tile_x = tile_list[i][0]
            tile_y = tile_list[i][1]
            tile_value = tile_list[i][4]

            previous_tile_x = tile_list[i - 1][0]
            previous_tile_y = tile_list[i - 1][1]
            previous_tile_value = tile_list[i - 1][4]

            if tile_value == previous_tile_value and tile_y == previous_tile_y and has_just_merged == False:
                # Tiles should merge - they have the same value and are in the same row:
                tile_list[i][5] -= BOARD_SQUARE_LENGTH # end_x
                tile_list[i][4] *= 2 # tile_value
                has_just_merged = True
                for j in range(i + 1, len(tile_list)):
                    tile_y = tile_list[j][1]
                    previous_tile_y = tile_list[j - 1][1]
                    if tile_y == previous_tile_y:
                        tile_list[j][5] -= BOARD_SQUARE_LENGTH
                    else:
                        break
            else:
                has_just_merged = False

    elif direction == 'right':
        for i in range(len(tile_list) - 1, 0, -1):
            tile_x = tile_list[i][0]
            tile_y = tile_list[i][1]
            tile_value = tile_list[i][4]

            previous_tile_x = tile_list[i - 1][0]
            previous_tile_y = tile_list[i - 1][1]
            previous_tile_value = tile_list[i - 1][4]

            if tile_value == previous_tile_value and tile_y == previous_tile_y and has_just_merged == False:
                # Tiles should merge - they have the same value and are in the same row:
                tile_list[i - 1][5] += BOARD_SQUARE_LENGTH # end_x
                tile_list[i - 1][4] *= 2 # tile_value
                canvas.tag_raise(tile_list[i - 1][2])
                canvas.tag_raise(tile_list[i - 1][3])
                has_just_merged = True
                for j in range(i - 1, 0, -1):
                    tile_y = tile_list[j][1]
                    previous_tile_y = tile_list[j - 1][1]
                    if tile_y == previous_tile_y:
                        tile_list[j - 1][5] += BOARD_SQUARE_LENGTH
                    else:
                        break
            else:
                has_just_merged = False
                
    elif direction == 'down':
        for i in range(len(tile_list) - 1, 0, -1):
            tile_x = tile_list[i][0]
            tile_y = tile_list[i][1]
            tile_value = tile_list[i][4]

            previous_tile_x = tile_list[i - 1][0]
            previous_tile_y = tile_list[i - 1][1]
            previous_tile_value = tile_list[i - 1][4]

            if tile_value == previous_tile_value and tile_x == previous_tile_x and has_just_merged == False:
                # Tiles should merge - they have the same value and are in the same column:
                tile_list[i - 1][6] += BOARD_SQUARE_LENGTH # end_y
                tile_list[i - 1][4] *= 2 # tile_value
                canvas.tag_raise(tile_list[i - 1][2])
                canvas.tag_raise(tile_list[i - 1][3])
                has_just_merged = True
                for j in range(i - 1, 0, -1):
                    tile_x = tile_list[j][0]
                    previous_tile_x = tile_list[j - 1][0]
                    if tile_x == previous_tile_x:
                        tile_list[j - 1][6] += BOARD_SQUARE_LENGTH
                    else:
                        break
            else:
                has_just_merged = False

    if direction == 'up':
        for i in range(1, len(tile_list)):
            tile_x = tile_list[i][0]
            tile_y = tile_list[i][1]
            tile_value = tile_list[i][4]

            previous_tile_x = tile_list[i - 1][0]
            previous_tile_y = tile_list[i - 1][1]
            previous_tile_value = tile_list[i - 1][4]

            if tile_value == previous_tile_value and tile_x == previous_tile_x and has_just_merged == False:
                # Tiles should merge - they have the same value and are in the same column:
                tile_list[i][6] -= BOARD_SQUARE_LENGTH # end_y
                tile_list[i][4] *= 2 # tile_value
                has_just_merged = True
                for j in range(i + 1, len(tile_list)):
                    tile_x = tile_list[j][0]
                    previous_tile_x = tile_list[j - 1][0]
                    if tile_x == previous_tile_x:
                        tile_list[j][6] -= BOARD_SQUARE_LENGTH
                    else:
                        break
            else:
                has_just_merged = False
def move_objects(tile_list: list[list[float, float, int, int, int, float, float]], direction: str):
    '''
    Moves the phantom tiles in the specified direction until they reach their end positions.
    The end positions are updated based on the merging of tiles that may occur during the move.
    The function first updates the end positions of the tiles based on the merging of tiles,
    and then moves the tiles in the specified direction until they reach their end positions.
    Args:
        tile_list (list[list[float, float, int, int, int, float, float]]): A list of tiles to be moved.
            Each tile is represented as a list containing the following information:
            [tile_x, tile_y, tile_id, tile_text_id, tile_value, end_x, end_y]
        direction (str): The direction in which the tiles should be moved ('left', 'right', 'up', 'down').
    '''
    update_end_merge_points(tile_list, direction)
    times_moved = 1
    while times_moved != 0:
        times_moved = 0
        for tile in tile_list:
            tile_x = tile[0]
            tile_y = tile[1]
            end_x = tile[5]
            end_y = tile[6]
            if direction == 'left':
                if tile_x > end_x:
                    move_phantom_tile(tile, 'left')
                    times_moved += 1
            elif direction == 'right':
                if tile_x < end_x:
                    move_phantom_tile(tile, 'right')
                    times_moved += 1
            elif direction == 'down':
                if tile_y < end_y:
                    move_phantom_tile(tile, 'down')
                    times_moved += 1
            elif direction == 'up':
                if tile_y > end_y:
                    move_phantom_tile(tile, 'up')
                    times_moved += 1
        canvas.after(10)
        canvas.update()

    canvas.delete('phantom')


################################################
# MOVEMENT FUNCTIONS (left, right, up, down) : #
################################################

def move_left(event):
    '''
    Moves the tiles to the left, combining them if they have the same value.
    This function is bound to the left arrow key and is called when the key is pressed.
    It checks if the player can move (i.e. the game is not won or lost) and then moves the tiles
    to the left by iterating through each row of the board.
    If a tile is zero, it is moved to the end of the row.
    After moving the tiles, it checks if any tiles can be combined (i.e. two tiles with the same value are next to each other).
    If they can, it combines them and creates a new zero at the place of the first combined number.
    It then checks if the board has changed and updates it accordingly.
    If the board has changed, it updates the board and spawns a new square.
    If the player has reached 2048, it initiates a win state.
    If the player has lost (i.e. there are no more moves left), it initiates a loss state.
    To prevent multiple moves from happening at the same time, a global variable 'can_move' is used. 
    It is set to False when the function is called and set to True at the end of the function.
    Args:
        event (Event): The event that triggered the function (i.e. the left arrow key being pressed).
    '''
    global can_move
    if can_move == False: return
    global score
    global board
    global BOARD_SQUARE_LENGTH

    previous_board = deepcopy_2D_list(board)

    for i, row in enumerate(board):
        for j, num in enumerate(row):
            if num == 0:
                first_zero_index = row.index(0)
                # We need to use the index of the first zero instead of the 'j'-th zero we are currently at, due to the fact
                # that the move_index functions would skip over even indexes when moving the zero to the end
                move_index(board[i], first_zero_index, len(row) - 1)
    
    if event.keysym == 'Left':
        can_move = False
        create_phantom_tiles(previous_board, board, 'left')
        update_board(board, BOARD_SQUARE_LENGTH)
        can_move = True
    # Scan over the board again to determine whether there are numbers that should be combined:
    board_to_return = deepcopy_2D_list(board)
    for l, row in enumerate(board):
        for k, num in enumerate(row):
            if k > 0 and board[l][k - 1] == board[l][k]:
                # combine two numbers and create a new zero at the place of the first combined number
                board[l][k] = 0
                board[l][k - 1] *= 2
                score += board[l][k - 1]
                move_index(board[l], k, len(row) - 1)
                # move this new zero to the end of the row
    # Check if the board has changed
    if compare_boards(previous_board, board) == False and event.keysym == 'Left':
        update_board(board, BOARD_SQUARE_LENGTH)
        if check_2048(board):
            initiate_win()
            return
        else:
            create_square_on_board(board, BOARD_SQUARE_LENGTH)
    if check_loss(board):
        initiate_loss()
        return
    if event.keysym == 'Up':
        can_move = False
        return return_columns(board_to_return)

def move_right(event):
    global can_move
    if can_move == False: return
    # Works in basically the same way as the move_left function, except that zeros are moved to the start
    # of the row
    global score
    global board
    global BOARD_SQUARE_LENGTH
    previous_board = deepcopy_2D_list(board)

    for i, row in enumerate(board):
        for j, num in enumerate(row):
            if num == 0:
                move_index(board[i], j, 0)

    if event.keysym == 'Right':
        can_move = False
        create_phantom_tiles(previous_board, board, 'right')
        update_board(board, BOARD_SQUARE_LENGTH)
        can_move = True
        # Check whether 2 numbers next to each other match - if so, combine them
        # Iterate from right to left, so that right-most numbers get combined first instead of left-most numbers
        # This is so that a situation like this:
        # (0 2 2 2) = (0 0 2 4)
        # and not 
        # (0 2 2 2) = (0 0 4 2)
    board_to_return = deepcopy_2D_list(board)
    for i, row in enumerate(board):
        for k in range(len(row) - 1, -1, -1):
            if k < len(row) - 1 and board[i][k + 1] == board[i][k]:
                board[i][k + 1] *= 2
                score += board[i][k + 1]
                board[i][k] = 0
                move_index(board[i], k, 0)  
                # move this new zero to the start of the row
    # Check if the board has changed
    if compare_boards(previous_board, board) == False and event.keysym == 'Right':
        # event.keysym used as a workaround so that the board is updated at this point only if the 'right' arrow
        # key is pressed. This is to avoid spawning squares when moving down, which uses this function
        # (we want the check to happen at the end of the move_down function)
        
        # This is because the move_down function uses this function to transpose the matrix
        # and we don't want to spawn squares when transposing the matrix.
        update_board(board, BOARD_SQUARE_LENGTH)
        if check_2048(board):
            initiate_win()
            return
        else:
            create_square_on_board(board, BOARD_SQUARE_LENGTH)
    if check_loss(board):
        initiate_loss()
        return
    # returns a board without the numbers merged yet - this is for the purpose of animating tiles when moving down
    # because animating tiles when moving down requires the board to be in the same state as it was before the move
    # (i.e. without the numbers merged yet)
    if event.keysym == 'Down':
        can_move = False
        return return_columns(board_to_return)

# The move_down and move_up functions work by transposing the board (swapping rows and columns)
# and then reusing the move_right and move_left logic, respectively, to perform the move.
# This approach leverages existing code but introduces a dependency: any changes to move_left or move_right
# may have subtle effects on move_down or move_up, since they are called internally after transposing.
# The time complexity is O(n^2) due to the transposition, but this method simplifies code reuse and future modifications.

def move_down(event):
    global can_move
    if can_move == False: return
    global board
    global BOARD_SQUARE_LENGTH
    previous_board = deepcopy_2D_list(board)
    
    # Transpose the matrix:
    board = return_columns(board)
    create_phantom_tiles(previous_board, move_right(event), 'down')
    board = return_columns(board)
    update_board(board, BOARD_SQUARE_LENGTH)
    if compare_boards(previous_board, board) == False:
        if check_2048(board):
            initiate_win()
            return
        else:
            create_square_on_board(board, BOARD_SQUARE_LENGTH)
    if check_loss(board):
        initiate_loss()
        return
    can_move = True

def move_up(event):
    global can_move
    if can_move == False: return
    global board
    global BOARD_SQUARE_LENGTH
    previous_board = deepcopy_2D_list(board)

    board = return_columns(board)
    create_phantom_tiles(previous_board, move_left(event), 'up')
    board = return_columns(board)
    update_board(board, BOARD_SQUARE_LENGTH)
    if compare_boards(previous_board, board) == False:
        if check_2048(board):
            initiate_win()
            return
        else:
            create_square_on_board(board, BOARD_SQUARE_LENGTH)
    if check_loss(board):
        initiate_loss()
        return
    can_move = True

################################################
# END OF MOVEMENT FUNCTIONS                    #
################################################

def check_2048(board: list[list[int]]) -> bool:
    '''
    Returns True if '2048' is on the grid, False otherwise.
    Used to determine whether the 'initiate_win' function should be used.
    '''  
    for row in board:
        for num in row:
            if num == 2048:
                return True
    return False

def initiate_win():
    '''
    This function initiates the win cutscene.
    '''
    global score
    global can_move
    can_move = False
    canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text='YOU WON!', fill='yellow', font=f'{FONT} {font_size * 3} bold')
    canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + font_size * 3, text=f'Final score: {score}', fill='gold', font=f'{FONT} {font_size} bold')

def check_loss(board: list[list[int]]):
    for row in board:
        if 0 in row: return False
    for i in range(len(board)):
        for j in range(1, len(board[0])):
            if board[i][j] == board[i][j - 1]:
                return False
            
    for i in range(len(board[0])):
        for j in range(1, len(board)):
            if board[j][i] == board[j - 1][i]:
                return False
    
    
    return True # LOSS

def initiate_loss():
    global can_move
    can_move = False
    canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text='YOU LOST!', fill='red', font=f'{FONT} {font_size * 3} bold')
    canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + font_size * 3, text=f'Final score: {score}', fill='crimson', font=f'{FONT} {font_size} bold')

center_screen()
create_square_on_board(board, BOARD_SQUARE_LENGTH)
create_square_on_board(board, BOARD_SQUARE_LENGTH)

# root.bind('<Button-1>', create_square_on_click)
root.bind('<Left>', move_left)
root.bind('<Right>', move_right)
root.bind('<Down>', move_down)
root.bind('<Up>', move_up)
root.mainloop()

# test
# test