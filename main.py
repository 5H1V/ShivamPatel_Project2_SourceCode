import random
import numpy as np
from game_config import solution, board_labels, rooms, players, weapons, player_start_positions
from board.DrawBoard import draw_board, position_matrix
from logic.card_dealing import deal_cards

from logic.game_mechanics import roll_dice, move_player, make_suggestion, use_secret_passage, make_accusation
from logic.game_state import CluedoGame

def main():
    print("Cluedo!")
    print("===================")

    board = np.full((25, 25), board_labels["Empty"], dtype=int)

    player_names = list(players.values())
    board = position_matrix(board)

    game_solution = solution
    print(f"DEBUG: Solution is {rooms[game_solution['room']]}, {players[game_solution['player']]}, {weapons[game_solution['weapon']]}")
    
    # Deal cards (excluding solution cards)
    card_hands = deal_cards(player_names, [game_solution['room'], game_solution['player'], game_solution['weapon']])
    
    # Initialize player states with proper starting positions
    player_states = {}
    for player_name in player_names:
        start_pos = player_start_positions.get(player_name, (12, 12))  # Default center if not found
        player_states[player_name] = {"position": start_pos,"eliminated": False}
    
    # Create game state manager
    game = CluedoGame(player_names, board, card_hands, game_solution)
    
    # Show initial board
    positions = {name: state["position"] for name, state in player_states.items()}
    for y, x in positions.values():
        print(x,y)

    draw_board(board, positions)

    print(f"\nGame Start!")
    #----------------------------------------------------#

    # Main game loop
    turn_count = 0
    while not game.is_game_over():
        current_player = game.get_current_player()
        
        # Skip eliminated players
        if current_player in game.eliminated:
            game.next_player()
            continue
        
        turn_count += 1
        print(f"\n{'='*60}")
        print(f"TURN {turn_count}: {current_player}'s turn")
        print(f"{'='*60}")
        
        # Show player's cards
        player_card_names = game.get_player_hand_names(current_player)
        print(f"Your cards: {', '.join(player_card_names)}")
        
        # Show current position
        current_pos = player_states[current_player]["position"]
        print(f"Current position: {current_pos}")
        
        # Check if in a room
        current_room = get_current_room(current_pos, board)
        if current_room:
            room_name = rooms[current_room]
            print(f"You are in the {room_name}.")
            
            # Check for secret passage
            if can_use_secret_passage(current_room):
                use = input("You are in a room with a secret passage. Use it? (yes/no): ").lower().strip()
                if use == "yes":
                    new_room = use_secret_passage(current_player, player_states, board, current_room)
                    if new_room:
                        new_room_name = rooms[new_room]
                        print(f"{current_player} used a secret passage to the {new_room_name}.")
                        
                        # Make suggestion in new room
                        make_suggestion_in_room(game, current_player, new_room)
                        
                        # Ask for accusation
                        if ask_for_accusation(game, current_player):
                            break
                        
                        game.next_player()
                        continue

        # Roll dice and move
        input("Press Enter to roll the dice...")
        steps = roll_dice()
        print(f"{current_player} rolled a {steps}.")

        # Handle movement
        success, new_room = move_player(current_player, steps, board, player_states)
        
        if success and new_room:
            room_name = rooms[new_room]
            print(f"{current_player} entered the {room_name}.")
            
            # Make suggestion in the room
            make_suggestion_in_room(game, current_player, new_room)
        elif not success:
            print("Movement completed.")

        # Ask for accusation
        if ask_for_accusation(game, current_player):
            break

        # Move to next player
        game.next_player()

    # Game over
    print_game_results(game)

def make_suggestion_in_room(game, player_name, room_id):
    """Handle making a suggestion in a room"""
    room_name = rooms[room_id]
    
    print(f"\n{player_name}, you can make a suggestion in the {room_name}.")
    make_suggestion = input("Do you want to make a suggestion? (yes/no): ").lower().strip()
    
    if make_suggestion == "yes":
        print("Available characters:", list(players.values()))
        print("Available weapons:", list(weapons.values()))
        
        character = input("Suggest a character: ").strip()
        weapon = input("Suggest a weapon: ").strip()
        
        # Make the suggestion through the game state manager
        shown_card = game.make_suggestion(player_name, character, weapon, room_name)
        
        if shown_card:
            print(f"Your suggestion was disproven.")
        else:
            print("Nobody could disprove your suggestion!")

def ask_for_accusation(game, player_name):
    """Ask player if they want to make an accusation"""
    accuse = input("Do you want to make an accusation? (yes/no): ").lower().strip()
    
    if accuse == "yes":
        print("Available characters:", list(players.values()))
        print("Available weapons:", list(weapons.values()))
        print("Available rooms:", list(rooms.values()))
        
        character = input("Accuse a character: ").strip()
        weapon = input("Accuse a weapon: ").strip()
        room = input("Accuse a room: ").strip()
        
        # Make accusation through game state manager
        if game.make_accusation(player_name, character, weapon, room):
            return True  # Game won
        else:
            return False  # Continue game
    
    return False

def print_game_results(game):
    """Print the final game results"""
    print("\n" + "="*60)
    print("GAME OVER")
    print("="*60)
    
    winner = game.get_winner()
    if winner:
        print(f"🎉 {winner} wins the game! 🎉")
    else:
        print("No winner - all players eliminated!")
    
    print(f"\nThe correct solution was: {game.get_solution_string()}")
    
    if game.eliminated:
        print(f"Eliminated players: {', '.join(game.eliminated)}")
    
    print(f"Total suggestions made: {len(game.suggestions)}")
    print("\nThank you for playing Cluedo!")

def get_current_room(position, board):
    """Check if player is in a room"""
    y, x = position
    if 0 <= y < board.shape[0] and 0 <= x < board.shape[1]:
        cell_value = board[y, x]
        if cell_value in rooms:
            return cell_value
    return None

def can_use_secret_passage(room_id):
    """Check if current room has a secret passage"""
    from game_config import secret_passages
    return room_id in secret_passages

if __name__ == "__main__":
    main()