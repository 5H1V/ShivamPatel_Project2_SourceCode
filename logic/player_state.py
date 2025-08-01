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
        
        # Removing AI's cards from solution since they cannot be in solution
        for card in self.card_hand:
            if card in self.knowledge:
                self.knowledge.remove(card)

        # Tracking AI knowledge
        if is_ai:
            self.player_cards = {}
            self.player_no_cards = {}
            for player in players.values():
                if player == self.name:
                    continue
                self.player_cards[player] = set()
                self.player_no_cards[player] = set()
                
            self.suggestions_made = []
            self.refutations_seen = []

            # Initializing card probability weights
            self.card_probabilities = {card_id: 1.0/18 for card_id in self.knowledge}

    def update_AI_on_cards_shown(self, showing_player, card_id):
        """
        Updating the knowledge AI has based on cards shown
        """
        if not self.is_ai or showing_player == self.name:
            return
        if showing_player not in self.player_cards:
            return
        self.player_cards[showing_player].add(card_id)
        if card_id in self.card_probabilities:
            self.card_probabilities[card_id] = 0.0
        
    def update_AI_on_refutations(self, suggestion, players_checked):
        """
        Updating the knowledge AI has for other players' cards, what they have not been shown
        """
        if not self.is_ai:
            return
        for player in players_checked:
            if player == self.name:
                continue
            if player not in self.player_no_cards:
                continue
            for card_id in suggestion:
                self.player_no_cards[player].add(card_id)
        
        for card_id in suggestion:
            if card_id in self.card_probabilities:
                self.card_probabilities[card_id] += 1.0
    
    def normalize_probabilities(self):
        """
        Normalizing probabilities to add up to 1 (100%)
        """
        def normalize(category_ids):
            total = sum([self.card_probabilities.get(cid,0) for cid in category_ids])
            return {cid: (self.card_probabilities.get(cid,0)/total if total>0 else 0) for cid in category_ids}
        return {
            "characters": normalize(players.keys()),
            "weapons": normalize(weapons.keys()),
            "rooms": normalize(rooms.keys())
        }

    def make_ai_suggestion(self, current_room_id):
        """
        AI makes suggestion based on knowledge
        """
        if not self.is_ai:
            return None
        
        norm_probs = self.normalize_probabilities()
        
        def pick_most_likely(category_probs):
            # Picking most likely card
            return max(category_probs.items(), key=lambda x: x[1])[0]
        
        character = pick_most_likely(norm_probs["characters"])
        weapon = pick_most_likely(norm_probs["weapons"])
        return character, weapon, current_room_id
        
    def should_make_accusation(self):
        """
        Deciding if AI should make an accusation based on number cards left per category
        """
        if not self.is_ai:
            return False, None
        
        character_probs = {cid: self.card_probabilities[cid] for cid in players if cid in self.knowledge}
        weapon_probs = {wid: self.card_probabilities[wid] for wid in weapons if wid in self.knowledge}
        room_probs = {rid: self.card_probabilities[rid] for rid in rooms if rid in self.knowledge}
        
        def most_likely_one(prob_dict):
            """
            Criteria for if AI should make their accusation
            """
            size_met = len(prob_dict) == 1
            probability_met = max(prob_dict.values()) >= 0.9
            others_probability = all(prob<0.1 for player, prob in prob_dict.items() if player!= max(prob_dict, key=prob_dict.get))
            return size_met or (len(prob_dict)>0 and probability_met and others_probability)
        
        if most_likely_one(character_probs) and most_likely_one(weapon_probs) and most_likely_one(room_probs):
            character = max(character_probs, key=character_probs.get)
            weapon = max(weapon_probs, key=weapon_probs.get)
            room = max(room_probs, key=room_probs.get)
            return True, (character, weapon, room)
        
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