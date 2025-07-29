import numpy as np
import matplotlib.path as Path
from game_config import board_labels, rooms


class BoardBuilder:
    def position_matrix(board_labels, rooms):
        board = np.zeros((25,24), dtype=int)
        for name, coordinates in rooms.items():
            path = Path(coordinates)
            for y in range(25):
                for x in range(25):
                    if path.contains_point((x + 0.5, y + 0.5)):
                        board[y, x] = board_labels[name]
        
        return board

        doorway = [(6,19),(11,18),(12,18),(14,20),(17,21),(17,16),
                (20,14),(6,15),(7,12),(22,12),(18,9),(4,6),
                (8,5),(9,7),(14,7),(15,5),(18,4)]

        for x,y in doorway:
            board[y, x] = board_labels["Door"]

        starting_positions = [(9,0),(14,0),(23,6),(23,19),(7,24),(0,17)]
        for x, y in starting_positions:
            board[y, x] = board_labels["Occupied"]

        secret = [(4,5),(18,3),(17,22),(6,20)]
        for x, y in secret:
            board[y, x] = board_labels["Secret"]

        game_walls = {0:[0,1,2,3,4,5,6,7,8,15,16,17,18,19,20,21,22,23],
                    1:[6,17], 5:[23], 6:[0], 7:[23], 8:[0], 13:[23],
                    14:[23], 16:[0], 18:[0,23], 20:[23], 24:[6,8,15,17]}

        for row, cols in game_walls.items():
            for col in cols:
                board[row, col] = board_labels["Invalid"]

        np.set_printoptions(linewidth=200)
        print(board.astype(int))

        return board
