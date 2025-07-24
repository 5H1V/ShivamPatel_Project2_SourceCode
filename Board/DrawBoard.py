import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np



class DrawBoard:

    def __init__(self):

        return

    def draw_cluedo_board():
        fig, ax = plt.subplots()

        # Coordinates of room boundaries
            
        game_walls = [(0,25),(6,25),(6,24),(7,24),(7,25),(8,25),(8,24),(9,24),(9,25),
                    (15,25),(15,24),(16,24),(16,25),(17,25),(17,24),(18,24),(18,25),
                    (24,25),(24,21),(23,21),(23,20),(24,20),(24,19),(23,19),(23,18),
                    (24,18),(24,15),(23,15),(23,13),(24,13),(24,8),(23,8),(23,7),(24,7),
                    (24,6),(23,6),(23,5),(24,5),(24,1),(18,1),(18,2),(17,2),(17,1),
                    (15,1),(15,0),(9,0),(9,1),(7,1),(7,2),(6,2),(6,1),(0,1),(0,6),(1,6),
                    (1,7),(0,7),(0,8),(1,8),(1,9),(0,9),(0,16),(1,16),(1,17),(0,17),
                    (0,18),(1,18),(1,19),(0,19),(0,25)]
        
        x_vals = [x for x,y in game_walls]
        y_vals = [y for x,y in game_walls]
        
        plt.plot(x_vals, y_vals, color='black')

        starting_positions = [(7,24),(23,19),(23,6),(14,0),(9,0),(0,17)]

        for x,y in starting_positions:
            position = patches.Rectangle((x, y), 1, 1, facecolor='lightgrey')
            ax.add_patch(position)
        
        plt.xticks([])
        plt.yticks([])
        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        plt.gca().invert_yaxis()

        plt.show()




if __name__=="__main__":
    DrawBoard.draw_cluedo_board()
"""
Mansion Layout:

This layout can be represented abstractly (e.g., a graph where rooms are nodes and passages are edges) or
concretely (e.g., a 2D grid or array). Ensure that the connections between rooms (i.e., which rooms are adjacent
and allow movement) are clearly defined. Try to include secret passages between certain rooms as per the original
game rules (e.g., Study to Kitchen, Conservatory to Lounge). Define designated starting positions for each character,
typically in hallways or outside specific rooms.

"""
