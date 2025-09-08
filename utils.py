import random

def randbool(probability, max_probability):
    return random.randint(0, max_probability) <= probability

def randcell(width, height):
    return (random.randint(0, height - 1), random.randint(0, width - 1))

def randcell2(x, y):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dx, dy = random.choice(moves)
    return (x + dx, y + dy)