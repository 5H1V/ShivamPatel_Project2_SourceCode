import numpy as np
from matplotlib.path import Path
from game_config import board_labels, rooms, doors, starting_positions, secret, game_walls


def position_matrix():
    board = np.zeros((25,24), dtype=int)
    for name, coordinates in rooms.items():
        poly_path = Path(coordinates)
        for y in range(25):
            for x in range(25):
                if poly_path.contains_point((x + 0.5, y + 0.5)):
                    board[y, x] = board_labels[name]

    for x,y in doors:
        board[y, x] = board_labels["Door"]

    for x, y in starting_positions:
        board[y, x] = board_labels["Occupied"]

    for x, y in secret:
        board[y, x] = board_labels["Secret"]

    for row, cols in game_walls.items():
        for col in cols:
            board[row, col] = board_labels["Invalid"]

    return board