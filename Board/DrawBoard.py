import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
from game_config import rooms_coordinates, doors, board_labels, starting_positions, secret, game_walls, player_colors, rooms

def position_matrix(board, player_positions=None):
    #Labelling rooms, doors, starting positions, secret passages, walls
    board_height, board_width = board.shape
    
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

def draw_board(board, player_positions=None):
    """Drawing Cluedo board"""
    # Creating color map to color tiles
    # All rooms will be GOLD
    cmap = {-1 : "black", 0 : "white", 1 :"skyblue", 11 : "grey", 12 : "coral", 13 : "lightgreen"}

    for room_id in rooms.keys():
        cmap[room_id] = "gold"

    board_height, board_width = board.shape

    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Draw board tiles
    for y in range(board_height):
        for x in range(board_width):
            color = cmap.get(board[y, x], "gold")
            ax.add_patch(plt.Rectangle((x, board_height - 1 - y), 1, 1, color=color, edgecolor='black', linewidth=0.5))

    # Draw player tokens
    if player_positions != None:
        for x, y in player_positions.values():
            board[y, x] = board_labels["Occupied"]

    if player_positions:
        for player_name, position in player_positions.items():
            if position:
                y, x = position
                if 0 <= y < board_height and 0 <= x < board_width:
                    color = player_colors.get(player_name, "black")
                    circle = plt.Circle((x + 0.5, board_height - 1 - y + 0.5), 0.3, color=color, zorder=10)
                    ax.add_patch(circle)

    # Setting up the plot
    ax.set_xlim(0, board_width)
    ax.set_ylim(0, board_height)
    ax.set_aspect('equal')
    ax.set_title('Cluedo Board')
    ax.set_xticks(range(board_width + 1))
    ax.set_yticks(range(board_height + 1))
    ax.grid(True)
    
    # Add legend for colors
    legend_elements = []
    for room_id, room_name in rooms.items():
        if room_id in cmap:
            legend_elements.append(patches.Patch(color=cmap[room_id], label=room_name))

    legend_elements.extend([
        patches.Patch(color='coral', label='Doors'),
        patches.Patch(color='lightgreen', label='Secret Passages'),
        patches.Patch(color='yellow', label='Starting Positions'),
        patches.Patch(color='black', label='Walls')
    ])

    for player_name, color in player_colors.items():
        legend_elements.append(patches.Patch(color=color, label=player_name))

    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.show()
