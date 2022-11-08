

class Node:

    def __init__(self, cords, g, h):
        self.cords = cords
        self.g = g
        self.h = h
        self.f = self.g + self.h
        self.is_wall = False
        self.door = False
        self.key = False
        self.wired = False
        self.previous = None