import random
import numpy as np


def hand_out_cards(players, solution):
    remaining_cards = [card for card in range(2,23) if card not in solution]
    random.shuffle(remaining_cards)
    card_hands = {player: [] for player in players}
    while remaining_cards:
        for player in players:
            if remaining_cards:
                card_hands[player].append(remaining_cards.pop())

    return card_hands
