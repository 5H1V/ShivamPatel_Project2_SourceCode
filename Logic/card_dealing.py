import random
from game_config import rooms, players, weapons

def deal_cards(player_names, solution_cards):
    """Deal cards to players, excluding the solution cards"""
    # Create full deck
    all_cards = list(rooms.keys()) + list(players.keys()) + list(weapons.keys())
    
    # Remove solution cards from deck
    remaining_cards = [card for card in all_cards if card not in solution_cards]
    
    # Shuffle the remaining cards
    random.shuffle(remaining_cards)
    
    # Initialize hands
    card_hands = {player: [] for player in player_names}
    
    # Deal cards evenly
    current_player = 0
    for card in remaining_cards:
        player_name = player_names[current_player]
        card_hands[player_name].append(card)
        current_player = (current_player + 1) % len(player_names)
    
    # Print hands for debugging (remove in production)
    print("\n=== CARD DISTRIBUTION ===")
    for player, cards in card_hands.items():
        card_names = []
        for card in cards:
            if card in rooms:
                card_names.append(f"Room: {rooms[card]}")
            elif card in players:
                card_names.append(f"Player: {players[card]}")
            elif card in weapons:
                card_names.append(f"Weapon: {weapons[card]}")
        print(f"{player}: {card_names}")
    print("========================\n")
    
    return card_hands