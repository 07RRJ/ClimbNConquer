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
        self.floor = 1
        self.part = 1
        self.turn = 0

class Player:
    def __init__(self):
        self.MAX_HP = 20
        self.HP = 20
        self.STR = 1
        self.AOE = 1
        self.MULTI_ATTACK = 5
        self.HEAL = 1
        self.DEF = 0
        self.BLOCK = 3
        self.BASE_STAMINA = 1
        self.STAMINA_REGEN = 1
        self.MAX_STAMINA = 5
        self.STAMINA = 0
        self.MAX_MANA = 5
        self.MANA = 0
        self.EXP = 0
        self.NEXT_LVL = 5
        self.LVL = 0
        self.ABILITIES = [["ATTACK", 1], ["AOE", 3], ["MULTI SLAM", 5], ["HEAL", 1], ["BLOCK", 1], ["REST", 0]]

    def listStats(self):
        stats = [
            "Player:",
            "\n" 
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
        print("".join(stats))

    def Move(self):
        player.DEF -= player.DEF // 2 + 1
        if player.DEF < 0:
            player.DEF = 0
        self.listStats()
        possibleMoves = []
        moveIdx = 1
        for move in self.ABILITIES:
            if move[1] <= self.STAMINA:
                possibleMoves.append(move)
                print(f"{moveIdx}: {move[0]}")
                moveIdx += 1
        move = possibleMoves[Limit("your move: ", 0, len(possibleMoves) + 1) - 1]
        print(f"you chose: {move[0]}")
        if move[0] == "ATTACK":
            self.STAMINA -= move[1]
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            Attack(self.STR, enemies.current[enemyToAttack])
            enemies.killed()
        elif move[0] == "AOE":
            self.STAMINA -= move[1]
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            listToAttack = [[enemyToAttack, 1]]
            for i in range(self.AOE):
                i += 1
                listToAttack.append([enemyToAttack + i, (i + 1) / 1.5])
                listToAttack.append([enemyToAttack - i, (i + 1) / 1.5])
            for attack in listToAttack:
                if attack[0] >= 0:
                    if attack[0] <= len(enemies.current):
                        try:
                            Attack(self.STR // attack[1], enemies.current[attack[0]])
                        except:
                            pass
            enemies.killed()
        elif move[0] == "MULTI ATTACK":
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            for attack in range(self.MULTI_ATTACK):
                Attack((self.STR // 2 + self.MULTI_ATTACK))
        elif move[0] == "HEAL":
            self.STAMINA -= move[1]
            if self.HP != self.MAX_HP and self.HP + self.HEAL < self.MAX_HP:
                self.HP += self.HEAL
            else:
                self.HP = self.MAX_HP
        elif move[0] == "BLOCK":
            self.STAMINA -= move[1]
            self.DEF += self.BLOCK
        elif move[0] == "REST":
            self.STAMINA -= move[1]
            self.STAMINA += self.STAMINA_REGEN
        self.STAMINA += 1
        if self.STAMINA > self.MAX_STAMINA:
            self.STAMINA = self.MAX_STAMINA

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
    
    def killed(self):
        for i in range(len(self.current)):
            for idx, enemy in enumerate(self.current):
                if enemy.HP <= 0:
                    player.ExpUp(enemy.EXP)
                    self.current.pop(idx)
    
    def difficultyUp(self):
        self.amountEnemies[0] = self.amountEnemies[1]
        self.amountEnemies[1] = self.amountEnemies[2]
        self.amountEnemies[2] += 1
        self.possible.append(enemyTypes[(gameData.floor) % len(enemyTypes)])

class Slime:
    TYPE = "Slime"
    def __init__(self, summoned = False):
        multi = gameData.floor
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 1 * multi
        self.MAX_HP = 5 * multi
        self.HP = 5 * multi
        self.STR = 1 * multi
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
        multi = gameData.floor
        self.EXP = 2 * multi
        self.MAX_HP = 5 * multi
        self.HP = 5 * multi
        self.STR = 2 * multi
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
        multi = gameData.floor
        self.EXP = 2 * multi
        self.MAX_HP = 10 * multi
        self.HP = 10 * multi
        self.STR = int(1.5 * multi)
        self.BLOCK = 5 * multi
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
        multi = gameData.floor
        self.EXP = 2 * multi
        self.MAX_HP = 10 * multi
        self.HP = 10 * multi
        self.STR = int(1.5 * multi)
        self.BLOCK = 5 * multi
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
        multi = gameData.floor
        self.EXP = 2 * multi
        self.MAX_HP = 10 * multi
        self.HP = 10 * multi
        self.STR = int(1.5 * multi)
        self.BLOCK = 5 * multi
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

# ======================================
# SECTION: BOSSES
# ======================================

class KingSlime:
    TYPE = "King Slime"
    def __init__(self):
        multi = gameData.floor
        self.MAX_HP = 50 * multi
        self.HP = 50 * multi
        self.BLOCK = 10 * multi
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
        multi = gameData.floor
        self.MAX_HP = 50 * multi
        self.HP = 50 * multi
        self.STR = 10 * multi
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
        multi = gameData.floor
        self.MAX_HP = 50 * multi
        self.HP = 50 * multi
        self.BLOCK = 10 * multi
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
        multi = gameData.floor
        self.MAX_HP = 50 * multi
        self.HP = 50 * multi
        self.BLOCK = 10 * multi
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
        multi = gameData.floor
        self.MAX_HP = 50 * multi
        self.HP = 50 * multi
        self.BLOCK = 10 * multi
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
    player.STAMINA = player.BASE_STAMINA
    while True:
        if enemies.current and player.HP > 0:
            gameData.turn += 1
            if gameData.part != 10:
                print(f"Floor {gameData.floor}-{gameData.part}, Turn: ({gameData.turn})")
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
        if gameData.floor < 6:
            enemies.generate()
            result = playFloor()
            if result == "won":
                if gameData.part == 5:
                    enemies.difficultyUp()
                if gameData.part < 10:
                    gameData.part += 1
                else:
                    gameData.part += 1
                    if gameData.floor % 5 == 1:
                        kingSlime = KingSlime()
                        enemies.current = [kingSlime]
                    elif gameData.floor % 5 == 2:
                        ratKing = RatKing()
                        enemies.current = [ratKing]
                    elif gameData.floor % 5 == 3:
                        royalBoar = RoyalBoar()
                        enemies.current = [royalBoar]
                    elif gameData.floor % 5 == 4:
                        goblinGeneral = GoblinGeneral()
                        enemies.current = [goblinGeneral]
                    elif gameData.floor % 5 == 0:
                        lich = Lich()
                        enemies.current = [lich]
                    result = playFloor()
                    if result == "won":
                        gameData.part += 1
                    else:
                        return "dead"
                    gameData.part = 1
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
        print(f"you died, floor: ({gameData.floor}-{gameData.part})")
    print("play again (y/n):")
    while getwch().lower() != "y":
        pass