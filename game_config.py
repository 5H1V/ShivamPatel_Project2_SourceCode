import numpy as np

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

board_labels = {"Invalid": -1,
                "Empty" : 0,
                "Occupied" : 1,
                "Ballroom" : 2,
                "BillardRoom" : 3,
                "Conservatory" : 4,
                "DiningRoom" : 5,
                "Hall" : 6,
                "Kitchen" : 7,
                "Library" : 8,
                "Lounge" : 9,
                "Study" : 10,
                "Center" : 11,
                "Door" : 12,
                "Secret" : 13}

rooms = {
    "Lounge": [(0,25),(6,25),(6,24),(7,24),(7,19),(0,19)],
    "Hall": [(9,25),(15,25),(15,18),(9,18)],
    "Study": [(18,25),(24,25),(24,21),(17,21),(17,24),(18,24)],
    "DiningRoom": [(0,16),(8,16),(8,10),(5,10),(5,9),(0,9)],
    "Library": [(18,19),(23,19),(23,18),(24,18),(24,15),(23,15),(23,14),(18,14),(18,15),(17,15),(17,18),(18,18)],
    "BillardRoom": [(18,13),(24,13),(24,8),(18,8)],
    "Kitchen": [(1,7),(6,7),(6,1),(0,1),(0,6),(1,6)],
    "Ballroom": [(8,8),(16,8),(16,2),(14,2),(14,0),(10,0),(10,2),(8,2)],
    "Conservatory": [(19,6),(23,6),(23,5),(24,5),(24,1),(18,1),(18,5),(19,5)],
    "Center": [(10,17),(15,17),(15,10),(10,10)],
}

doors = [(6,19),(11,18),(12,18),(14,20),(17,21),(17,16),
        (20,14),(6,15),(7,12),(22,12),(18,9),(4,6),
        (8,5),(9,7),(14,7),(15,5),(18,4)]

secret = [(4,5),(18,3),(17,22),(6,20)]

starting_positions = [(9,0),(14,0),(23,6),(23,19),(7,24),(0,17)]

game_walls = {0:[0,1,2,3,4,5,6,7,8,15,16,17,18,19,20,21,22,23],
              1:[6,17], 5:[23], 6:[0], 7:[23], 8:[0], 13:[23],
              14:[23], 16:[0], 18:[0,23], 20:[23], 24:[6,8,15,17]}

# Solution = room, player, weapon
solution = [np.random.randint(2,11), np.random.randint(11,17), np.random.randint(17,23)]
