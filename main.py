import random
import numpy as np
from game_config import board_labels, rooms, players, weapons, player_start_positions, get_solution
from board.DrawBoard import draw_board, position_matrix
from logic.card_dealing import deal_cards
from logic.player_state import Player
from logic.game_state import CluedoGame

def main():
    print("Welcome to Cluedo!")
    print("===================")
    
    # Setup game
    board = np.full((25, 25), board_labels["Empty"], dtype=int)
    board = position_matrix(board)
    
    # Get number of AI players
    while True:
        try:
            num_ai = int(input("How many AI players do you want? (0-5): "))
            if 0 <= num_ai <= 5:
                break
            print("Please enter a number between 0 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Select players (mix of human and AI)
    all_player_names = list(players.values())
    random.shuffle(all_player_names)
    
    if num_ai == 6:
        selected_players = all_player_names
        human_players = []
        ai_players = selected_players
    else:
        num_human = 6 - num_ai
        selected_players = all_player_names[:6]  # Use all 6 characters
        ai_players = selected_players[:num_ai]
        human_players = selected_players[num_ai:]
    
    print(f"Players in game:")
    for i, player_name in enumerate(selected_players):
        player_type = "AI" if player_name in ai_players else "Human"
        print(f"{i+1}. {player_name} ({player_type})")
    
    # Generate solution
    game_solution = get_solution()
    print(f"DEBUG: Solution is {rooms[game_solution['room']]}, {players[game_solution['player']]}, {weapons[game_solution['weapon']]}")
    
    # Deal cards
    card_hands = deal_cards(selected_players, [game_solution['room'], game_solution['player'], game_solution['weapon']])
    
    # Create player states
    player_states = {}
    for name in selected_players:
        is_ai = name in ai_players
        player_states[name] = Player(name, card_hands, is_ai)
        player_states[name].eliminated = False
    
    # Create game
    game = CluedoGame(player_states, board, game_solution)
    
    # Draw initial board
    positions = {name: state.current_position for name, state in player_states.items()}
    draw_board(board, positions)
    
    print(f"\nGame Start!\n")
    
    # Main game loop
    turn_count = 0
    max_turns = 100  # Prevent infinite games
    
    while not game.is_game_over(player_states) and turn_count < max_turns:
        current_player = game.get_current_player()
        player_state = player_states.get(current_player)
        
        if player_state.eliminated:
            game.next_player()
            continue
        
        turn_count += 1
        print(f"\n=== Turn {turn_count}: {current_player}'s turn ===")
        
        if player_state.is_ai:
            print(f"{current_player} (AI) is taking their turn...")
            play_ai_turn(game, player_states, current_player, board)
        else:
            play_human_turn(game, player_states, current_player, board)
        
        if game.is_game_over(player_states):
            break
        
        game.next_player()
        
        # Show game state every 5 turns
        if turn_count % 5 == 0:
            print(f"\n--- Turn {turn_count} Summary ---")
            active_players = game.get_active_players(player_states)
            print(f"Active players: {', '.join(active_players)}")
            if game.eliminated:
                print(f"Eliminated players: {', '.join(game.eliminated)}")
    
    if turn_count >= max_turns:
        print(f"\nGame ended after {max_turns} turns.")
    
    print_game_results(game, player_states)

def play_human_turn(game, player_states, player_name, board):
    """Handle a human player's turn"""
    player_state = player_states.get(player_name)
    
    # Show player's cards
    player_card_names = player_state.get_player_hand_names()
    print(f"Your cards: {', '.join(player_card_names)}")
    
    current_pos = player_state.current_position
    print(f"Current position: {current_pos}")
    
    # Check if in room
    current_room = game.get_current_room(current_pos, board)
    if current_room:
        room_name = rooms[current_room]
        print(f"You are in the {room_name}.")
        
        # Check for secret passage
        if game.can_use_secret_passage(current_room):
            use = input("You are in a room with a secret passage. Use it? (yes/no): ").lower().strip()
            if use == "yes":
                new_room = game.use_secret_passage(player_name, player_states, board, current_room)
                if new_room:
                    new_room_name = rooms[new_room]
                    print(f"{player_name} used a secret passage to the {new_room_name}.")
                    game.make_suggestion_in_room(player_states, player_name, new_room)
                    
                    if game.ask_for_accusation(player_states, player_name):
                        return
                    return
    
    # Roll dice and move
    input("Press Enter to roll the dice...")
    steps = random.randint(1, 6)
    print(f"{player_name} rolled a {steps}.")
    
    success, new_room = game.move_player(player_states, player_name, steps, board)
    
    if success and new_room:
        room_name = rooms[new_room]
        print(f"{player_name} entered the {room_name}.")
        game.make_suggestion_in_room(player_states, player_name, new_room)
    elif not success:
        print("Movement completed.")
    
    # Final check for accusation
    game.ask_for_accusation(player_states, player_name)

def play_ai_turn(game, player_states, player_name, board):
    """Handle an AI player's turn"""
    player_state = player_states.get(player_name)
    
    current_pos = player_state.current_position
    current_room = game.get_current_room(current_pos, board)
    
    # AI checks for accusation first
    if game.ask_for_accusation(player_states, player_name):
        return
    
    if current_room:
        room_name = rooms[current_room]
        print(f"{player_name} is in the {room_name}.")
        
        # Check for secret passage
        if game.can_use_secret_passage(current_room):
            if random.choice([True, False]):  # 50% chance to use secret passage
                new_room = game.use_secret_passage(player_name, player_states, board, current_room)
                if new_room:
                    new_room_name = rooms[new_room]
                    print(f"{player_name} used a secret passage to the {new_room_name}.")
                    game.make_suggestion_in_room(player_states, player_name, new_room)
                    return
    
    # Roll dice and move
    steps = random.randint(1, 6)
    print(f"{player_name} rolled a {steps}.")
    
    success, new_room = game.move_player(player_states, player_name, steps, board)
    
    if success and new_room:
        room_name = rooms[new_room]
        print(f"{player_name} entered the {room_name}.")
        game.make_suggestion_in_room(player_states, player_name, new_room)

def print_game_results(game, player_states):
    """Print the final game results"""
    print("\n" + "="*60)
    print("GAME OVER")
    print("="*60)
    
    winner = game.get_winner(player_states)
    if winner:
        player_type = "(AI)" if player_states[winner].is_ai else "(Human)"
        print(f"{winner} {player_type} wins the game!")
    else:
        print("No winner - all players eliminated!")
    
    print(f"\nThe correct solution was: {game.get_solution_string()}")
    
    eliminated_players = [name for name, state in player_states.items() if state.eliminated]
    if eliminated_players:
        print(f"Eliminated players: {', '.join(eliminated_players)}")
    
    # Show final knowledge state for debugging
    print(f"\nFinal player knowledge:")
    for name, state in player_states.items():
        if state.is_ai:
            remaining_knowledge = [game.get_card_name(card) for card in state.knowledge]
            print(f"{name} (AI) still thought these could be the solution: {remaining_knowledge}")
    
    print("\nThank you for playing Cluedo!")

if __name__ == "__main__":
    main()