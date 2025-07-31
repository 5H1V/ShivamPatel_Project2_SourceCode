import random
from game_config import get_all_cards

def deal_cards(player_names, solution_cards):
    """
    Handing out cards to players from the deck without the solution cards
    """
    all_cards = get_all_cards()
    remaining_cards = [card for card in all_cards if card not in solution_cards]
    random.shuffle(remaining_cards)
    card_hands = {player: [] for player in player_names}
    
    current_player = 0
    for card in remaining_cards:
        player_name = player_names[current_player]
        card_hands[player_name].append(card)
        current_player = (current_player + 1) % len(player_names)
        
    return card_hands