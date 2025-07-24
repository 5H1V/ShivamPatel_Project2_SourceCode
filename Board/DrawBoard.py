import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np



class DrawBoard:

    def __init__(self):

        return

    def draw_cluedo_board():

        # Coordinates of room boundaries
        rooms = {
            "Lounge": [(0,0),(6,0),(6,1),(7,1),(7,6),(0,6)],
            "Hall": [(9,0),(15,0),(15,7),(9,7)],
            "Study": [(18,0),(24,0),(24,4),(17,4),(17,1),(18,1)],
            "DiningRoom": [(0,9),(8,9),(8,15),(5,15),(5,16),(0,16)],
            "Library": [(18,6),(23,6),(23,7),(24,7),(24,10),(23,10),(23,11),(18,11),(18,10),(17,10),(17,7),(18,7)],
            "BillardRoom": [(18,12),(24,12),(24,17),(18,17)],
            "Kitchen": [(1,18),(6,18),(6,24),(0,24),(0,19),(1,19)],
            "Ballroom": [(8,17),(16,17),(16,23),(14,23),(14,25),(10,25),(10,23),(8,23)],
            "Conservatory": [(19,19),(23,19),(23,20),(24,20),(24,24),(18,24),(18,20),(19,20)],
            "Center": [(10,8),(15,8),(15,15),(10,15)],
        }
        
        # Doorway positions top left (x, y)
        doors = [(6,6),(11,7),(12,7),(14,5),(17,4),(17,9),(20,11),(22,13),(18,16),(18,21),
                 (6,10),(7,13),(4,19),(8,20),(9,18),(14,18),(15,20)]

        # Draw rooms
        for name, coordinates in rooms.items():
            x, y = zip(*coordinates)
            plt.fill(x, y, color='lightgray')
            plt.plot(x + (x[0],), y + (y[0],), color='r')

        # Draw doorways - 17
        doorway = [(6,7,6,6),(11,13,7,7),(15,15,4,5),(17,18,4,4),(17,17,8,9),(20,21,11,11),
                   (6,7,9,9),(8,8,12,13),(22,23,12,12),(18,18,15,16),(4,5,18,18),(8,8,19,20),(9,10,17,17),
                   (14,15,17,17),(16,16,19,20),(18,19,20,20)]

        # Draw each remaining edge individually
        for x1,x2,y1,y2 in doorway:
            plt.plot([x1,x2],[y1,y2],color='blue')

        secret = [(6,7,5,5),(17,18,3,3),(4,5,19,19),(18,19,21,21)]

        for x1,x2,y1,y2 in secret:
            plt.plot([x1,x2],[y1,y2],color='green')
            
        game_walls = [(0,0),(6,0),(6,1),(7,1),(7,0),(8,0),(8,1),(9,1),(9,0),
                      (15,0),(15,1),(16,1),(16,0),(17,0),(17,1),(18,1),(18,0),
                      (24,0),(24,4),(23,4),(23,5),(24,5),(24,6),(23,6),(23,7),
                      (24,7),(24,10),(23,10),(23,12),(24,12),(24,17),(23,17),
                      (23,18),(24,18),(24,19),(23,19),(23,20),(24,20),(24,24),
                      (18,24),(18,23),(17,23),(17,24),(15,24),(15,25),(9,25),
                      (9,24),(7,24),(7,23),(6,23),(6,24),(0,24),(0,19),(1,19),
                      (1,18),(0,18),(0,17),(1,17),(1,16),(0,16),(0,9),(1,9),
                      (1,8),(0,8),(0,7),(1,7),(1,6),(0,6),(0,0)]
        
        x_vals = [x for x,y in game_walls]
        y_vals = [y for x,y in game_walls]
        
        plt.plot(x_vals, y_vals, color='black')

        plt.xticks([])
        plt.yticks([])
        for spine in plt.gca().spines.values():
            spine.set_visible(False)
        
        plt.show()


    def tiles():
        # 25 x 25 board
        # 0,0 in bottom left
        #
        return
    def Kitchen():

        return
    
    def Library():

        return

    def Ballroom():

        return

    def Study():

        return

    def Hall():
        #(9,0)->(114,5)
        return

    def BillardRoom():

        return

    def Conservatory():

        return

    def DiningRoom():

        return

    def Lounge():
        #(0,0) -> (6,5)
        return


"""
    Node(Kitchen)
    Node(Library)
    Node(Ballroom)
    Node(Study)
    Node(Hall)
    Node(BillardRoom)
    Node(Conservatory)
    Node(DiningRoom)
    Node(Lounge)
    Edge(Kitchen)
"""
"""
Mansion Layout:

This layout can be represented abstractly (e.g., a graph where rooms are nodes and passages are edges) or
concretely (e.g., a 2D grid or array). Ensure that the connections between rooms (i.e., which rooms are adjacent
and allow movement) are clearly defined. Try to include secret passages between certain rooms as per the original
game rules (e.g., Study to Kitchen, Conservatory to Lounge). Define designated starting positions for each character,
typically in hallways or outside specific rooms.

"""

if __name__=="__main__":
    DrawBoard.draw_cluedo_board()
