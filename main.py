import random
import numpy as np
from game_config import solution, board_labels, rooms, players, weapons, player_start_positions
from board.DrawBoard import draw_board, position_matrix
from logic.card_dealing import deal_cards
from logic.player_state import Player
from logic.game_state import CluedoGame


def main():
    print("Cluedo!")
    print("===================")

    board = np.full((25, 25), board_labels["Empty"], dtype=int)

    player_names = list(players.values())
    board = position_matrix(board)

    game_solution = solution
    print(f"DEBUG: Solution is {rooms[game_solution['room']]}, {players[game_solution['player']]}, {weapons[game_solution['weapon']]}")
    
    card_hands = deal_cards(player_names, [game_solution['room'], game_solution['player'], game_solution['weapon']])
    
    player_states = {name: Player(name, card_hands) for name in player_names}
    for player, state in player_states.items():
        state.eliminated = False

    game = CluedoGame(player_states, board, game_solution)
    
    positions = {name: state.current_position for name, state in player_states.items()}

    draw_board(board, positions)

    print(f"\nGame Start!")

    # Main game loop
    turn_count = 0
    while not game.is_game_over(player_states):
        current_player = game.get_current_player()
        
        if player_states.get(player).eliminated:
            game.next_player()
            continue
        
        turn_count += 1

        player_card_names = player_states.get(current_player).get_player_hand_names(current_player)
        print(f"Your cards: {', '.join(player_card_names)}")
        
        current_pos = player_states.get(current_player).current_position
        print(f"Current position: {current_pos}")

        current_room = game.get_current_room(current_pos, board)
        if current_room:
            room_name = rooms[current_room]
            print(f"You are in the {room_name}.")

            if game.can_use_secret_passage(current_room):
                use = input("You are in a room with a secret passage. Use it? (yes/no): ").lower().strip()
                if use == "yes":
                    new_room = game.use_secret_passage(current_player, player_states, board, current_room)
                    if new_room:
                        new_room_name = rooms[new_room]
                        print(f"{current_player} used a secret passage to the {new_room_name}.")

                        game.make_suggestion_in_room(player_states.get(current_player), current_player, new_room)
                        
                        if game.ask_for_accusation(player_states.get(current_player), current_player):
                            break
                        
                        game.next_player()
                        continue


        input("Press Enter to roll the dice...")
        steps = random.randint(1, 6)
        print(f"{current_player} rolled a {steps}.")

        success, new_room = game.move_player(player_states, current_player, steps, board)

        if success and new_room:
            room_name = rooms[new_room]
            print(f"{current_player} entered the {room_name}.")
            game.make_suggestion_in_room(player_states.get(current_player), current_player, new_room)
        elif not success:
            print("Movement completed.")

        if game.ask_for_accusation(player_states.get(current_player), current_player):
            break

        game.next_player()

    print_game_results(game, player_states)


def print_game_results(game, player_states):
    """Print the final game results"""
    print("\n" + "="*60)
    print("GAME OVER")
    print("="*60)
    
    winner = game.get_winner()
    if winner:
        print(f"{winner} wins the game!")
    else:
        print("No winner - all players eliminated!")
    
    print(f"\nThe correct solution was: {game.get_solution_string()}")

    if any(state.eliminated for state in player_states.values()):
        all_eliminated = [name for state in player_states.values() for name in state.eliminated]
        print(f"Eliminated players: {', '.join(all_eliminated)}")

    print("\nThank you for playing Cluedo!")


if __name__ == "__main__":
    main()