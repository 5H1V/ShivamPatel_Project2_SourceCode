class PlayerStates:

    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.cards = []
        self.notes = {}
    
    def move(self, new_position):
        self.position = new_position
    
    def receive_hand(self, card):
        self.cards.append(card)
    
    def update_notes(self,card,known_by):
        self.notes[card] = known_by
    
    def __repr__(self):
        return f"<Player {self.name}, Pos: {self.position}, Cards: {self.cards}>"