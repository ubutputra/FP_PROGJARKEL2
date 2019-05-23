import random
def dice():
    move = random.randrange(1, 7, 1)
    return move

def diceNotPrime():
    listMoves = [1,4,6]
    rand = random.randrange(0, 3, 1)
    move = listMoves[rand]
    return move

def dicePrime():
    listMoves = [2,3,5]
    rand = random.randrange(0, 3, 1)
    move = listMoves[rand]
    return move
