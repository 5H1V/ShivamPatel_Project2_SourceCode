import pytest
from logic.card_dealing import deal_cards
from game_config import players, solution

def test_deal_cards():
    hands = deal_cards(players, solution)

    assert all(len(hand) >= 3 for hand in hands.values())

    all_cards = [card for hand in hands.values() for card in hand]
    assert len(set(all_cards)) == len(all_cards)

    for sol_card in solution:
        assert sol_card not in all_cards
