import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np



class DrawBoard:

    def __init__(self):

        return

    def draw_cluedo_board():
        fig, ax = plt.subplots()

        # Coordinates of room boundaries
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


        # Doorway positions top left (x, y)
        doors = [(6,19),(11,18),(12,18),(14,20),(17,21),(17,16),(20,14),(22,12),(18,9),(18,4),
                 (6,15),(7,12),(4,6),(8,5),(9,7),(14,7),(15,5)]

        # Draw rooms
        for name, coordinates in rooms.items():
            x, y = zip(*coordinates)
            plt.fill(x, y, color='lightgray')
            plt.plot(x + (x[0],), y + (y[0],), color='r')



        # Draw doorways - 17
        doorway = [(6,7,19,19),(11,13,18,18),(15,15,21,20),(17,18,21,21),(17,17,17,16),
                (20,21,14,14),(6,7,16,16),(8,8,13,12),(22,23,13,13),(18,18,10,9),
                (4,5,7,7),(8,8,6,5),(9,10,8,8),(14,15,8,8),(16,16,6,5),(18,19,5,5)]
        
        # Draw each remaining edge individually
        for x1,x2,y1,y2 in doorway:
            plt.plot([x1,x2],[y1,y2],color='blue')

        secret = [(6,7,20,20),(17,18,22,22),(4,5,6,6),(18,19,4,4)]

        for x1,x2,y1,y2 in secret:
            plt.plot([x1,x2],[y1,y2],color='green')

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
        plt.gca().set_aspect('equal', adjustable='box')

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
