import random
import numpy as np


class CardSetup:
    def __init__(self):
        return

    player_colors = {"scarlet" : "Miss Scarlett",
                     "mustard" : "Colonel Mustard",
                     "white" : "Mrs. White",
                     "green" : "Reverend Green",
                     "peacock" : "Mrs. Peacock",
                     "plum" : "Professor Plum"}

    players = {0 : "Miss Scarlett",
               1 : "Colonel Mustard",
               2 : "Mrs. White",
               3 : "Reverend Green",
               4 : "Mrs. Peacock",
               5 : "Professor Plum"}

    weapons = {6 : "Candlestick",
               7 : "Dagger",
               8 : "Lead Pipe",
               9 : "Revolver",
               10 : "Rope",
               11 : "Wrench"}

    rooms = {12 : "Ballroom",
             13 : "BillardRoom",
             14 : "Conservatory",
             15 : "DiningRoom",
             16 : "Hall",
             17 : "Kitchen",
             18 : "Library",
             19 : "Lounge",
             20 : "Study"}

    def solution(players, weapons, rooms):
        player_sol = np.random.randint(0,6)
        weapon_sol = np.random.randint(6,12)
        room_sol = np.random.randint(12,21)
    
        return {player_sol : players[player_sol],
                weapon_sol : weapons[weapon_sol],
                room_sol : rooms[room_sol]}

    def hand_out_cards(players, weapons, rooms, solution):
        remaining_cards = [card for card in range(21) if card not in solution]
        random.shuffle(remaining_cards)
        num_cards = len(remaining_cards)/len(players)
        card_hands = {player: [] for player in players}
        for player, hand in card_hands.items():
            hand[player:player+3] = remaining_cards[player*3:player*3+3]

        return card_hands


if __name__=="__main__":
   players = CardSetup.players
   weapons = CardSetup.weapons
   rooms = CardSetup.rooms

   solution = CardSetup.solution(players, weapons, rooms)
   print(CardSetup.hand_out_cards(players, weapons, rooms, solution))

