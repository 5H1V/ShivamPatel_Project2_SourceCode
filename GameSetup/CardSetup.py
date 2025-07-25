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

    rooms = {2 : "Ballroom",
             3 : "BillardRoom",
             4 : "Conservatory",
             5 : "DiningRoom",
             6 : "Hall",
             7 : "Kitchen",
             8 : "Library",
             9 : "Lounge",
             10 : "Study"}

    players = {11 : "Miss Scarlett",
               12 : "Colonel Mustard",
               13 : "Mrs. White",
               14 : "Reverend Green",
               15 : "Mrs. Peacock",
               16 : "Professor Plum"}

    weapons = {17 : "Candlestick",
               18 : "Dagger",
               19 : "Lead Pipe",
               20 : "Revolver",
               21 : "Rope",
               22 : "Wrench"}

    def solution(players, weapons, rooms):
        room_sol = np.random.randint(2,11)
        player_sol = np.random.randint(11,17)
        weapon_sol = np.random.randint(17,23)

        return {player_sol : players[player_sol],
                weapon_sol : weapons[weapon_sol],
                room_sol : rooms[room_sol]}

    def hand_out_cards(players, weapons, rooms, solution):
        remaining_cards = [card for card in range(2,23) if card not in solution]
        random.shuffle(remaining_cards)
        card_hands = {player: [] for player in players}
        for i in range(3):
            for player in players:
                if remaining_cards:
                    card_hands[player].append(remaining_cards.pop())

        return card_hands


if __name__=="__main__":
   players = CardSetup.players
   weapons = CardSetup.weapons
   rooms = CardSetup.rooms

   solution = CardSetup.solution(players, weapons, rooms)
   print(CardSetup.hand_out_cards(players, weapons, rooms, solution))

