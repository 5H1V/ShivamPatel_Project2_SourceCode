from Board.BoardBuilder import position_matrix
from Board.DrawBoard import drawBoard
from Logic.CardStates import hand_out_cards
from Logic.PlayerStates import PlayerStates
from game_config import players, starting_positions, solution

def main():
    # Build and display board
    board = position_matrix()
    drawBoard(board)

    # Initialize players
    player_states = {
        name: PlayerStates(name, pos)
        for name, pos in zip(players.values(), starting_positions)
    }

    # Deal cards
    card_hands = hand_out_cards(players.values(), solution)
    for name, cards in card_hands.items():
        player_states[name].cards = cards

    # Output each player's cards
    for name, state in player_states.items():
        print(f"{name} cards: {state.cards}")

if __name__ == "__main__":
    main()
