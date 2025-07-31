import random
from game_config import get_all_cards

def deal_cards(player_names, solution_cards):
    """
    Handing out cards to players from the deck without the solution cards
    """
    # All cards, including solution cards
    all_cards = get_all_cards()
    
    # Cards available to hand out, excluding solution cards
    remaining_cards = [card for card in all_cards if card not in solution_cards]
    
    # Shuffling deck
    random.shuffle(remaining_cards)
    
    # Creating dictionary for player and their respective cards
    card_hands = {player: [] for player in player_names}

    # Dealing out cards, making sure they are all distributed with some players having more than others
    current_player = 0
    for card in remaining_cards:
        player_name = player_names[current_player]
        card_hands[player_name].append(card)
        current_player = (current_player + 1) % len(player_names)
    
    return card_hands