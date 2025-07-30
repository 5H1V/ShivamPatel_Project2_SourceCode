import random
from game_config import board_labels, rooms, players, weapons

# --- Dice Rolling Function ---
def roll_dice():
    return random.randint(1, 6)

# --- Movement Functions ---
def move_player(player_name, steps, board, player_states):
    """Handle player movement with step-by-step validation"""
    current_pos = player_states[player_name]["position"]
    print(f"Current position: {current_pos}")
    print(f"You have {steps} steps to move.")
    print("Available directions: UP, DOWN, LEFT, RIGHT")
    
    new_pos = current_pos
    remaining_steps = steps
    
    while remaining_steps > 0:
        print(f"Remaining steps: {remaining_steps}")
        direction = input("Enter direction (UP/DOWN/LEFT/RIGHT) or DONE to stop: ").upper()
        
        if direction == "DONE":
            break
            
        if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
            print("Invalid direction. Please enter UP, DOWN, LEFT, or RIGHT.")
            continue
            
        # Calculate new position
        y, x = new_pos
        if direction == "UP":
            test_pos = (y - 1, x)
        elif direction == "DOWN":
            test_pos = (y + 1, x)
        elif direction == "LEFT":
            test_pos = (y, x - 1)
        elif direction == "RIGHT":
            test_pos = (y, x + 1)
        
        # Validate move
        if is_valid_position(test_pos, board):
            new_pos = test_pos
            remaining_steps -= 1
            print(f"Moved to {new_pos}")
        else:
            print("Can't move there - blocked by wall or out of bounds.")
    
    # Update player position
    player_states[player_name]["position"] = new_pos
    
    # Check if in a room
    current_room = get_current_room(new_pos, board)
    return True, current_room

def is_valid_position(pos, board):
    """Check if position is valid (not wall, within bounds)"""
    y, x = pos
    if y < 0 or y >= board.shape[0] or x < 0 or x >= board.shape[1]:
        return False
    
    cell_value = board[y, x]
    return cell_value != board_labels["Invalid"]

def get_current_room(position, board):
    """Check if player is in a room"""
    y, x = position
    if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
        cell_value = board[y, x]
        if cell_value in rooms:
            return cell_value
    return None

# --- Secret Passage Logic ---
def use_secret_passage(player_name, player_states, board, current_room):
    """Use secret passage to move to connected room"""
    secret_passages = {
        10: 7,  # Study to Kitchen
        7: 10,  # Kitchen to Study
        4: 9,   # Conservatory to Lounge
        9: 4    # Lounge to Conservatory
    }
    
    target_room = secret_passages.get(current_room)
    if target_room:
        # Find a position in the target room
        target_pos = find_room_position(target_room, board)
        if target_pos:
            player_states[player_name]["position"] = target_pos
            return target_room
    return None

def find_room_position(room_id, board):
    """Find a valid position within a room"""
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            if board[y, x] == room_id:
                return (y, x)
    return None

# --- Suggestion Logic ---
def make_suggestion(player_name, player_states, card_hands, board, room_id, active_players):
    """Make a suggestion in the current room"""
    room_name = rooms[room_id]
    print(f"\n{player_name}, you are in the {room_name}.")
    print("Make a suggestion:")
    
    # Show available options
    print("Characters:", list(players.values()))
    print("Weapons:", list(weapons.values()))
    
    character = input("Suggest a character: ").strip()
    weapon = input("Suggest a weapon: ").strip()
    
    # Find the IDs for the suggested items
    character_id = None
    weapon_id = None
    
    for pid, pname in players.items():
        if pname.lower() == character.lower():
            character_id = pid
            break
    
    for wid, wname in weapons.items():
        if wname.lower() == weapon.lower():
            weapon_id = wid
            break
    
    if character_id is None or weapon_id is None:
        print("Invalid suggestion. Please use exact names.")
        return
    
    suggestion = (character_id, weapon_id, room_id)
    print(f"{player_name} suggests it was {character} with the {weapon} in the {room_name}.")
    
    # Check other players for cards
    player_list = list(active_players)
    current_idx = player_list.index(player_name)
    
    for i in range(1, len(player_list)):
        next_idx = (current_idx + i) % len(player_list)
        next_player = player_list[next_idx]
        
        if next_player not in active_players:
            continue
            
        matching_cards = []
        for card in card_hands[next_player]:
            if card in suggestion:
                matching_cards.append(card)
        
        if matching_cards:
            shown_card = random.choice(matching_cards)
            card_name = get_card_name(shown_card)
            print(f"{next_player} shows {player_name} the {card_name} card.")
            return shown_card
    
    print("No player could refute the suggestion.")
    return None

def get_card_name(card_id):
    """Convert card ID to readable name"""
    if card_id in rooms:
        return rooms[card_id]
    elif card_id in players:
        return players[card_id]
    elif card_id in weapons:
        return weapons[card_id]
    return f"Unknown card {card_id}"

# --- Accusation Logic ---
def make_accusation(player_name, solution):
    """Make an accusation"""
    print(f"\n{player_name}, make your accusation:")
    print("Characters:", list(players.values()))
    print("Weapons:", list(weapons.values()))
    print("Rooms:", list(rooms.values()))
    
    character = input("Accuse a character: ").strip()
    weapon = input("Accuse a weapon: ").strip()
    room = input("Accuse a room: ").strip()
    
    # Find the IDs for the accused items
    character_id = None
    weapon_id = None
    room_id = None
    
    for pid, pname in players.items():
        if pname.lower() == character.lower():
            character_id = pid
            break
    
    for wid, wname in weapons.items():
        if wname.lower() == weapon.lower():
            weapon_id = wid
            break
            
    for rid, rname in rooms.items():
        if rname.lower() == room.lower():
            room_id = rid
            break
    
    if character_id is None or weapon_id is None or room_id is None:
        print("Invalid accusation. Please use exact names.")
        return False
    
    accusation = {
        'player': character_id,
        'weapon': weapon_id,
        'room': room_id
    }
    
    print(f"{player_name} accuses it was {character} with the {weapon} in the {room}!")
    
    return (accusation['player'] == solution['player'] and 
            accusation['weapon'] == solution['weapon'] and 
            accusation['room'] == solution['room'])