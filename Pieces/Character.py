class Character:

    def __init__(self, characters, position):

        return
    
    player_colors = {"scarlet" : "Miss Scarlett",
                     "mustard" : "Colonel Mustard",
                     "white" : "Mrs. White",
                     "green" : "Reverend Green",
                     "peacock" : "Mrs. Peacock",
                     "plum" : "Professor Plum"}


"""
Character Definition:

Define the 6 standard Cluedo characters: .

Assign each character a starting position on the board.
"""


"""
Solution Selection:

From the full set of Character, Weapon, and Room cards, randomly select one of each category to form the "murder solution"
(the three cards placed in the confidential envelope). These cards should be hidden from all players throughout the game.
After the solution is selected, the remaining cards (the "deck") must be shuffled and distributed evenly among all active players.
If the number of cards doesn't divide evenly, some players may receive one more card than others.

"""