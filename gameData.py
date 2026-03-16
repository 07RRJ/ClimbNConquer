from time import time
from dataclasses import dataclass, field
import pygame

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
    keyBinds = {
        "quit": (pygame.K_ESCAPE, "quit"),
        "attack": (pygame.K_1, 0),
        "heal": (pygame.K_2, 1),
        "block": (pygame.K_3, 2),
        "rest": (pygame.K_4, 3),
        "aoe": (pygame.K_5, 4),
        "regen": (pygame.K_6, 5),
        "fortress": (pygame.K_7, 6),
        "meditate": (pygame.K_8, 7),
        "nuke": (pygame.K_9, 8)
    }