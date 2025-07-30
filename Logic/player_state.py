from game_config import starting_positions

def initialize_players(player_names, board):
    """Initialize all players with their starting positions"""
    player_states = {}
    
    # Cluedo starting positions (in order)
    start_positions = [
        (24, 9),   # Miss Scarlett - Hall entrance
        (24, 14),  # Colonel Mustard - Lounge entrance  
        (6, 23),   # Mrs. White - Ballroom/Kitchen area
        (19, 23),  # Reverend Green - Conservatory area
        (24, 7),   # Mrs. Peacock - Library entrance
        (17, 0)    # Professor Plum - Study entrance
    ]
    
    for i, player_name in enumerate(player_names):
        if i < len(start_positions):
            position = start_positions[i]
        else:
            # Default position if more players than starting positions
            position = (12, 12)
            
        player_states[player_name] = {
            "position": position,
            "in_room": None,
            "can_use_passage": False,
            "eliminated": False
        }
    
    return player_states

class PlayerStates:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.cards = []
        self.notes = {}
        self.eliminated = False
    
    def move(self, new_position):
        self.position = new_position
    
    def receive_card(self, card):
        self.cards.append(card)
    
    def update_notes(self, card, known_by):
        self.notes[card] = known_by
    
    def eliminate(self):
        self.eliminated = True
    
    def __repr__(self):
        return f"<Player {self.name}, Pos: {self.position}, Cards: {self.cards}, Eliminated: {self.eliminated}>"