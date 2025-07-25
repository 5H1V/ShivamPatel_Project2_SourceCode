import numpy as np
from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches



class DrawBoard:

    def __init__(self):

        return

    board_labels = {"Invalid": -1,
                    "Empty" : 0,
                    "Occupied" : 1,
                    "Ballroom" : 2,
                    "BillardRoom" : 3,
                    "Conservatory" : 4,
                    "DiningRoom" : 5,
                    "Hall" : 6,
                    "Kitchen" : 7,
                    "Library" : 8,
                    "Lounge" : 9,
                    "Study" : 10,
                    "Center" : 11,
                    "Door" : 12,
                    "Secret" : 13}

    rooms = {
        "Lounge": [(0,25),(6,25),(6,24),(7,24),(7,19),(0,19)],
        "Hall": [(9,25),(15,25),(15,18),(9,18)],
        "Study": [(18,25),(24,25),(24,21),(17,21),(17,24),(18,24)],
        "DiningRoom": [(0,16),(8,16),(8,10),(5,10),(5,9),(0,9)],
        "Library": [(18,19),(23,19),(23,18),(24,18),(24,15),(23,15),(23,14),(18,14),(18,15),(17,15),(17,18),(18,18)],
        "BillardRoom": [(18,13),(24,13),(24,8),(18,8)],
        "Kitchen": [(1,7),(6,7),(6,1),(0,1),(0,6),(1,6)],
        "Ballroom": [(8,8),(16,8),(16,2),(14,2),(14,0),(10,0),(10,2),(8,2)],
        "Conservatory": [(19,6),(23,6),(23,5),(24,5),(24,1),(18,1),(18,5),(19,5)],
        "Center": [(10,17),(15,17),(15,10),(10,10)],
    }

    def position_matrix(board_labels, rooms):
        board = np.zeros((25,24))
        for name, coordinates in rooms.items():
            poly_path = Path(coordinates)
            for y in range(25):
                for x in range(25):
                    if poly_path.contains_point((x + 0.5, y + 0.5)):
                        board[y, x] = board_labels[name]


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

    def drawBoard(board):
        cmap = {-1 : "black", 0 : "white", 1 :"skyblue", 11 : "grey", 12 : "coral", 13 : "lightgreen"}
        fig, ax = plt.subplots()
        for y in range(25):
            for x in range(24):
                color = cmap.get(board[y, x], "gold")
                ax.add_patch(plt.Rectangle((x, 24 - y), 1, 1, color=color))
        ax.set_xlim(0, 24)
        ax.set_ylim(0, 25)
        ax.set_xticks(range(25))
        ax.set_yticks(range(26))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(True)
        ax.set_aspect('equal')

        plt.show()



if __name__=="__main__":
    position_matrix = DrawBoard.position_matrix(DrawBoard.board_labels,DrawBoard.rooms)
    
    DrawBoard.drawBoard(position_matrix)
"""
Mansion Layout:

This layout can be represented abstractly (e.g., a graph where rooms are nodes and passages are edges) or
concretely (e.g., a 2D grid or array). Ensure that the connections between rooms (i.e., which rooms are adjacent
and allow movement) are clearly defined. Try to include secret passages between certain rooms as per the original
game rules (e.g., Study to Kitchen, Conservatory to Lounge). Define designated starting positions for each character,
typically in hallways or outside specific rooms.

"""
