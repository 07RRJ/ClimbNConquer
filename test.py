import os, sys
import random as rng
from msvcrt import getwch
from time import sleep

# ======================================
# SECTION: BASE
# ======================================

def cls():
    os.system("cls")

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

class GameData:
    def __init__(self):
        self.floor = 0
        self.visualF = 1
        self.part = 0
        self.visualP = 1
        self.turn = 0

class Player:
    def __init__(self):
        self.MAX_HP = 20
        self.HP = 20
        self.STR = 1
        self.AOE = 1
        self.HEAL = 1
        self.DEF = 0
        self.BLOCK = 3
        self.STAMINA = 0
        self.EXP = 0
        self.NEXT_LVL = 5
        self.LVL = 0
        self.ABILITIES = ["ATTACK", "AOE", "HEAL", "BLOCK"]

    def Move(self):
        player.DEF -= player.DEF // 2 + 1
        if player.DEF < 0:
            player.DEF = 0
        print(f"Player:\nHP: ({self.HP}/{self.MAX_HP}), DEF ({self.DEF}/{self.BLOCK}), STR: ({self.STR}), HEAL ({self.HEAL}), LVL ({self.LVL}), EXP ({self.EXP}/{self.NEXT_LVL})")
        for idx, move in enumerate(self.ABILITIES, 1):
            print(idx, move)
        move = self.ABILITIES[Limit("your move: ", 0, len(self.ABILITIES) + 1) - 1]
        print(f"you chose: {move}")
        if move == "ATTACK":
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            Attack(self.STR, enemies.current[enemyToAttack])
            if enemies.current[enemyToAttack].HP <= 0:
                player.ExpUp(enemies.current[enemyToAttack].EXP)
                enemies.current.pop(enemyToAttack)
        elif move == "AOE":
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            Attack(self.STR, enemies.current[enemyToAttack])
            for i in range(self.AOE):
                i += 1
                try:
                    Attack(self.STR // i, enemies.current[enemyToAttack - i])
                except:
                    pass
                try:
                    Attack(self.STR // i, enemies.current[enemyToAttack + i])
                except:
                    pass
                for idx, enemy in enumerate(enemies.current):
                    if enemy.HP <= 0:
                        player.ExpUp(enemy.EXP)
                        enemies.current.pop(idx)
        elif move == "HEAL":
            if self.HP != self.MAX_HP and self.HP + self.HEAL < self.MAX_HP:
                self.HP += self.HEAL
            else:
                self.HP = self.MAX_HP
        elif move == "BLOCK":
            self.DEF += self.BLOCK

    def ExpUp(self, exp):
        self.EXP += exp
        while self.EXP >= self.NEXT_LVL:
            self.EXP -= self.NEXT_LVL
            self.LVL += 1
            self.NEXT_LVL += self.LVL
            self.STR += 1
            self.MAX_HP += 1
            self.BLOCK += 1
            self.HEAL += 1

# ======================================
# SECTION: ENEMIES
# ======================================

enemyTypes = ["Slime", "Rat", "Boar", "Goblin", "Zombie"]

class Enemies:
    def __init__(self):
        self.current = []
        self.possible = ["Slime"]
        self.amountEnemies = [1, 1, 1]

    def generate(self):
        if not self.current:
            xEnemies = rng.choice(self.amountEnemies)
            generatedEnemies = []
            for i in range(xEnemies):
                enemy = rng.choice(self.possible)
                if enemy == "Slime":
                    enemy = Slime()
                elif enemy == "Rat":
                    enemy = Rat()
                elif enemy == "Boar":
                    enemy = Boar()
                elif enemy == "Goblin":
                    enemy = Goblin()
                elif enemy == "Zombie":
                    enemy = Zombie()
                generatedEnemies.append(enemy)
            self.current = generatedEnemies
    
    def difficultyUp(self):
        self.amountEnemies[0] = self.amountEnemies[1]
        self.amountEnemies[1] = self.amountEnemies[2]
        self.amountEnemies[2] += 1
        self.possible.append(enemyTypes[(gameData.floor + 1) % len(enemyTypes)])

class Slime:
    TYPE = "Slime"
    def __init__(self, summoned = False):
        floor = gameData.floor + 1
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 1 * floor
        self.MAX_HP = 5 * floor
        self.HP = 5 * floor
        self.STR = 1 * floor
    HEAL = 0
    DEF = 0
    BLOCK = 0
    ABILITIES = ["ATTACK", "PASS"]

    def Move(self):
        enemyMove = rng.choice(self.ABILITIES)
        if enemyMove == "ATTACK":
            Attack(self.STR, player)

class Rat:
    TYPE = "Rat"
    def __init__(self):
        floor = gameData.floor + 1
        self.EXP = 2 * floor
        self.MAX_HP = 5 * floor
        self.HP = 5 * floor
        self.STR = 2 * floor
    HEAL = 0
    DEF = 0
    BLOCK = 0
    ABILITIES = ["ATTACK"]
    
    def Move(self):
        enemyMove = rng.choice(self.ABILITIES)
        if enemyMove == "ATTACK":
            Attack(self.STR, player)

class Boar:
    TYPE = "Boar"
    def __init__(self):
        floor = gameData.floor + 1
        self.EXP = 2 * floor
        self.MAX_HP = 10 * floor
        self.HP = 10 * floor
        self.STR = int(1.5 * floor)
        self.BLOCK = 5 * floor
    HEAL = 0
    DEF = 0
    ABILITIES = ["PASS", "BLOCK", "ATTACK"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = rng.choice(self.ABILITIES)
        if enemyMove == "ATTACK":
            Attack(self.STR, player)
        elif enemyMove == "BLOCK":
            self.DEF += self.BLOCK

class Goblin:
    TYPE = "Goblin"
    def __init__(self):
        floor = gameData.floor + 1
        self.EXP = 2 * floor
        self.MAX_HP = 10 * floor
        self.HP = 10 * floor
        self.STR = int(1.5 * floor)
        self.BLOCK = 5 * floor
    HEAL = 0
    DEF = 0
    ABILITIES = ["PASS", "BLOCK", "ATTACK"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = rng.choice(self.ABILITIES)
        if enemyMove == "ATTACK":
            Attack(self.STR, player)
        elif enemyMove == "BLOCK":
            self.DEF += self.BLOCK

class Zombie:
    TYPE = "Zombie"
    def __init__(self):
        floor = gameData.floor + 1
        self.EXP = 2 * floor
        self.MAX_HP = 10 * floor
        self.HP = 10 * floor
        self.STR = int(1.5 * floor)
        self.BLOCK = 5 * floor
    HEAL = 0
    DEF = 0
    ABILITIES = ["PASS", "BLOCK", "ATTACK"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = rng.choice(self.ABILITIES)
        if enemyMove == "ATTACK":
            Attack(self.STR, player)
        elif enemyMove == "BLOCK":
            self.DEF += self.BLOCK

# class Zombie:
#     TYPE = "Zombie"
#     def __init__(self):
#         floor = gameData.floor + 1
#         self.EXP = 2 * floor
#         self.MAX_HP = 10 * floor
#         self.HP = 10 * floor
#         self.STR = int(1.5 * floor)
#         self.BLOCK = 5 * floor
#     HEAL = 0
#     DEF = 0
#     ABILITIES = ["PASS", "BLOCK", "ATTACK"]
    
#     def Move(self):
#         self.DEF -= self.DEF // 2 + 1
#         if self.DEF < 0:
#             self.DEF = 0
#         enemyMove = rng.choice(self.ABILITIES)
#         if enemyMove == "ATTACK":
#             Attack(self.STR, player)
#         elif enemyMove == "BLOCK":
#             self.DEF += self.BLOCK

# ======================================
# SECTION: BOSSES
# ======================================

class KingSlime:
    TYPE = "King Slime"
    def __init__(self):
        floor = gameData.floor + 1
        self.MAX_HP = 50 * floor
        self.HP = 50 * floor
        self.BLOCK = 10 * floor
    STR = 0
    EXP =  0
    MOVE = 0
    HEAL = 0
    DEF = 0
    ABILITIES = ["SUMMON", "BLOCK", "PASS"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = self.ABILITIES[self.MOVE]
        if enemyMove == "BLOCK":
            self.DEF += self.BLOCK
        if enemyMove == "SUMMON":
            slime = Slime(True)
            enemies.current.append(slime)
        self.MOVE += 1
        if self.MOVE > len(self.ABILITIES) - 1:
            self.MOVE = 0

class RatKing:
    TYPE = "Rat King"
    def __init__(self):
        floor = gameData.floor + 1
        self.MAX_HP = 50 * floor
        self.HP = 50 * floor
        self.STR = 10 * floor
    EXP =  0
    MOVE = 0
    HEAL = 0
    DEF = 0
    ABILITIES = ["ATTACK"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = self.ABILITIES[self.MOVE]
        if enemyMove == "ATTACK":
            Attack(self.STR, player)
        self.MOVE += 1
        if self.MOVE > len(self.ABILITIES) - 1:
            self.MOVE = 0

class RoyalBoar:
    TYPE = "Royal Boar"
    def __init__(self):
        floor = gameData.floor + 1
        self.MAX_HP = 50 * floor
        self.HP = 50 * floor
        self.BLOCK = 10 * floor
    STR = 0
    EXP =  0
    MOVE = 0
    HEAL = 0
    DEF = 0
    ABILITIES = ["BLOCK", "PASS", "CHARGE", "ATTACK", "ATTACK"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = self.ABILITIES[self.MOVE]
        if enemyMove == "BLOCK":
            self.DEF += self.BLOCK
        if enemyMove == "SUMMON":
            slime = Slime(True)
            enemies.current.append(slime)
        self.MOVE += 1
        if self.MOVE > len(self.ABILITIES) - 1:
            self.MOVE = 0

class GoblinGeneral:
    TYPE = "Goblin General"
    def __init__(self):
        floor = gameData.floor + 1
        self.MAX_HP = 50 * floor
        self.HP = 50 * floor
        self.BLOCK = 10 * floor
    STR = 0
    EXP =  0
    MOVE = 0
    HEAL = 0
    DEF = 0
    ABILITIES = ["SUMMON", "BLOCK", "PASS"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = self.ABILITIES[self.MOVE]
        if enemyMove == "BLOCK":
            self.DEF += self.BLOCK
        if enemyMove == "SUMMON":
            slime = Slime(True)
            enemies.current.append(slime)
        self.MOVE += 1
        if self.MOVE > len(self.ABILITIES) - 1:
            self.MOVE = 0

class Lich:
    TYPE = "Lich"
    def __init__(self):
        floor = gameData.floor + 1
        self.MAX_HP = 50 * floor
        self.HP = 50 * floor
        self.BLOCK = 10 * floor
    STR = 0
    EXP =  0
    MOVE = 0
    HEAL = 0
    DEF = 0
    ABILITIES = ["SUMMON", "BLOCK", "HEAL", "PASS"]
    
    def Move(self):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        enemyMove = self.ABILITIES[self.MOVE]
        if enemyMove == "BLOCK":
            self.DEF += self.BLOCK
        if enemyMove == "SUMMON":
            slime = Slime(True)
            enemies.current.append(slime)
        self.MOVE += 1
        if self.MOVE > len(self.ABILITIES) - 1:
            self.MOVE = 0

# ======================================
# SECTION: FUNCS
# ======================================

def Attack(STR, enemy):
    if STR >= enemy.DEF + enemy.HP:
        enemy.DEF = 0
        enemy.HP = 0
    elif enemy.DEF:
        enemy.DEF -= STR
        if enemy.DEF < 0:
            enemy.HP += enemy.DEF
            enemy.DEF = 0
    else:
        enemy.HP -= STR


def Limit(question, Min, Max):
    while True:
        try:
            print(question)
            value = int(getwch())
            if value > Min:
                if value < Max:
                    return value
        except:
            pass

def GetEnemyStats():
    stats = []
    for idx, enemy in enumerate(enemies.current):
        stats.append(f"({idx + 1}){enemy.TYPE}, HP: ({enemy.HP}/{enemy.MAX_HP}), DEF: ({enemy.DEF}/{enemy.BLOCK}), STR: {enemy.STR}")
    print("Enemies:")
    for enemy in stats:
        print(enemy)

# ======================================
# SECTION: THE GAME LOOP STUFF
# ======================================

def playFloor():
    player.DEF = 0
    gameData.turn = 0
    while True:
        if enemies.current and player.HP > 0:
            gameData.turn += 1
            if gameData.part != 10:
                print(f"Floor {gameData.floor + 1}-{gameData.part + 1}, Turn: ({gameData.turn})")
            else:
                print(f"Boss battle, Turn: ({gameData.turn})")
            GetEnemyStats()
            player.Move()

            for enemy in enemies.current:
                # sleep(1)
                enemy.Move()

            cls()
        if not enemies.current:
            return "won"
        elif player.HP <= 0:
            return "dead"

runing = True

def play():
    result = ""
    while result != "dead":
        if gameData.floor < 5:
            enemies.generate()
            result = playFloor()
            if result == "won":
                if gameData.part == 4:
                    enemies.difficultyUp()
                if gameData.part < 9:
                    gameData.part += 1
                else:
                    gameData.part += 1
                    if gameData.floor % 5 == 0:
                        kingSlime = KingSlime()
                        enemies.current = [kingSlime]
                    elif gameData.floor % 5 == 1:
                        ratKing = RatKing()
                        enemies.current = [ratKing]
                    elif gameData.floor % 5 == 2:
                        royalBoar = RoyalBoar()
                        enemies.current = [royalBoar]
                    elif gameData.floor % 5 == 3:
                        goblinGeneral = GoblinGeneral()
                        enemies.current = [goblinGeneral]
                    elif gameData.floor % 5 == 4:
                        lich = Lich()
                        enemies.current = [lich]
                    result = playFloor()
                    if result == "won":
                        gameData.part += 1
                    else:
                        return "dead"
                    gameData.part = 0
                    gameData.floor += 1
            elif result == "dead":
                return "dead"
        else:
            return "won"

while True:
    cls()
    player = Player()
    enemies = Enemies()
    gameData = GameData()
    result = play()
    if result == "won":
        print("you won")
    else:
        print(f"you died, floor: ({gameData.floor + 1}-{gameData.part + 1})")
    print("play again (y/n):")
    while getwch().lower() != "y":
        pass