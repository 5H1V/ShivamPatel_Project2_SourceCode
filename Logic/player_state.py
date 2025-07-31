import random
from game_config import players, weapons, rooms, player_start_positions, get_all_cards

class Player:
    def __init__(self, name, card_hand, is_ai=False):
        self.name = name
        self.index = [key for key, value in players.items() if value == name][0]
        self.starting_position = player_start_positions.get(name)
        self.card_hand = card_hand.get(name, [])
        self.current_position = player_start_positions.get(name)
        self.knowledge = get_all_cards().copy()  # Cards we think might be the solution
        self.eliminated = False
        self.game_won = False
        self.winner = None
        self.is_ai = is_ai
        
        # AI-specific knowledge tracking
        if is_ai:
            self.player_cards = {}  # Track what cards other players have shown
            self.player_no_cards = {}  # Track what cards other players don't have
            self.suggestions_made = []
            self.refutations_seen = []
            
            # Initialize knowledge about other players
            for player_name in players.values():
                if player_name != name:
                    self.player_cards[player_name] = set()
                    self.player_no_cards[player_name] = set()
        
        # Remove our own cards from knowledge (we know they're not the solution)
        for card in self.card_hand:
            if card in self.knowledge:
                self.knowledge.remove(card)
    
    def update_ai_knowledge_card_shown(self, showing_player, card_id):
        """AI learns that a specific player has a specific card"""
        if self.is_ai and showing_player in self.player_cards:
            self.player_cards[showing_player].add(card_id)
            # Remove from knowledge if we now know who has it
            if card_id in self.knowledge:
                self.knowledge.remove(card_id)
    
    def update_ai_knowledge_no_refutation(self, suggestion, players_checked):
        """AI learns that certain players don't have certain cards"""
        if self.is_ai:
            for player_name in players_checked:
                if player_name in self.player_no_cards:
                    for card_id in suggestion:
                        self.player_no_cards[player_name].add(card_id)
    
    def make_ai_suggestion(self, current_room_id):
        """AI makes a strategic suggestion"""
        if not self.is_ai:
            return None
        
        # Choose cards we're uncertain about
        possible_characters = [card for card in players.keys() if card in self.knowledge]
        possible_weapons = [card for card in weapons.keys() if card in self.knowledge]
        
        # If we have no uncertain cards, choose randomly from all
        if not possible_characters:
            possible_characters = list(players.keys())
        if not possible_weapons:
            possible_weapons = list(weapons.keys())
        
        character = random.choice(possible_characters)
        weapon = random.choice(possible_weapons)
        
        return character, weapon, current_room_id
    
    def should_make_accusation(self):
        """AI decides if it should make an accusation"""
        if not self.is_ai:
            return False, None
        
        # Only accuse if we're confident about all three categories
        possible_characters = [card for card in players.keys() if card in self.knowledge]
        possible_weapons = [card for card in weapons.keys() if card in self.knowledge]
        possible_rooms = [card for card in rooms.keys() if card in self.knowledge]
        
        # Make accusation if we have exactly one possibility in each category
        if len(possible_characters) == 1 and len(possible_weapons) == 1 and len(possible_rooms) == 1:
            return True, (possible_characters[0], possible_weapons[0], possible_rooms[0])
        
        return False, None
    
    def get_player_id_by_name(self, name):
        for pid, pname in players.items():
            if pname.lower() == name.lower():
                return pid
        return None
    
    def get_weapon_id_by_name(self, name):
        for wid, wname in weapons.items():
            if wname.lower() == name.lower():
                return wid
        return None
    
    def get_room_id_by_name(self, name):
        for rid, rname in rooms.items():
            if rname.lower() == name.lower():
                return rid
        return None
    
    def get_card_name(self, card_id):
        if card_id in rooms:
            return rooms[card_id]
        elif card_id in players:
            return players[card_id]
        elif card_id in weapons:
            return weapons[card_id]
        return f"Unknown card {card_id}"
    
    def get_player_hand_names(self):
        return [self.get_card_name(card) for card in self.card_hand]