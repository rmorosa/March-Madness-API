def get_bonus(bracketround, winner):   
    if bracketround == "elite eight" and winner:
        bonus = 3
    elif bracketround == "final four" and winner:
        bonus = 6
    elif bracketround == "championship" and winner:
        bonus = 9
    else:
        bonus = 0
    return bonus