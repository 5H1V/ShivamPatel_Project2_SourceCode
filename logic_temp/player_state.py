import random
from game_config import players, weapons, rooms, player_start_positions, get_all_cards

class Player:
    def __init__(self, name, card_hand, is_ai=False):
        self.name = name
        self.index = [key for key, value in players.items() if value == name][0]
        self.starting_position = player_start_positions.get(name)
        self.card_hand = card_hand.get(name, [])
        self.current_position = player_start_positions.get(name)
        self.knowledge = get_all_cards().copy()
        self.eliminated = False
        self.game_won = False
        self.winner = None
        self.is_ai = is_ai
        
        # Tracking AI knowledge
        if is_ai:
            self.player_cards = {}
            self.player_no_cards = {}
            self.suggestions_made = []
            self.refutations_seen = []
            
            for player_name in players.values():
                if player_name != name:
                    self.player_cards[player_name] = set()
                    self.player_no_cards[player_name] = set()
        
        # Removing AI's cards from solution since they cannot be in solution
        for card in self.card_hand:
            if card in self.knowledge:
                self.knowledge.remove(card)

    def update_AI_on_cards_shown(self, showing_player, card_id):
        """
        Updating the knowledge AI has based on cards shown
        """
        if self.is_ai and showing_player in self.player_cards:
            self.player_cards[showing_player].add(card_id)
            if card_id in self.knowledge:
                self.knowledge.remove(card_id)
    
    def update_AI_on_refutations(self, suggestion, players_checked):
        """
        Updating the knowledge AI has for other players' cards, what they cannot be
        """
        if self.is_ai:
            for player_name in players_checked:
                if player_name in self.player_no_cards:
                    for card_id in suggestion:
                        self.player_no_cards[player_name].add(card_id)
    
    def make_ai_suggestion(self, current_room_id):
        """
        AI makes suggestion based on knowledge
        """
        if not self.is_ai:
            return None
        
        # All possible characters, weapons that are still unknown (self.knowledge)
        possible_characters = [card for card in players.keys() if card in self.knowledge]
        possible_weapons = [card for card in weapons.keys() if card in self.knowledge]
        
        # If there is no uncertainty, list all cards as possibilities
        if not possible_characters:
            possible_characters = list(players.keys())
        if not possible_weapons:
            possible_weapons = list(weapons.keys())
        
        character = random.choice(possible_characters)
        weapon = random.choice(possible_weapons)
        
        return character, weapon, current_room_id

    def should_make_accusation(self):
        """
        Deciding if AI should make an accusation based on number cards left per category
        AI will only make accusation if 1 card left in each category
        """
        if not self.is_ai:
            return False, None
        
        possible_characters = [card for card in players.keys() if card in self.knowledge]
        possible_weapons = [card for card in weapons.keys() if card in self.knowledge]
        possible_rooms = [card for card in rooms.keys() if card in self.knowledge]
        
        if len(possible_characters) == 1 and len(possible_weapons) == 1 and len(possible_rooms) == 1:
            return True, (possible_characters[0], possible_weapons[0], possible_rooms[0])
        
        return False, None
        
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