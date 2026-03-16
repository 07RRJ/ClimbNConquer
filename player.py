# from gameFuncs import Attack
from dataclasses import dataclass, field
import pygame, keyboard
from gameData import KeyBinds as KB
import uiElements

@dataclass
class Player:
    MAX_HP: int = 20
    HP: int = MAX_HP
    HEAL: int = 3

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

    # def Move(self, gameData, enemies):
    #     self.DEF -= self.DEF // 2 + 1
    #     if self.DEF < 0:
    #         self.DEF = 0
    #     self.listStats()
    #     possibleMoves = []
    #     moveIdx = 1
    #     for move in self.ABILITIES:
    #         if move[1] <= self.STAMINA:
    #             if move[2] == True or gameData.enemiesKilled[move[2]] != 0:
    #                 possibleMoves.append(move)
    #                 moveIdx += 1
    #     # move = possibleMoves[Limit("your move: ", 0, len(possibleMoves) + 1) - 1]
    #     if move[0] == "ATTACK":
    #         self.STAMINA -= move[1]
    #         # enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
    #         # Attack(self.STR, enemies.current[enemyToAttack])
    #         enemies.killed(self, gameData)
    #     elif move[0] == "AOE":
    #         self.STAMINA -= move[1]
    #         # enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
    #         # listToAttack = [[enemyToAttack, 1]]
    #         for i in range(self.AOE):
    #             i += 1
    #             # listToAttack.append([enemyToAttack + i, (i + 1) / 1.5])
    #             # listToAttack.append([enemyToAttack - i, (i + 1) / 1.5])
    #         # for attack in listToAttack:
    #         #     if attack[0] >= 0:
    #         #         if attack[0] <= len(enemies.current):
    #         #             try:
    #         #                 Attack(int(self.STR / attack[1]), enemies.current[attack[0]])
    #         #             except:
    #         #                 pass
    #         enemies.killed()
    #     elif move[0] == "MULTI SLAM":
    #         # enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
    #         for attack in range(self.MULTI_ATTACK):
    #             pass
    #             # Attack(max(int(self.STR // 2 * (attack + 2)), 1), enemies.current[enemyToAttack])
    #         enemies.killed()
    #     elif move[0] == "HEAL":
    #         self.STAMINA -= move[1]
    #         if self.HP != self.MAX_HP and self.HP + self.HEAL < self.MAX_HP:
    #             self.HP += self.HEAL
    #         else:
    #             self.HP = self.MAX_HP
    #     elif move[0] == "BLOCK":
    #         self.STAMINA -= move[1]
    #         self.DEF += self.BLOCK
    #     elif move[0] == "REST":
    #         self.STAMINA -= move[1]
    #         self.STAMINA += self.STAMINA_REGEN
    #     self.STAMINA += 1
    #     if self.STAMINA > self.MAX_STAMINA:
    #         self.STAMINA = self.MAX_STAMINA