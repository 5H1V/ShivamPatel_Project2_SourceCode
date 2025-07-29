
def move_player(board, player_state, new_position):
    y,x = new_position
    if 0 <=y <25 and 0 <=x<25 and board[y,x] != -1:
        player_state.move((x,y))
        return True
    return False

def make_suggestion(player,suspect,weapon,room):
    return {"suspect": suspect, "weapon": weapon,"room":room}

def check_accusation(solution, accusation):
    return solution==accusation

