import random
from game_config import board_labels, rooms, players, weapons
from logic.game_state import CluedoGame


# --- Accusation Logic ---
def make_accusation(player, solution):
    """Make an accusation"""
    print(f"\n{player}, make your accusation:")
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
    
    print(f"{player} accuses it was {character} with the {weapon} in the {room}!")
    
    return (accusation['player'] == solution['player'] and 
            accusation['weapon'] == solution['weapon'] and 
            accusation['room'] == solution['room'])