import random
from game_config import rooms, players, weapons

class CluedoGame:
    def __init__(self, player_names, board, card_hands, solution):
        self.player_names = player_names
        self.board = board
        self.card_hands = card_hands
        self.solution = solution
        self.current_player_index = 0
        self.suggestions = []
        self.eliminated = set()
        self.game_won = False
        self.winner = None

    def next_player(self):
        """Move to the next active player"""
        original_index = self.current_player_index
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.player_names)
            current_player = self.player_names[self.current_player_index]
            
            # If we've looped back to the original player, break to avoid infinite loop
            if self.current_player_index == original_index:
                break
                
            # If this player is not eliminated, we found our next player
            if current_player not in self.eliminated:
                break

    def get_current_player(self):
        """Get the current active player"""
        return self.player_names[self.current_player_index]

    def get_active_players(self):
        """Get list of players who haven't been eliminated"""
        return [player for player in self.player_names if player not in self.eliminated]

    def make_suggestion(self, player, person_name, weapon_name, room_name):
        """Handle a player making a suggestion"""
        # Convert names to IDs
        person_id = self._get_player_id_by_name(person_name)
        weapon_id = self._get_weapon_id_by_name(weapon_name)
        room_id = self._get_room_id_by_name(room_name)
        
        if not all([person_id, weapon_id, room_id]):
            print("Invalid suggestion - couldn't find matching cards")
            return None
            
        suggestion = (person_id, weapon_id, room_id)
        self.suggestions.append((player, person_name, weapon_name, room_name))
        print(f"{player} suggests it was {person_name} in the {room_name} with the {weapon_name}.")

        # Check other players to disprove
        player_index = self.player_names.index(player)
        for i in range(1, len(self.player_names)):
            other_index = (player_index + i) % len(self.player_names)
            other_player = self.player_names[other_index]
            
            if other_player in self.eliminated:
                continue
                
            hand = self.card_hands[other_player]
            matching_cards = [card for card in suggestion if card in hand]
            
            if matching_cards:
                shown_card = random.choice(matching_cards)
                shown_card_name = self._get_card_name(shown_card)
                print(f"{other_player} shows the {shown_card_name} card to {player}.")
                return shown_card

        print("No one could disprove the suggestion.")
        return None

    def make_accusation(self, player, person_name, weapon_name, room_name):
        """Handle a player making an accusation"""
        # Convert names to IDs
        person_id = self._get_player_id_by_name(person_name)
        weapon_id = self._get_weapon_id_by_name(weapon_name)
        room_id = self._get_room_id_by_name(room_name)
        
        if not all([person_id, weapon_id, room_id]):
            print("Invalid accusation - couldn't find matching cards")
            return False
            
        print(f"{player} accuses it was {person_name} in the {room_name} with the {weapon_name}!")
        
        # Check if accusation matches solution
        accusation_correct = (
            person_id == self.solution['player'] and
            weapon_id == self.solution['weapon'] and
            room_id == self.solution['room']
        )
        
        if accusation_correct:
            print(f"{player} wins the game!")
            self.game_won = True
            self.winner = player
            return True
        else:
            print(f"{player}'s accusation was incorrect and is eliminated.")
            self.eliminated.add(player)
            return False

    def is_game_over(self):
        """Check if the game is over"""
        if self.game_won:
            return True
            
        active_players = self.get_active_players()
        return len(active_players) <= 1

    def get_winner(self):
        """Get the winner of the game"""
        if self.winner:
            return self.winner
        
        active_players = self.get_active_players()
        if len(active_players) == 1:
            return active_players[0]
        
        return None

    def eliminate_player(self, player):
        """Eliminate a player from the game"""
        self.eliminated.add(player)

    def get_solution_string(self):
        """Get a readable string of the solution"""
        room_name = rooms.get(self.solution['room'], 'Unknown Room')
        player_name = players.get(self.solution['player'], 'Unknown Player')
        weapon_name = weapons.get(self.solution['weapon'], 'Unknown Weapon')
        return f"{player_name} in the {room_name} with the {weapon_name}"

    def _get_player_id_by_name(self, name):
        """Find player ID by name"""
        for pid, pname in players.items():
            if pname.lower() == name.lower():
                return pid
        return None

    def _get_weapon_id_by_name(self, name):
        """Find weapon ID by name"""
        for wid, wname in weapons.items():
            if wname.lower() == name.lower():
                return wid
        return None

    def _get_room_id_by_name(self, name):
        """Find room ID by name"""
        for rid, rname in rooms.items():
            if rname.lower() == name.lower():
                return rid
        return None

    def _get_card_name(self, card_id):
        """Convert card ID to readable name"""
        if card_id in rooms:
            return rooms[card_id]
        elif card_id in players:
            return players[card_id]
        elif card_id in weapons:
            return weapons[card_id]
        return f"Unknown card {card_id}"

    def get_player_hand_names(self, player):
        """Get readable names of cards in player's hand"""
        if player not in self.card_hands:
            return []
        
        return [self._get_card_name(card) for card in self.card_hands[player]]

    def print_game_state(self):
        """Print current game state for debugging"""
        print(f"\n=== GAME STATE ===")
        print(f"Current player: {self.get_current_player()}")
        print(f"Active players: {self.get_active_players()}")
        print(f"Eliminated players: {list(self.eliminated)}")
        print(f"Suggestions made: {len(self.suggestions)}")
        print(f"Game over: {self.is_game_over()}")
        if self.is_game_over():
            print(f"Winner: {self.get_winner()}")
        print(f"Solution: {self.get_solution_string()}")
        print("==================\n")