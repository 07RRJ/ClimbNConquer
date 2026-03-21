from gameFuncs import Attack
from dataclasses import dataclass, field
import uiElements
# import pygame
# import uiElements
import random as rng

@dataclass
class Player:
    MAX_HP: int = 20
    HP: int = MAX_HP
    HEAL: int = 3
    REGEN: int = 3
    ACTIVE_REGEN: int = 0

    DEF: int = 0
    BLOCK: int = 3
    FORTRESS: int = 0

    STR: int = 1
    AOE: int = 0
    NUKE: int = 0

    BASE_STAMINA: float = 1
    STAMINA: int = BASE_STAMINA
    STAMINA_REGEN: float = 1
    MAX_STAMINA: int = 5
    MEDITATE: int = 0

    MAX_MANA: int = 5
    MANA: float = 0

    EXP: int = 0
    NEXT_LVL: int = 5
    LVL: int = 0

    # def listStats(self):
    #     stats = [
    #         f"HP: ({self.HP}/{self.MAX_HP})",
    #         f", DEF ({self.DEF}/{self.BLOCK})",
    #         f", STAMINA({self.STAMINA}/{self.MAX_STAMINA})",
    #         f", LVL ({self.LVL})",
    #         f", EXP ({self.EXP}/{self.NEXT_LVL})",
    #         "\n",
    #         f"STR: ({self.STR})",
    #         f", HEAL ({self.HEAL})",
    #         f", BLOCK ({self.BLOCK})",
    #         f", REST ({self.STAMINA_REGEN})"
    #     ]

    def Attack(self, gameData, enemies, selectedEnemyIdx, enemyPos):
        x, y = enemyPos[selectedEnemyIdx][0] + rng.randint(50, 150), enemyPos[selectedEnemyIdx][1] + rng.randint(50, 150)
        self.STAMINA -= 1
        try:
            Attack(self.STR, enemies.current[selectedEnemyIdx])
            theAttack = uiElements.DamageText(f"-{self.STR}", (x, y))
            enemies.killed(self, gameData)
            return False, theAttack
        except Exception as e:
            print(e)
            return True, theAttack
    
    def Aoe(self, gameData, enemies, selectedEnemyIdx, enemyPos):
        theAttacks = []
        try:
            x, y = enemyPos[selectedEnemyIdx][0] + rng.randint(50, 150), enemyPos[selectedEnemyIdx][1] + rng.randint(50, 150)
            listToAttack = [[selectedEnemyIdx, 1, (x, y)]]
            for i in range(self.AOE):
                i += 1
                x, y = enemyPos[selectedEnemyIdx + i][0] + rng.randint(50, 150), enemyPos[selectedEnemyIdx + i][1] + rng.randint(50, 150)
                listToAttack.append([selectedEnemyIdx + i, (i + 1) / 1.5, (x, y)])
                x, y = enemyPos[selectedEnemyIdx - i][0] + rng.randint(50, 150), enemyPos[selectedEnemyIdx - i][1] + rng.randint(50, 150)
                listToAttack.append([selectedEnemyIdx - i, (i + 1) / 1.5, (x, y)])
            for attack in listToAttack:
                if attack[0] >= 0:
                    if attack[0] <= len(enemies.current):
                        try:
                            Attack(int(self.STR / attack[1]), enemies.current[attack[0]])
                            theAttacks.append(uiElements.DamageText(f"-{int(self.STR / attack[1])}", attack[2]))
                        except:
                            pass
            enemies.killed(self, gameData)
            return False, theAttacks
        except Exception as e:
            print(e)
            return True, None

    def Nuke(self, gameData, enemies, selectedEnemyIdx, enemyPos):
        x, y = enemyPos[selectedEnemyIdx]
        self.STAMINA -= 1
        theAttacks = []
        try:
            for attack in range(self.NUKE):
                dmg = max(int(self.STR // 2 * (attack + 2)), 1)
                Attack(dmg, enemies.current[selectedEnemyIdx])
                theAttacks.append(uiElements.DamageText(f"-{dmg}", (x+rng.randint(50, 150), y+rng.randint(50, 150))))
            enemies.killed(self, gameData)
            return False, theAttacks
        except Exception as e:
            print(e)
            return True, theAttacks

    def Heal(self):
        self.STAMINA -= 1
        self.HP += self.HEAL
        if self.HP > self.MAX_HP:
            self.HP = self.MAX_HP

    def Regen(self):
        self.STAMINA -= 3
        self.ACTIVE_REGEN += self.REGEN

    def Block(self):
        self.STAMINA -= 1
        self.DEF += self.BLOCK

    def Fortress(self):
        self.STAMINA -= 3
        self.DEF += self.DEF * self.FORTRESS

    def Rest(self):
        self.STAMINA += self.STAMINA_REGEN
        if self.STAMINA > self.MAX_STAMINA:
            self.STAMINA = self.MAX_STAMINA

    def Meditate(self):
        self.HP -= self.MEDITATE
        self.STAMINA += self.STAMINA_REGEN + self.MEDITATE

    def StartOfTurn(self):
        self.STAMINA += self.STAMINA_REGEN
        if self.STAMINA >= self.MAX_STAMINA:
            self.STAMINA = self.MAX_STAMINA
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0