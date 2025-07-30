import random

#Mapping for character, color
player_colors = {
    "Miss Scarlett": "red",
    "Colonel Mustard": "orange", 
    "Mrs. White": "pink",
    "Reverend Green": "green",
    "Mrs. Peacock": "blue",
    "Professor Plum": "purple"
}

#Mappings for id, room for shuffle purposes
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

#Mappings for id, character for shuffle purposes
players = {
    11: "Miss Scarlett",
    12: "Colonel Mustard",
    13: "Mrs. White", 
    14: "Reverend Green",
    15: "Mrs. Peacock",
    16: "Professor Plum"
    }

#Mappings for id, weapon for shuffle purposes
weapons = {
    17: "Candlestick",
    18: "Dagger",
    19: "Lead Pipe",
    20: "Revolver", 
    21: "Rope",
    22: "Wrench"
    }

#Mappings for tile, status for coloring purposes
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

#Room coordinates (vertices are defining room edges)
rooms_coordinates = {
    "Lounge": [(0,25),(6,25),(6,24),(7,24),(7,19),(0,19)],
    "Hall": [(9,25),(15,25),(15,18),(9,18)],
    "Study": [(18,25),(24,25),(24,21),(17,21),(17,24),(18,24)],
    "Dining Room": [(0,16),(8,16),(8,10),(5,10),(5,9),(0,9)],
    "Library": [(18,19),(23,19),(23,18),(24,18),(24,15),(23,15),(23,14),(18,14),(18,15),(17,15),(17,18),(18,18)],
    "Billiard Room": [(18,13),(24,13),(24,8),(18,8)],
    "Kitchen": [(1,7),(6,7),(6,1),(0,1),(0,6),(1,6)],
    "Ballroom": [(8,8),(16,8),(16,2),(14,2),(14,0),(10,0),(10,2),(8,2)],
    "Conservatory": [(19,6),(23,6),(23,5),(24,5),(24,1),(18,1),(18,5),(19,5)],
    "Center": [(10,17),(15,17),(15,10),(10,10)]
    }
#Center of room for labelling
room_centers = {
    2: (12, 4),     # Ballroom
    3: (21, 11),   # Billiard Room  
    4: (21, 3),    # Conservatory
    5: (4, 13),    # Dining Room
    6: (12, 21),   # Hall
    7: (3, 3),     # Kitchen
    8: (21, 15),   # Library
    9: (3, 21),    # Lounge
    10: (21, 23)   # Study
}

#Door positions (coordinates of tile inside doorway)
doors = [
    (6,19),(11,18),(12,18),(14,20),(17,21),(17,16),
    (20,14),(6,15),(7,12),(22,12),(18,9),
    (4,6),(8,5),(9,7),(14,7),(15,5),(18,4)
    ]

#Secret Passage positions (coordinates of tile 1 tile straight of doorway in room)
secret = [(4,5),(18,3),(17,22),(6,20)]

#Starting positions (coordinates of tile)
starting_positions = [(9,0),(14,0),(23,6),(23,19),(7,24),(0,17)]

#Wall positions (showing row, outside wall boundary)
game_walls = {0:[0,1,2,3,4,5,6,7,8,15,16,17,18,19,20,21,22,23],
              1:[6,17],
              5:[23],
              6:[0],
              7:[23],
              8:[0],
              13:[23],
              14:[23],
              16:[0],
              18:[0,23],
              20:[23],
              24:[6,8,15,17]
              }

#Secret passage room connections
secret_passages = {
    10:7, 7:10,     #Study to Kitchen and vice versa
    4:9, 9:4        #Conservatory to Lounge and vice cersa
    }

solution = {
    'room': random.choice(list(rooms.keys())),
    'player': random.choice(list(players.keys())),
    'weapon': random.choice(list(weapons.keys()))
    }

#TEMPORARY Player starting positions
"""Need to randomize starting positions"""
player_start_positions = {
    "Miss Scarlett": (24,7),
    "Colonel Mustard": (17,0),
    "Mrs. White": (19,23),
    "Reverend Green": (6,23),
    "Mrs. Peacock": (0,9),
    "Professor Plum": (0,14)
    }

valid_rooms = list(rooms.values())
valid_players = list(players.values()) 
valid_weapons = list(weapons.values())

def get_all_cards():
    """All 21 cards"""
    return list(rooms.keys()) + list(players.keys()) + list(weapons.keys())

#----------------------------------------------------

def get_card_name(card_id):
    """Find the card based on card id"""
    if card_id in rooms:
        return rooms[card_id]
    elif card_id in players:
        return players[card_id]
    elif card_id in weapons:
        return weapons[card_id]
    else:
        return f"Unknown card {card_id}"
