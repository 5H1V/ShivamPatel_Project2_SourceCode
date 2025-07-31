import numpy as np
from matplotlib.path import Path
from game_config import rooms_coordinates, doors, board_labels, starting_positions, secret, game_walls

def position_matrix(board, player_positions=None):
    """
    Creating matrix to keep track of board boundaries, doors, secret passages, player positions, walls
    """
    board_height, board_width = board.shape
    
    # Adding room locations
    for name, coordinates in rooms_coordinates.items():
        poly_path = Path(coordinates)
        for y in range(board_height):
            for x in range(board_width):
                if poly_path.contains_point((x + 0.5, y + 0.5)):
                    if name in board_labels:
                        board[y, x] = board_labels[name]

    for x, y in doors:
        if 0 <= y < board_height and 0 <= x < board_width:
            board[y, x] = board_labels["Door"]

    for x, y in secret:
        if 0 <= y < board_height and 0 <= x < board_width:
            board[y, x] = board_labels["Secret"]

    if not player_positions:
        for x, y in starting_positions:
            if 0 <= y < board_height and 0 <= x < board_width:
                board[y, x] = board_labels["Occupied"]

    for row, cols in game_walls.items():
        if 0 <= row < board_height:
            for col in cols:
                if 0 <= col < board_width:
                    board[row, col] = board_labels["Invalid"]
    
    return board

def print_board(board):
    """
    Prints out board in command line for debugging purposes
    """
    np.set_printoptions(linewidth=200)
    print(board.astype(int))
