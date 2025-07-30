import random

# Player character mappings
player_colors = {
    "scarlet": "Miss Scarlett",
    "mustard": "Colonel Mustard", 
    "white": "Mrs. White",
    "green": "Reverend Green",
    "peacock": "Mrs. Peacock",
    "plum": "Professor Plum"
}

# Room mappings (ID -> Name)
rooms = {
    2: "Ballroom",
    3: "Billiard Room",
    4: "Conservatory", 
    5: "Dining Room",
    6: "Hall",
    7: "Kitchen",
    8: "Library",
    9: "Lounge",
    10: "Study"
}

# Player character mappings (ID -> Name)
players = {
    11: "Miss Scarlett",
    12: "Colonel Mustard",
    13: "Mrs. White", 
    14: "Reverend Green",
    15: "Mrs. Peacock",
    16: "Professor Plum"
}

# Weapon mappings (ID -> Name)
weapons = {
    17: "Candlestick",
    18: "Dagger",
    19: "Lead Pipe",
    20: "Revolver", 
    21: "Rope",
    22: "Wrench"
}

# Board element labels
board_labels = {
    "Invalid": -1,
    "Empty": 0,
    "Occupied": 1,
    "Ballroom": 2,
    "Billiard Room": 3,
    "Conservatory": 4,
    "Dining Room": 5,
    "Hall": 6,
    "Kitchen": 7,
    "Library": 8,
    "Lounge": 9,
    "Study": 10,
    "Center": 11,
    "Door": 12,
    "Secret": 13
}

# Room coordinates (polygon vertices defining room boundaries)
rooms_coordinates = {
    "Lounge": [(0, 25), (6, 25), (6, 24), (7, 24), (7, 19), (0, 19)],
    "Hall": [(9, 25), (15, 25), (15, 18), (9, 18)],
    "Study": [(18, 25), (24, 25), (24, 21), (17, 21), (17, 24), (18, 24)],
    "Dining Room": [(0, 16), (8, 16), (8, 10), (5, 10), (5, 9), (0, 9)],
    "Library": [(18, 19), (23, 19), (23, 18), (24, 18), (24, 15), (23, 15), (23, 14), (18, 14), (18, 15), (17, 15), (17, 18), (18, 18)],
    "Billiard Room": [(18, 13), (24, 13), (24, 8), (18, 8)],
    "Kitchen": [(1, 7), (6, 7), (6, 1), (0, 1), (0, 6), (1, 6)],
    "Ballroom": [(8, 8), (16, 8), (16, 2), (14, 2), (14, 0), (10, 0), (10, 2), (8, 2)],
    "Conservatory": [(19, 6), (23, 6), (23, 5), (24, 5), (24, 1), (18, 1), (18, 5), (19, 5)],
    "Center": [(10, 17), (15, 17), (15, 10), (10, 10)]
}

# Door positions (x, y coordinates)
doors = [
    (6, 19), (11, 18), (12, 18), (14, 20), (17, 21), (17, 16),
    (20, 14), (6, 15), (7, 12), (22, 12), (18, 9), (4, 6),
    (8, 5), (9, 7), (14, 7), (15, 5), (18, 4)
]

# Secret passage positions (x, y coordinates)
secret = [(4, 5), (18, 3), (17, 22), (6, 20)]

# Starting positions for players (x, y coordinates)
starting_positions = [(9, 0), (14, 0), (23, 6), (23, 19), (7, 24), (0, 17)]

# Wall positions by row
game_walls = {
    0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22, 23],
    1: [6, 17],
    5: [23],
    6: [0],
    7: [23], 
    8: [0],
    13: [23],
    14: [23],
    16: [0],
    18: [0, 23],
    20: [23],
    24: [6, 8, 15, 17]
}

# Secret passage connections
secret_passages = {
    10: 7,  # Study to Kitchen
    7: 10,  # Kitchen to Study
    4: 9,   # Conservatory to Lounge
    9: 4    # Lounge to Conservatory
}

# Generate random solution (one from each category)
def generate_solution():
    """Generate a random solution for the game"""
    return {
        'room': random.choice(list(rooms.keys())),
        'player': random.choice(list(players.keys())),
        'weapon': random.choice(list(weapons.keys()))
    }

# Default solution (will be overridden in game)
solution = generate_solution()

# Player starting positions mapping
player_start_positions = {
    "Miss Scarlett": (24, 9),    # Bottom center
    "Colonel Mustard": (0, 14),  # Bottom right of center
    "Mrs. White": (6, 23),       # Left side
    "Reverend Green": (19, 23),  # Right side
    "Mrs. Peacock": (0, 9),     # Bottom left of center
    "Professor Plum": (17, 0)    # Top right
}

# Game constants
MAX_DICE_ROLL = 6
MIN_DICE_ROLL = 1
MAX_PLAYERS = 6
MIN_PLAYERS = 3

# Suggestion validation lists (for input validation)
valid_rooms = list(rooms.values())
valid_players = list(players.values()) 
valid_weapons = list(weapons.values())

def get_all_cards():
    """Get all cards in the game"""
    return list(rooms.keys()) + list(players.keys()) + list(weapons.keys())

def get_card_type(card_id):
    """Determine the type of a card by its ID"""
    if card_id in rooms:
        return "room"
    elif card_id in players:
        return "player"
    elif card_id in weapons:
        return "weapon"
    else:
        return "unknown"

def get_card_name(card_id):
    """Get the name of a card by its ID"""
    if card_id in rooms:
        return rooms[card_id]
    elif card_id in players:
        return players[card_id]
    elif card_id in weapons:
        return weapons[card_id]
    else:
        return f"Unknown card {card_id}"

def validate_suggestion(room_name, player_name, weapon_name):
    """Validate that a suggestion contains valid items"""
    return (room_name in valid_rooms and 
            player_name in valid_players and 
            weapon_name in valid_weapons)

def print_game_info():
    """Print all game information for reference"""
    print("=== CLUEDO GAME REFERENCE ===")
    print("\nROOMS:")
    for room_id, room_name in rooms.items():
        print(f"  {room_id}: {room_name}")
    
    print("\nPLAYERS:")
    for player_id, player_name in players.items():
        print(f"  {player_id}: {player_name}")
    
    print("\nWEAPONS:")
    for weapon_id, weapon_name in weapons.items():
        print(f"  {weapon_id}: {weapon_name}")
    
    print("\nSECRET PASSAGES:")
    for from_room, to_room in secret_passages.items():
        from_name = rooms.get(from_room, f"Room {from_room}")
        to_name = rooms.get(to_room, f"Room {to_room}")
        print(f"  {from_name} <-> {to_name}")
    
    print("\nSTARTING POSITIONS:")
    for player_name, position in player_start_positions.items():
        print(f"  {player_name}: {position}")
    
    print("============================\n")

# Testing and debugging functions
def test_board_integrity():
    """Test that all board elements are properly configured"""
    issues = []
    
    # Check room coordinates are within bounds
    for room_name, coords in rooms_coordinates.items():
        for x, y in coords:
            if not (0 <= x <= 24 and 0 <= y <= 25):
                issues.append(f"Room {room_name} has coordinates out of bounds: ({x}, {y})")
    
    # Check door positions are within bounds
    for x, y in doors:
        if not (0 <= x < 24 and 0 <= y < 25):
            issues.append(f"Door at ({x}, {y}) is out of bounds")
    
    # Check starting positions are within bounds
    for x, y in starting_positions:
        if not (0 <= x < 24 and 0 <= y < 25):
            issues.append(f"Starting position at ({x}, {y}) is out of bounds")
    
    # Check secret passage connections are valid
    for from_room, to_room in secret_passages.items():
        if from_room not in rooms:
            issues.append(f"Secret passage from unknown room ID: {from_room}")
        if to_room not in rooms:
            issues.append(f"Secret passage to unknown room ID: {to_room}")
    
    if issues:
        print("BOARD INTEGRITY ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Board integrity check passed!")
    
    return len(issues) == 0

if __name__ == "__main__":
    print_game_info()
    test_board_integrity()
    