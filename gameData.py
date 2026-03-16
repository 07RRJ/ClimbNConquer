from time import time
from dataclasses import dataclass, field

@dataclass
class GameData:
    startTime: float = time()
    floor: int = 1
    part: int = 1
    totalTurns: int = 0
    turn: int = 0
    endless: bool = False
    enemiesKilled: dict[str, int] = field(default_factory=lambda: {
        "Slime": 0, "Rat": 0, "Boar": 0, "Goblin": 0, "Zombie": 0,
        "King Slime": 0, "Rat King": 0, "Royal Boar": 0, "Goblin General": 0, "Lich": 0
    })

class KeyBinds:
    quit = "esc"
    attack = "1"
    heal = "2"
    block = "3"
    rest = "4"
    aoe = "5"
    regen = "6"
    fortress = "7"
    meditate = "8"
    nuke = "9"