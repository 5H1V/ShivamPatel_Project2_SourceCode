


"""
Mansion Layout:

Create a representation of the mansion layout with different rooms (e.g., kitchen, library, ballroom, etc.).
This layout can be represented abstractly (e.g., a graph where rooms are nodes and passages are edges) or
concretely (e.g., a 2D grid or array). Ensure that the connections between rooms (i.e., which rooms are adjacent
and allow movement) are clearly defined. Try to include secret passages between certain rooms as per the original
game rules (e.g., Study to Kitchen, Conservatory to Lounge). Define designated starting positions for each character,
typically in hallways or outside specific rooms.

"""

"""
Character Definition:

Define the 6 standard Cluedo characters: Miss Scarlett, Colonel Mustard, Mrs. White, Reverend Green, Mrs. Peacock, and Professor Plum.

Assign each character a starting position on the board.
"""


"""
Weapon Definition:

Define the 6 standard Cluedo weapons: Candlestick, Dagger, Lead Pipe, Revolver, Rope, and Wrench.

"""



"""
Solution Selection:

From the full set of Character, Weapon, and Room cards, randomly select one of each category to form the "murder solution"
(the three cards placed in the confidential envelope). These cards should be hidden from all players throughout the game.
After the solution is selected, the remaining cards (the "deck") must be shuffled and distributed evenly among all active players.
If the number of cards doesn't divide evenly, some players may receive one more card than others.

"""