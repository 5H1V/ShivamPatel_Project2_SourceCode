import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from game_config import rooms_coordinates, doors, board_labels, starting_positions, secret, game_walls, player_colors, rooms

def position_matrix(board, player_positions=None):
    #Labelling rooms, doors, starting positions, secret passages, walls
    for name, coordinates in rooms_coordinates.items():
        poly_path = Path(coordinates)
        for y in range(25):
            for x in range(24):
                if poly_path.contains_point((x + 0.5, y + 0.5)):
                    board[y, x] = board_labels[name]

    for x, y in doors:
        board[y, x] = board_labels["Door"]
        
    for x, y in secret:
        board[y, x] = board_labels["Secret"]

    if player_positions:
        for x, y in player_positions:
            board[y, x] = board_labels["Occupied"]
    else:
        for x, y in starting_positions:
            board[y, x] = board_labels["Occupied"]    

    for row, cols in game_walls.items():
        for col in cols:
            board[row, col] = board_labels["Invalid"]
    
    return board

def draw_board(board, player_positions=None):
    """Drawing Cluedo board"""
    # Creating color map to color tiles
    # All rooms will be GOLD
    cmap = {-1 : "black", 0 : "white", 1 :"skyblue", 11 : "grey", 12 : "coral", 13 : "lightgreen"}

    # Plot board
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Draw board tiles
    for y in range(25):
        for x in range(24):
            color = cmap.get(board[y, x], "gold")
            ax.add_patch(plt.Rectangle((x, 24 - y), 1, 1, color=color))

    # Draw player tokens
    if player_positions != None:
        for x, y in player_positions.values():
            board[y, x] = board_labels["Occupied"]

    if player_positions:
        for player_name, position in player_positions.items():
            if position:
                y, x = position
                color = player_colors.get(player_name, "black")
                ax.add_patch(plt.Rectangle((x, 24 - y), 1, 1, color=color))

    # Setting up the plot
    ax.set_xlim(0, board.shape[1]-1)
    ax.set_ylim(0, board.shape[0])
    ax.set_aspect('equal')
    ax.set_title('Cluedo Board')
    ax.set_xticks(range(board.shape[1]))
    ax.set_yticks(range(board.shape[0] + 1))
    ax.grid(True)
    
    # Add legend for colors
    legend_elements = []
    for room_id, room_name in rooms.items():
        if room_id in cmap:
            legend_elements.append(patches.Patch(color=cmap[room_id], label=room_name))

    #----------------------------------------------------

    # Add other elements to legend
    legend_elements.extend([
        patches.Patch(color='coral', label='Doors'),
        patches.Patch(color='lightgreen', label='Secret Passages'),
        patches.Patch(color='yellow', label='Starting Positions'),
        patches.Patch(color='black', label='Walls')
    ])

    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.show()
