import matplotlib.pyplot as plt
from game_config import board_labels

class DrawBoard:
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

"""

if __name__=="__main__":
    position_matrix = DrawBoard.position_matrix(DrawBoard.board_labels,DrawBoard.rooms)
    
    DrawBoard.drawBoard(position_matrix)

"""
