from game_config import players, weapons, rooms, player_start_positions, get_all_cards

class Player:
    def __init__(self, name, card_hand):
        self.name = name
        self.index = [key for key, value in players.items() if value == name][0]
        self.starting_position = player_start_positions.get(name)
        self.card_hand = card_hand.get(name)
        self.current_position = player_start_positions.get(name)
        self.knowledge = get_all_cards()
        self.eliminated = False
        self.game_won = False
        self.winner = None
    

    def get_player_id_by_name(self, name):
        for pid, pname in players.items():
            if pname.lower() == name.lower():
                return pid
        return None

    def get_weapon_id_by_name(self, name):
        for wid, wname in weapons.items():
            if wname.lower() == name.lower():
                return wid
        return None

    def get_room_id_by_name(self, name):
        for rid, rname in rooms.items():
            if rname.lower() == name.lower():
                return rid
        return None

    def get_card_name(self, card_id):
        if card_id in rooms:
            return rooms[card_id]
        elif card_id in players:
            return players[card_id]
        elif card_id in weapons:
            return weapons[card_id]
        return f"Unknown card {card_id}"

    def get_player_hand_names(self, player):
        return [self.get_card_name(card) for card in self.card_hand]
