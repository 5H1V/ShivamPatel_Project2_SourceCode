import random
from game_config import rooms, players, weapons, secret_passages, board_labels

class CluedoGame:
    def __init__(self, player_states, board, solution):
        self.player_names = list(player_states.keys())
        self.board = board
        self.card_hands = {name: player.card_hand for name, player in player_states.items()}
        self.solution = solution
        self.current_player_index = 0
        self.eliminated = []
        self.game_won = False
        self.winner = None
        
        # Tracking character and weapon positions
        self.character_positions = {}
        self.weapon_positions = {}
        
        for player_name, player_state in player_states.items():
            self.character_positions[player_name] = player_state.current_position
    
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
        person_id = None
        weapon_id = None
        room_id = None
        
        # Find card IDs
        for pid, pname in players.items():
            if pname.lower() == person_name.lower():
                person_id = pid
                break
        for wid, wname in weapons.items():
            if wname.lower() == weapon_name.lower():
                weapon_id = wid
                break
        for rid, rname in rooms.items():
            if rname.lower() == room_name.lower():
                room_id = rid
                break
        
        if not all([person_id, weapon_id, room_id]):
            print("Could not find matching cards")
            return None
        
        suggestion = [person_id, weapon_id, room_id]
        print(f"Suggestion: {[person_name, weapon_name, room_name]}")

        # Check players in clockwise order starting from the next player
        player_index = self.player_names.index(player)
        players_who_couldnt_refute = []

        for i in range(1, len(self.player_names)):
            other_index = (player_index + i) % len(self.player_names)
            other_player = self.player_names[other_index]
            
            if player_states.get(other_player).eliminated:
                players_who_couldnt_refute.append(other_player)
                continue
            
            hand = self.card_hands[other_player]
            matching_cards = [card for card in suggestion if card in hand]
            
            if matching_cards:
                shown_card = random.choice(matching_cards)
                shown_card_name = self.get_card_name(shown_card)
                
                print(f"{other_player} shows {shown_card_name} card")
                
                # Update AI knowledge for all AI players
                for ai_player_name, ai_player_state in player_states.items():
                    if ai_player_state.is_ai:
                        if ai_player_name == player:
                            # The AI made the suggestion and saw the card
                            ai_player_state.update_AI_on_cards_shown(other_player, shown_card)
                        else:
                            # The AI observed that someone could refute but didn't see the card
                            # Remove the suggestion from their knowledge with some probability
                            pass
                
                # Remove from suggesting player's knowledge
                if shown_card in player_states.get(player).knowledge:
                    player_states.get(player).knowledge.remove(shown_card)

                return shown_card
            else:
                players_who_couldnt_refute.append(other_player)
        
        print("No one shows any card")
        
        # Update AI knowledge - no one had any of these cards
        for ai_player_name, ai_player_state in player_states.items():
            if ai_player_state.is_ai:
                ai_player_state.update_AI_on_refutations(suggestion, players_who_couldnt_refute)
        
        return None
    
    def get_card_name(self, card_id):
        if card_id in rooms:
            return rooms[card_id]
        elif card_id in players:
            return players[card_id]
        elif card_id in weapons:
            return weapons[card_id]
        return f"Unknown card {card_id}"
    
    def get_current_room(self, position, board):
        y, x = position
        if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
            cell_value = board[y, x]
            if cell_value in rooms:
                return cell_value
        return None
    
    def can_use_secret_passage(self, room_id):
        return room_id in secret_passages
    
    def find_room_position(self, room_id, board):
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                if board[y, x] == room_id:
                    return (y, x)
        return None
    
    def use_secret_passage(self, player_name, player_states, board, current_room):
        target_room = secret_passages.get(current_room)
        if target_room:
            target_pos = self.find_room_position(target_room, board)
            if target_pos:
                player_states.get(player_name).current_position = target_pos
                return target_room
        return None
    
    def make_suggestion_in_room(self, player_states, player_name, room_id):
        room_name = rooms[room_id]
        player_state = player_states.get(player_name)
                
        if player_state.is_ai:
            # AI makes suggestion
            suggestion = player_state.make_ai_suggestion(room_id)
            if suggestion:
                character_id, weapon_id, room_id = suggestion
                character_name = players[character_id]
                weapon_name = weapons[weapon_id]
                shown_card = self.make_suggestion(player_states, player_name, character_name, weapon_name, room_name)
        else:
            # Human player makes suggestion
            make_suggestion = input("Suggestion (yes/no): ").lower().strip()
            if make_suggestion == "yes":
                available_players = list(players.values())
                available_weapons = list(weapons.values())
                
                print("Available characters: ", available_players)
                print("Available weapons: ", available_weapons)
                
                character_name = input("Suggest a character: ").strip()
                weapon_name = input("Suggest a weapon: ").strip()
                
                shown_card = self.make_suggestion(player_states, player_name, character_name, weapon_name, room_name)
                if shown_card:
                    print(f"Your suggestion was incorrect.")
                else:
                    print("Could not find matching cards")
    
    def ask_for_accusation(self, player_states, player_name):
        player_state = player_states.get(player_name)
        
        if player_state.is_ai:
            # AI decides whether to make accusation
            should_accuse, accusation = player_state.should_make_accusation()
            if should_accuse:
                character_id, weapon_id, room_id = accusation
                character_name = players[character_id]
                weapon_name = weapons[weapon_id]
                room_name_acc = rooms[room_id]
                return self.make_accusation(player_states, player_name, character_name, weapon_name, room_name_acc)
            return False
        else:
            # Human player decides
            accuse = input("Accusation (yes/no): ").lower().strip()
            
            if accuse == "yes":
                available_players = list(players.values())
                available_weapons = list(weapons.values())
                available_rooms = list(rooms.values())
                
                print("Available characters: ", available_players)
                print("Available weapons: ", available_weapons)
                print("Available rooms: ", available_rooms)
                
                character = input("Accuse a character: ").strip()
                weapon = input("Accuse a weapon: ").strip()
                room = input("Accuse a room: ").strip()
                
                return self.make_accusation(player_states, player_name, character, weapon, room)
            
            return False
    
    def make_accusation(self, player_states, player, person_name, weapon_name, room_name):
        person_id = None
        weapon_id = None
        room_id = None
        
        for pid, pname in players.items():
            if pname.lower() == person_name.lower():
                person_id = pid
                break
        for wid, wname in weapons.items():
            if wname.lower() == weapon_name.lower():
                weapon_id = wid
                break
        for rid, rname in rooms.items():
            if rname.lower() == room_name.lower():
                room_id = rid
                break
        
        if not all([person_id, weapon_id, room_id]):
            print("Could not find matching cards")
            return False
        
        print(f"Accusation: {[person_name, weapon_name, room_name]}")

        accusation_correct = (person_id == self.solution['player'] and 
                            weapon_id == self.solution['weapon'] and 
                            room_id == self.solution['room'])
        
        if accusation_correct:
            print(f"{player} wins!")
            player_states.get(player).game_won = True
            player_states.get(player).winner = True
            self.game_won = True
            self.winner = player
            return True
        else:
            print(f"{player} was wrong and is eliminated")
            player_states.get(player).eliminated = True
            self.eliminated.append(player)
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
        
        if player_states.get(player_name).is_ai:
            # AI movement - simplified random valid movement
            new_pos = self.ai_move(current_pos, steps, board)
            player_states.get(player_name).current_position = new_pos
            print(f"{player_name} moves to {new_pos}")
        else:
            # Human movement
            print("Available directions (UP, DOWN, LEFT, RIGHT): ")
            new_pos = current_pos
            remaining_steps = steps
            
            while remaining_steps > 0:
                print(f"Remaining steps: {remaining_steps}")
                direction = input("Enter direction (UP/DOWN/LEFT/RIGHT) or DONE to exit: ").upper()
                if direction == "DONE":
                    break
                if direction not in ["UP", "DOWN", "LEFT", "RIGHT"]:
                    print("Invalid direction.")
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
                    print("Invalid location, structure in the way")
            
            player_states.get(player_name).current_position = new_pos
        
        current_room = self.get_current_room(new_pos, board)
        return True, current_room
    
    def ai_move(self, current_pos, steps, board):
        """Simple AI movement - try to enter a room"""
        new_pos = current_pos
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        
        for _ in range(steps):
            random.shuffle(directions)
            moved = False
            for dy, dx in directions:
                test_pos = (new_pos[0] + dy, new_pos[1] + dx)
                if self.is_valid_position(test_pos, board):
                    new_pos = test_pos
                    moved = True
                    # If we found a room, stop moving
                    if self.get_current_room(new_pos, board):
                        break
                    break
            if not moved:
                break
        
        return new_pos
    
    def is_valid_position(self, pos, board):
        y, x = pos
        if y < 0 or y >= board.shape[0] or x < 0 or x >= board.shape[1]:
            return False
        cell_value = board[y, x]
        return cell_value != board_labels["Invalid"]