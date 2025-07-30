import matplotlib.pyplot as plt
import matplotlib.patches as patches
from game_config import board_labels, rooms, players

def draw_board(board, player_positions=None):
    """Draw the Cluedo board with optional player positions"""
    # Color mapping for different board elements
    color_map = {
        -1: "black",        # Invalid/Walls
        0: "lightgray",     # Empty spaces
        1: "yellow",        # Starting positions/Occupied
        2: "lightblue",     # Ballroom
        3: "lightgreen",    # Billiard Room
        4: "lightcoral",    # Conservatory
        5: "lightyellow",   # Dining Room
        6: "lightpink",     # Hall
        7: "lightcyan",     # Kitchen
        8: "lavender",      # Library
        9: "lightseagreen", # Lounge
        10: "lightsalmon",  # Study
        11: "gray",         # Center
        12: "brown",        # Doors
        13: "purple"        # Secret passages
    }
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Draw board cells
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            cell_value = board[y, x]
            color = color_map.get(cell_value, "white")
            
            # Create rectangle for each cell
            rect = patches.Rectangle((x, board.shape[0] - y - 1), 1, 1, 
                                   linewidth=0.5, edgecolor='black', 
                                   facecolor=color, alpha=0.8)
            ax.add_patch(rect)
    
    # Add room labels
    room_centers = {
        2: (12, 18),   # Ballroom
        3: (21, 12),   # Billiard Room  
        4: (21, 3),    # Conservatory
        5: (4, 13),    # Dining Room
        6: (12, 20),   # Hall
        7: (3, 3),     # Kitchen
        8: (20, 16),   # Library
        9: (3, 20),    # Lounge
        10: (20, 22)   # Study
    }
    
    for room_id, (x, y) in room_centers.items():
        if room_id in rooms:
            ax.text(x, y, rooms[room_id], ha='center', va='center', 
                   fontsize=8, fontweight='bold', 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Draw player positions if provided
    if player_positions:
        player_colors = {
            "Miss Scarlett": "red",
            "Colonel Mustard": "orange", 
            "Mrs. White": "white",
            "Reverend Green": "green",
            "Mrs. Peacock": "blue",
            "Professor Plum": "purple"
        }
        
        for player_name, position in player_positions.items():
            if position:
                y, x = position
                color = player_colors.get(player_name, "black")
                circle = patches.Circle((x + 0.5, board.shape[0] - y - 0.5), 0.3,
                                      facecolor=color, edgecolor='black', linewidth=2)
                ax.add_patch(circle)
                
                # Add player initial
                initial = player_name[0] if player_name else "?"
                ax.text(x + 0.5, board.shape[0] - y - 0.5, initial, 
                       ha='center', va='center', fontsize=10, fontweight='bold',
                       color='white' if color != 'white' else 'black')
    
    # Set up the plot
    ax.set_xlim(0, board.shape[1])
    ax.set_ylim(0, board.shape[0])
    ax.set_aspect('equal')
    ax.set_title('Cluedo Board', fontsize=16, fontweight='bold')
    
    # Add grid
    ax.set_xticks(range(board.shape[1] + 1))
    ax.set_yticks(range(board.shape[0] + 1))
    ax.grid(True, alpha=0.3)
    
    # Remove tick labels for cleaner look
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Add legend for room colors
    legend_elements = []
    for room_id, room_name in rooms.items():
        if room_id in color_map:
            legend_elements.append(patches.Patch(color=color_map[room_id], label=room_name))
    
    # Add other elements to legend
    legend_elements.extend([
        patches.Patch(color='brown', label='Doors'),
        patches.Patch(color='purple', label='Secret Passages'),
        patches.Patch(color='yellow', label='Starting Positions'),
        patches.Patch(color='black', label='Walls')
    ])
    
    ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.tight_layout()
    plt.show()

def draw_simple_board(board):
    """Draw a simple text representation of the board"""
    print("Board Layout (Text):")
    print("Legend: █=Wall, .=Empty, S=Start, D=Door, P=Passage, 2-10=Rooms")
    print()
    
    for y in range(board.shape[0]):
        row = ""
        for x in range(board.shape[1]):
            val = board[y, x]
            if val == -1:
                row += "█"  # Wall
            elif val == 0:
                row += "."  # Empty
            elif val == 1:
                row += "S"  # Starting position
            elif 2 <= val <= 10:
                row += str(val)  # Room
            elif val == 11:
                row += "C"  # Center
            elif val == 12:
                row += "D"  # Door
            elif val == 13:
                row += "P"  # Secret passage
            else:
                row += "?"
        print(f"{y:2d}: {row}")
    
    print("\nRoom Key:")
    for room_id, room_name in rooms.items():
        print(f"{room_id}: {room_name}")

def save_board_image(board, filename="cluedo_board.png", player_positions=None):
    """Save the board as an image file"""
    draw_board(board, player_positions)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Board saved as {filename}")

# Example usage
if __name__ == "__main__":
    from board_builder import position_matrix
    
    # Create and display the board
    board = position_matrix()
    
    # Draw the board
    draw_board(board)
    
    # Also show simple text version
    draw_simple_board(board)