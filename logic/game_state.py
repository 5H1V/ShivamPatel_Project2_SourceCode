import random
from game_config import doors, rooms, players, weapons, secret_passages, board_labels

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
        """
        Function for making suggestion based on player, weapon, room name
        """
        person_id = None
        weapon_id = None
        room_id = None
        
        # Finding person, weapon, room ids based on names
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
        print(f"I suggest it was {person_name}, with the {weapon_name}, in the {room_name}")
        # Clockwise order, checking to see if anyone has a card in hand
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

                # Updating AI knowledge
                for ai_player_name, ai_player_state in player_states.items():
                    if ai_player_state.is_ai:
                        # Someone showed AI a card, update knowledge
                        ai_player_state.update_AI_on_cards_shown(other_player, shown_card)
                
                        # Someone did not show AI a card, still uncertain, update knowledge
                        if players_who_couldnt_refute:
                            ai_player_state.update_AI_on_refutations(suggestion, players_who_couldnt_refute)
                
                # Removing shown card from possible solutions
                suggesting_player_state = player_states.get(player)
                if hasattr(suggesting_player_state, 'knowledge') and shown_card in suggesting_player_state.knowledge:
                    suggesting_player_state.knowledge.remove(shown_card)
                return shown_card
            else:
                players_who_couldnt_refute.append(other_player)
        
        print("No one shows any card")
        
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
            elif (x,y) in doors:
                if board[y+1, x] in rooms:
                    return board[y+1, x]
                elif board[y, x+1] in rooms:
                    return board[y, x+1]
                elif board[y-1, x] in rooms:
                    return board[y-1, x]
                elif board[y, x-1] in rooms:
                    return board[y, x-1]
        return None
    
    def can_use_secret_passage(self, room_id):
        return room_id in secret_passages
    
    def find_secret_position(self, room_id, board):
        if room_id == 10:  # Study
            return (6,4)
        elif room_id == 7: # Kitchen
            return (21,17)
        elif room_id == 4: # Conservatory
            return (19, 6)
        elif room_id == 9: # Lounge
            return (4, 18)
        return None
    
    def use_secret_passage(self, player_name, player_states, board, current_room):
        """
        If a player is in a room containing secret passage, this will put them at the doorway of the other end
        """
        target_room = secret_passages.get(current_room)
        if target_room:
            target_pos = self.find_secret_position(target_room, board)
            if target_pos:
                player_states.get(player_name).current_position = target_pos
                return target_room
        return None
    
    def make_suggestion_in_room(self, player_states, player_name, room_id):
        """
        Function to make a suggestion when inside a room
        """
        room_name = rooms[room_id]
        player_state = player_states.get(player_name)
                
        if player_state.is_ai:
            suggestion = player_state.make_ai_suggestion(room_id)
            if suggestion:
                character_id, weapon_id, room_id = suggestion
                character_name = players[character_id]
                weapon_name = weapons[weapon_id]
                shown_card = self.make_suggestion(player_states, player_name, character_name, weapon_name, room_name)
        else:
            make_suggestion = input("Suggestion (yes/no): ").lower().strip()
            if make_suggestion == "yes":
                available = player_state.knowledge
                available_cards = [players[i] for i in available if i in players] + [weapons[i] for i in available if i in weapons] + [rooms[i] for i in available if i in rooms]
                print("Available cards: ", available_cards)
                character_name = input("Suggest a character: ").strip()
                weapon_name = input("Suggest a weapon: ").strip()
                shown_card = self.make_suggestion(player_states, player_name, character_name, weapon_name, room_name)
                if shown_card:
                    print(f"Your suggestion was incorrect.")
                else:
                    print("Could not find matching cards")
    
    def ask_for_accusation(self, player_states, player_name):
        """
        Ask if player wants to make an accusation on any turn
        """
        player_state = player_states.get(player_name)
        
        if player_state.is_ai:
            should_accuse, accusation = player_state.should_make_accusation()
            if should_accuse:
                character_id, weapon_id, room_id = accusation
                character_name = players[character_id]
                weapon_name = weapons[weapon_id]
                room_name_acc = rooms[room_id]
                return self.make_accusation(player_states, player_name, character_name, weapon_name, room_name_acc)
            return False
        else:
            accuse = input("Accusation (yes/no): ").lower().strip()
            if accuse == "yes":
                available = player_state.knowledge
                available_cards = [players[i] for i in available if i in players] + [weapons[i] for i in available if i in weapons] + [rooms[i] for i in available if i in rooms]
                print("Available cards: ", available_cards)
                character = input("Accuse a character: ").strip()
                weapon = input("Accuse a weapon: ").strip()
                room = input("Accuse a room: ").strip()
                

                return self.make_accusation(player_states, player_name, character, weapon, room)
            
            return False
    
    def make_accusation(self, player_states, player, person_name, weapon_name, room_name):
        """
        Making accusation for person, weapon, room
        """
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
        """
        Checking if game is over based on winner, number of players remaining
        """
        if self.game_won:
            return True
        active_players = self.get_active_players(player_states)
        return len(active_players) <= 1
    
    def get_winner(self, player_states):
        """
        Retrieving winner for CLI purposes
        """
        if self.winner:
            return self.winner
        active_players = self.get_active_players(player_states)
        if len(active_players) == 1:
            return active_players[0]
        return None
    
    def get_solution_string(self):
        """
        Retrieving solution for CLI purposes
        """
        room_name = rooms.get(self.solution['room'], 'Unknown Room')
        player_name = players.get(self.solution['player'], 'Unknown Player')
        weapon_name = weapons.get(self.solution['weapon'], 'Unknown Weapon')
        return f"{player_name} in the {room_name} with the {weapon_name}"
    
    def move_player(self, player_states, player_name, steps, board, current_room):
        """
        Moving player for each turn
        """
        current_pos = player_states.get(player_name).current_position

        if player_states.get(player_name).is_ai:
            new_pos = self.ai_move(current_pos, steps, board)
            player_states.get(player_name).current_position = new_pos
            print(f"{player_name} moves to {new_pos}")
        else:
            new_pos = current_pos
            remaining_steps = steps
            # If player is in a room, move them out of it
            if current_room:
                y, x = new_pos
                if board[y-1, x] == board_labels["Empty"]:
                    direction = "UP"
                    test_pos = (y-1, x)
                elif board[y+1, x] == board_labels["Empty"]:
                    direction = "DOWN"
                    test_pos = (y+1, x)
                elif board[y, x+1] == board_labels["Empty"]:
                    direction = "RIGHT"
                    test_pos = (y, x+1)
                elif board[y, x-1] == board_labels["Empty"]:
                    direction = "LEFT"
                    test_pos = (y, x-1)
                new_pos = test_pos
                remaining_steps -= 1
                print(f"Moved to {new_pos}")
                current_room = self.get_current_room(new_pos, board)
            while remaining_steps > 0:
                print(f"Remaining steps: {remaining_steps}")
                direction = input("Enter your move (e.g., UP, DOWN, LEFT, RIGHT) or DONE to exit: ").upper()

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
        """
        AI random movement. Will enter a room when it has the chance.
        Have to update to avoid infinite loops.
        """
        new_pos = current_pos
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for step in range(steps):
            random.shuffle(directions)
            moved = False
            for dy, dx in directions:
                test_pos = (new_pos[0] + dy, new_pos[1] + dx)
                if self.is_valid_position(test_pos, board):
                    new_pos = test_pos
                    moved = True
                    if self.get_current_room(new_pos, board):
                        break
                    break
            if not moved:
                break

        return new_pos
    
    def is_valid_position(self, pos, board):
        """
        Checking if position to move to is valid depending on board value.
        Need to fix room walls to be -1 instead of part of room.
        """
        y, x = pos
        if y < 0 or y >= board.shape[0] or x < 0 or x >= board.shape[1]:
            return False
        cell_value = board[y, x]
        return cell_value in [board_labels["Empty"], board_labels["Door"]]