import random
from game_config import rooms, players, weapons, secret_passages, valid_players, valid_rooms, valid_weapons, solution, board_labels
from logic.player_state import Player

class CluedoGame:
    def __init__(self, player_states, board, solution):
        self.player_names = list(player_states.keys())
        self.board = board
        self.card_hands = [player.card_hand for player in player_states.values()]
        self.solution = solution
        self.current_player_index = 0
        self.eliminated = [player.eliminated for player in player_states.values()]
        self.game_won = False
        self.winner = None

    def get_current_player(self):
        return self.player_names[self.current_player_index]

    def next_player(self):
        original_index = self.current_player_index
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.player_names)
            current_player = self.player_names[self.current_player_index]

            if self.current_player_index == original_index:
                break
            if current_player not in self.eliminated:
                break

    def get_active_players(self, player_states):
        return [player for player in self.player_names if not player_states.get(player).eliminated]

    def make_suggestion(self, player_states, player, person_name, weapon_name, room_name):
        person_id = player_states._get_player_id_by_name(person_name)
        weapon_id = player_states._get_weapon_id_by_name(weapon_name)
        room_id = player_states._get_room_id_by_name(room_name)
        
        if not all([person_id, weapon_id, room_id]):
            print("Invalid suggestion - couldn't find matching cards")
            return None
            
        suggestion = [person_id, weapon_id, room_id]
        print(f"{player} suggests it was {person_name} in the {room_name} with the {weapon_name}.")

        player_index = self.player_names.index(player)
        for i in range(1, len(self.player_names)):
            other_index = (player_index + i) % len(self.player_names)
            other_player = self.player_names[other_index]
            
            if player_states.get(player).eliminated:
                continue
                
            hand = self.card_hands[other_player]
            matching_cards = [card for card in suggestion if card in hand]
            
            if matching_cards:
                shown_card = random.choice(matching_cards)
                shown_card_name = player_states._get_card_name(shown_card)
                print(f"{other_player} shows the {shown_card_name} card to {player}.")

                # MAKE SUGGESTION RETURNS A CARD THAT THE OTHER PLAYER SHOWS.
                # REMOVE THIS CARD FROM THE KNOWLEDGE
                player_states.get(player).knowledge.remove(shown_card_name)
                return shown_card

        print("No one could disprove the suggestion.")
        return None

    def get_current_room(self, position, board):
        y, x = position
        if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
            cell_value = board[y, x]
            if cell_value in rooms:
                return cell_value
        return None

    def can_use_secret_passage(self, room_id):
        return room_id in secret_passages

#----------------------------------------------------#
    ### FIXXXXXXXXXXXXXXXXXXXXXX
    def find_room_position(self, room_id, board):
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                if board[y, x] == room_id:
                    return (y, x)
        return None

    def use_secret_passage(self, player_name, player_states, board, current_room):
        target_room = secret_passages.get(current_room)
        if target_room:
            target_pos = self._find_room_position(target_room, board)
            if target_pos:
                player_states.get(player_name).current_position = target_pos
                return target_room
        return None

    def make_suggestion_in_room(self, player_states, player_name, room_id):
        room_name = rooms[room_id]
        
        print(f"\n{player_name}, you can make a suggestion in the {room_name}.")
        make_suggestion = input("Do you want to make a suggestion? (yes/no): ").lower().strip()

        if make_suggestion == "yes":
            players_list = [name for name in player_states.knowledge if name in valid_players]
            weapons_list = [weapon for weapon in player_states.knowledge if weapon in valid_weapons]
            print("Available characters:", players_list)
            print("Available weapons:", weapons_list)
            
            character_name = input("Suggest a character: ").strip()
            weapon_name = input("Suggest a weapon: ").strip()
            
            shown_card = self.make_suggestion(player_states, player_name, character_name, weapon_name, room_name)

            if shown_card:
                print(f"Your suggestion was disproven.")
            else:
                print("Nobody could disprove your suggestion!")

    def ask_for_accusation(self, player_states, player_name):
        accuse = input("Do you want to make an accusation? (yes/no): ").lower().strip()
        
        if accuse == "yes":
            players_list = [name for name in player_states.knowledge if name in valid_players]
            weapons_list = [weapon for weapon in player_states.knowledge if weapon in valid_weapons]
            rooms_list = [room for room in player_states.knowledge if room in valid_rooms]

            print("Available characters:", players_list)
            print("Available weapons:", weapons_list)
            print("Available rooms:", rooms_list)
            
            character = input("Accuse a character: ").strip()
            weapon = input("Accuse a weapon: ").strip()
            room = input("Accuse a room: ").strip()
            
            if self.make_accusation(player_states, player_name, character, weapon, room):
                return True
            else:
                return False
        
        return False

    def make_accusation(self, player_states, player, person_name, weapon_name, room_name):

        person_id = player_states._get_player_id_by_name(person_name)
        weapon_id = player_states._get_weapon_id_by_name(weapon_name)
        room_id = player_states._get_room_id_by_name(room_name)
        
        accusation = [person_id, weapon_id, room_id]

        if not all(accusation):
            print("Invalid accusation - couldn't find matching cards")
            return False
            
        print(f"{player} accuses {person_name} in the {room_name} with the {weapon_name}!")
        
        accusation_correct = (accusation == [self.solution['player'], self.solution['weapon'], self.solution['room']])
        
        if accusation_correct:
            print(f"{player} wins the game!")
            player_states.get(player).game_won = True
            player_states.get(player).winner = True
            self.game_won = True
            self.winner = player
            return True
        else:
            print(f"{player}'s accusation was incorrect and is eliminated.")
            player_states.get(player).eliminated = True
            return False

    def is_game_over(self, player_states):
        """End game"""
        if self.game_won:
            return True

        active_players = self.get_active_players(player_states)
        return len(active_players) <= 1

    def get_winner(self, player_states):
        """Winner"""
        if self.winner:
            return self.winner

        active_players = self.get_active_players(player_states)
        if len(active_players) == 1:
            return active_players[0]
        
        return None

    def get_solution_string(self):
        room_name = rooms.get(self.solution['room'], 'Unknown Room')
        player_name = players.get(self.solution['player'], 'Unknown Player')
        weapon_name = weapons.get(self.solution['weapon'], 'Unknown Weapon')
        return f"{player_name} in the {room_name} with the {weapon_name}"

    def move_player(self, player_states, player_name, steps, board):
        current_pos = player_states.get(player_name).current_position
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
                
            y, x = new_pos
            if direction == "UP":
                test_pos = (y - 1, x)
            elif direction == "DOWN":
                test_pos = (y + 1, x)
            elif direction == "LEFT":
                test_pos = (y, x - 1)
            elif direction == "RIGHT":
                test_pos = (y, x + 1)
            
            if self.is_valid_position(test_pos, board):
                new_pos = test_pos
                remaining_steps -= 1
                print(f"Moved to {new_pos}")
            else:
                print("Can't move there - blocked by wall or out of bounds.")
        
        player_states.get(player_name).current_position = new_pos

        current_room = self.get_current_room(new_pos, board)
        return True, current_room

    def is_valid_position(self, pos, board):
        y, x = pos
        if y < 0 or y >= board.shape[0] or x < 0 or x >= board.shape[1]:
            return False
        
        cell_value = board[y, x]
        return cell_value != board_labels["Invalid"]

    def print_game_state(self,player_states):
        """Print current game state for debugging"""
        print(f"\n=== GAME STATE ===")
        print(f"Current player: {self.get_current_player()}")
        print(f"Active players: {self.get_active_players(player_states)}")
        print(f"Eliminated players: {[player for player in player_states if player_states.get(player).eliminated]}")
        print(f"Knowledge: {[(player_name, player_state.knowledge) for player_name, player_state in player_states.items()]}")
        print(f"Game over: {self.is_game_over(player_states)}")
        if self.is_game_over(player_states):
            print(f"Winner: {self.get_winner(player_states)}")
        print(f"Solution: {self.get_solution_string()}")
        print("==================\n")
