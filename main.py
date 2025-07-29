from board.board_builder import build_board
from board.visualization import visualize_board
from logic.card_dealing import deal_cards
from logic.player_state import PlayerState
from game_config import players, starting_positions, solution

def main():
    # Build and display board
    board = build_board()
    visualize_board(board)

    # Initialize players
    player_states = {
        name: PlayerState(name, pos)
        for name, pos in zip(players, starting_positions)
    }

    # Deal cards
    card_hands = deal_cards(players, solution)
    for name, cards in card_hands.items():
        player_states[name].cards = cards

    # Output each player's cards
    for name, state in player_states.items():
        print(f"{name} cards: {state.cards}")

if __name__ == "__main__":
    main()
