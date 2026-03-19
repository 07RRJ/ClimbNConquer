# from gameFuncs import Attack
from dataclasses import dataclass, field
# import pygame
# import uiElements

@dataclass
class Player:
    MAX_HP: int = 20
    HP: int = MAX_HP
    HEAL: int = 3
    REGEN: int = 3
    ACTIVE_REGEN: int = 0

    DEF: int = 0
    BLOCK: int = 3

    STR: int = 1
    AOE: int = 0
    MULTI_ATTACK: int = 0

    BASE_STAMINA: float = 1
    STAMINA: float = BASE_STAMINA
    STAMINA_REGEN: float = 1
    MAX_STAMINA: int = 5

    MAX_MANA: int = 5
    MANA: float = 0

    EXP: int = 0
    NEXT_LVL: int = 5
    LVL: int = 0
    # ABILITIES: list [str] = field(default_factory=lambda: [["ATTACK", 1, True], ["AOE", 3, "King Slime"], ["MULTI SLAM", 5, "Rat King"], ["HEAL", 1, True], ["BLOCK", 1, True], ["REST", 0, True]])

    def listStats(self):
        stats = [
            f"HP: ({self.HP}/{self.MAX_HP})",
            f", DEF ({self.DEF}/{self.BLOCK})",
            f", STAMINA({self.STAMINA}/{self.MAX_STAMINA})",
            f", LVL ({self.LVL})",
            f", EXP ({self.EXP}/{self.NEXT_LVL})",
            "\n",
            f"STR: ({self.STR})",
            f", HEAL ({self.HEAL})",
            f", BLOCK ({self.BLOCK})",
            f", REST ({self.STAMINA_REGEN})"
        ]

    def Attack(self, gameData, enemies, idx):
        enemy = enemies.current[idx]
        enemy.DEF -= self.STR
        if enemy.DEF < 0:
            enemy.HP += enemy.DEF
            enemy.DEF = 0
        enemies.killed(self, gameData)

    def Heal(self):
        self.HP += self.HEAL
        if self.HP > self.MAX_HP:
            self.HP = self.MAX_HP

    def Block(self):
        self.DEF += self.BLOCK

    def Rest(self):
        self.STAMINA += self.STAMINA_REGEN
        if self.STAMINA > self.MAX_STAMINA:
            self.STAMINA = self.MAX_STAMINA

    def Regen(self):
        self.ACTIVE_REGEN += self.REGEN

    def Fortress(self):
        self.DEF += self.BLOCK

    def Meditate(self):
        pass

    def StartOfTurn(self):
        pass