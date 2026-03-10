from time import time

class GameData:
    def __init__(self):
        self.startTime = time()
        self.floor = 1
        self.part = 1
        self.totalTurns = 0
        self.turn = 0
        self.endless = ""
        self.enemiesKilled = {
            "Slime": 0, "Rat": 0, "Boar": 0, "Goblin": 0, "Zombie": 0,
            "King Slime": 0, "Rat King": 0, "Royal Boar": 0, "Goblin General": 0, "Lich": 0
        }