from gameFuncs import Attack
from dataclasses import dataclass, field
from uiElements import Button, Bar, DamageText
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
    FORTRESS: int = 0

    STR: int = 1
    AOE: int = 0
    MULTI_ATTACK: int = 0

    BASE_STAMINA: float = 1
    STAMINA: int = BASE_STAMINA
    STAMINA_REGEN: float = 1
    MAX_STAMINA: int = 5

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

    def Attack(self, gameData, enemies, selectedEnemyIdx, pos):
        self.STAMINA -= 1
        playerTurn = True
        theAttack = False
        try:
            Attack(self.STR, enemies.current[selectedEnemyIdx])
            playerTurn = False
            theAttack = DamageText(f"-{self.STR}", pos)
        except Exception as e:
            print(e)
        enemies.killed(self, gameData)
        return playerTurn, theAttack
    
    def Aoe(self, gameData, enemies, selectedEnemyIdx, enemyPos):
        
        theAttacks = []
        
        try:
            listToAttack = [[selectedEnemyIdx, 1]]
            for i in range(self.AOE):
                i += 1
                listToAttack.append([selectedEnemyIdx + i, (i + 1) / 1.5])
                listToAttack.append([selectedEnemyIdx - i, (i + 1) / 1.5])
            for attack in listToAttack:
                if attack[0] >= 0:
                    if attack[0] <= len(enemies.current):
                        try:
                            Attack(gameData, int(self.STR / attack[1]), enemies.current[attack[0]])
                            theAttacks.append(DamageText(f"-{int(self.STR / attack[1])}", pos))
                        except:
                            pass
            enemies.killed()
        except Exception as e:
            print(e)

    def Heal(self):
        self.STAMINA -= 1
        self.HP += self.HEAL
        if self.HP > self.MAX_HP:
            self.HP = self.MAX_HP

    def Block(self):
        self.STAMINA -= 1
        self.DEF += self.BLOCK

    def Rest(self):
        self.STAMINA += self.STAMINA_REGEN
        if self.STAMINA > self.MAX_STAMINA:
            self.STAMINA = self.MAX_STAMINA

    def Regen(self):
        self.STAMINA -= 3
        self.ACTIVE_REGEN += self.REGEN

    def Fortress(self):
        self.STAMINA -= 3
        self.DEF += self.DEF * self.FORTRESS

    def Meditate(self):
        self.HP -= self.Meditate
        self.STAMINA += 3

    def StartOfTurn(self):
        pass