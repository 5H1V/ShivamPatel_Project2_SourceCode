import numpy as np
from game_config import board_labels, rooms_coordinates, doors, starting_positions, secret, game_walls

def position_matrix():
    """Create the Cluedo board matrix with proper room assignments"""
    # Initialize board with empty spaces
    board = np.full((25, 24), board_labels["Empty"], dtype=int)
    
    # Mark rooms using coordinates
    for room_name, coordinates in rooms_coordinates.items():
        if room_name in board_labels:
            room_id = board_labels[room_name]
            # Convert polygon coordinates to filled area
            fill_polygon(board, coordinates, room_id)
    
    # Mark doors
    for x, y in doors:
        if 0 <= y < 25 and 0 <= x < 24:
            board[y, x] = board_labels["Door"]
    
    # Mark starting positions
    for x, y in starting_positions:
        if 0 <= y < 25 and 0 <= x < 24:
            board[y, x] = board_labels["Occupied"]
    
    # Mark secret passages
    for x, y in secret:
        if 0 <= y < 25 and 0 <= x < 24:
            board[y, x] = board_labels["Secret"]
    
    # Mark walls
    for row, cols in game_walls.items():
        if 0 <= row < 25:
            for col in cols:
                if 0 <= col < 24:
                    board[row, col] = board_labels["Invalid"]
    
    return board

def fill_polygon(board, coordinates, fill_value):
    """Fill a polygon area on the board with the given value"""
    if len(coordinates) < 3:
        return
    
    # Get bounding box
    min_x = min(coord[0] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)
    
    # Simple point-in-polygon test for rectangular-ish rooms
    for y in range(max(0, min_y), min(25, max_y + 1)):
        for x in range(max(0, min_x), min(24, max_x + 1)):
            if point_in_polygon(x, y, coordinates):
                board[y, x] = fill_value

def point_in_polygon(x, y, coordinates):
    """Check if a point is inside a polygon using ray casting algorithm"""
    n = len(coordinates)
    inside = False
    
    p1x, p1y = coordinates[0]
    for i in range(1, n + 1):
        p2x, p2y = coordinates[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside

def get_room_at_position(board, y, x):
    """Get the room ID at a specific board position"""
    if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
        cell_value = board[y, x]
        # Check if it's a room (values 2-10 in our configuration)
        if 2 <= cell_value <= 10:
            return cell_value
    return None

def get_valid_positions_in_room(board, room_id):
    """Get all valid positions within a specific room"""
    positions = []
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            if board[y, x] == room_id:
                positions.append((y, x))
    return positions

def find_nearest_room_entrance(board, room_id):
    """Find the nearest door/entrance to a room"""
    room_positions = get_valid_positions_in_room(board, room_id)
    if not room_positions:
        return None
    
    # Look for doors adjacent to room positions
    for y, x in room_positions:
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if (0 <= ny < board.shape[0] and 0 <= nx < board.shape[1] and 
                board[ny, nx] == board_labels["Door"]):
                return (ny, nx)
    
    # If no door found, return first room position
    return room_positions[0]

def is_adjacent_to_room(board, position, room_id):
    """Check if a position is adjacent to a specific room"""
    y, x = position
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = y + dy, x + dx
        if (0 <= ny < board.shape[0] and 0 <= nx < board.shape[1] and 
            board[ny, nx] == room_id):
            return True
    return False

def get_walkable_positions(board):
    """Get all positions that players can walk on"""
    walkable = []
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            cell_value = board[y, x]
            if cell_value != board_labels["Invalid"]:
                walkable.append((y, x))
    return walkable

def print_board_debug(board):
    """Print board for debugging purposes"""
    print("Board Layout:")
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
        print(row)
    print()