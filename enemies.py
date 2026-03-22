import pygame
import random as rng
from gameFuncs import Attack, ResourcePath
from dataclasses import dataclass, field
import uiElements
from uiData import Colours as CO
from uiData import Data

@dataclass
class Enemies:
    current: list = field(default_factory=lambda: [])
    possible: list = field(default_factory=lambda: ["Slime"])
    amountEnemies: list = field(default_factory=lambda: [2, 2, 1, 1])
    enemyTypes: list = field(default_factory=lambda: ["Slime", "Rat", "Boar", "Goblin", "Zombie"])

    def GetEnemyStats(self):
        pass

    def generate(self, gameData):
        xEnemies = rng.choice(self.amountEnemies)
        generatedEnemies = []
        for i in range(xEnemies):
            enemy = rng.choice(self.possible)
            if enemy == "Slime":
                enemy = Slime(gameData)
            elif enemy == "Rat":
                enemy = Rat(gameData)
            elif enemy == "Boar":
                enemy = Boar(gameData)
            elif enemy == "Goblin":
                enemy = Goblin(gameData)
            elif enemy == "Zombie":
                enemy = Zombie(gameData)
            generatedEnemies.append(enemy)
        self.current = generatedEnemies

    def generateBoss(self, gameData):
        if gameData.floor % 5 == 1:
            kingSlime = KingSlime(gameData)
            self.current = [kingSlime]
        elif gameData.floor % 5 == 2:
            ratKing = RatKing(gameData)
            self.current = [ratKing]
        elif gameData.floor % 5 == 3:
            royalBoar = RoyalBoar(gameData)
            self.current = [royalBoar]
        elif gameData.floor % 5 == 4:
            goblinGeneral = GoblinGeneral(gameData)
            self.current = [goblinGeneral]
        elif gameData.floor % 5 == 0:
            lich = Lich(gameData)
            self.current = [lich]

    def killed(self, player, gameData):
        for i in range(len(self.current)):
            for idx, enemy in enumerate(self.current):
                if enemy.HP <= 0:
                    player.EXP += enemy.EXP
                    gameData.enemiesKilled[enemy.TYPE] += 1
                    self.current.pop(idx)

    def difficultyUp(self, gameData):
        if self.amountEnemies[2] < 9:
            self.amountEnemies[0] = self.amountEnemies[1]
            self.amountEnemies[1] = self.amountEnemies[2]
            self.amountEnemies[2] += 1
        self.possible.append(self.enemyTypes[(gameData.floor) % len(self.enemyTypes)])

    def Draw(self, screen, idx, xy, selected):
        x, y = xy
        enemy = self.current[idx]
        enemy.rect = pygame.Rect(x, y, 200, 200)
        if selected:
            screen.blit(enemy.SELECTED_IMG, (x, y+20))
        else:
            screen.blit(enemy.IMG, (x, y+20))

        uiElements.Bar(CO.BLACK[1], x, y+220, 200, 24, None).draw(screen)
        uiElements.Bar(CO.GREEN[3], x+2, y+222, 196, 20, (enemy, "HP", "MAX_HP")).draw(screen)

        if enemy.MOVE == "PASS":
            displayIntent =  Data.text_font.render("Passing", True, (CO.BLACK[5]))
        elif enemy.MOVE == "ATTACK":
            displayIntent =  Data.text_font.render(f"Attacking: ({enemy.STR})", True, (CO.RED[2]))
        elif enemy.MOVE == "BLOCK":
            displayIntent =  Data.text_font.render(f"Block: ({enemy.BLOCK})", True, (CO.BLUE[2]))
        elif enemy.MOVE == "HEAL":
            displayIntent =  Data.text_font.render(f"Heal: ({enemy.HEAL})", True, (CO.GREEN[2]))
        elif enemy.MOVE == "SUMMON":
            displayIntent =  Data.text_font.render(f"Summoning", True, (CO.BLACK[5]))

        displayDef =  Data.text_font.render(f"{enemy.DEF}", True, (CO.BLUE[2]))
        screen.blit(displayDef, (x, y + 250))
        screen.blit(displayIntent, (x, y))

# ======================================
# SECTION: ENEMIES
# ======================================

class Slime:
    TYPE = "Slime"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 1 + int(2 * multi)
        
        self.MAX_HP = 4 + int(3 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1

        self.DEF = 0
        self.BLOCK = 1

        self.STR = 1 + int(1 * multi)
        self.ABILITIES = ["ATTACK", "PASS"]
        self.MOVE = rng.choice(self.ABILITIES)

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/slime.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/slime_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None

    def Move(self, player, enemies, gameData):
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        self.MOVE = rng.choice(self.ABILITIES)

class Rat:
    TYPE = "Rat"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 2 + int(3 * multi)
        
        self.MAX_HP = 3 + int(3 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1
        
        self.DEF = 0
        self.BLOCK = 1

        self.STR = 2 + int(multi)
        self.ABILITIES = ["ATTACK"]
        self.MOVE = rng.choice(self.ABILITIES)

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/rat.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/rat_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None

    def Move(self, player, enemies, gameData):
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        self.MOVE = rng.choice(self.ABILITIES)

class Boar:
    TYPE = "Boar"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 2 + int(2 * multi)
        
        self.MAX_HP = 5 + int(5 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1

        self.DEF = 0
        self.BLOCK = 2 + int(2 * multi)

        self.STR = int(1.5 + 1.5 * multi)
        self.ABILITIES = ["PASS", "BLOCK", "ATTACK"]
        self.MOVE = rng.choice(self.ABILITIES)

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/boar.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/boar_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None

    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        elif self.MOVE == "BLOCK":
            self.DEF += self.BLOCK
        self.MOVE = rng.choice(self.ABILITIES)

class Goblin:
    TYPE = "Goblin"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 3 + int(3 * multi)
        
        self.MAX_HP = 10 + int(10 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1

        self.DEF = 0
        self.BLOCK = int(5 * multi)
    
        self.STR = 1 + int(1 * multi)
        self.ABILITIES = ["PASS", "BLOCK", "ATTACK"]
        self.MOVE = rng.choice(self.ABILITIES)

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/goblin.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/goblin_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None

    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        elif self.MOVE == "BLOCK":
            for enemy in enemies.current:
                if enemy.TYPE == "GOBLIN":
                    self.DEF += self.BLOCK
        self.MOVE = rng.choice(self.ABILITIES)

class Zombie:
    TYPE = "Zombie"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 4 + int(4 * multi)

        self.MAX_HP = 15 + int(15 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1
        
        self.DEF = 0
        self.BLOCK = 1

        self.STR = 2 + int(2 * multi)
        self.ABILITIES = ["PASS", "ATTACK"]
        self.MOVE = rng.choice(self.ABILITIES)

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/zombie.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/zombie_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None
    
    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "ATTACK":
            amountOfZombies = 0
            for enemy in enemies.current:
                if enemy.TYPE == "ZOMBIE":
                    amountOfZombies += 1
            Attack(self.STR + amountOfZombies, player)
        self.MOVE = rng.choice(self.ABILITIES)

# ======================================
# SECTION: BOSSES
# ======================================

class KingSlime:
    TYPE = "King Slime"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP =  20 + int(20 * multi)
        
        self.MAX_HP = 25 + int(50 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1

        self.DEF = 0
        self.BLOCK = 5 + int(10 * multi)
        
        self.STR = 1
        self.ABILITIES = ["SUMMON", "BLOCK", "PASS", "PASS"]
        self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/king_slime.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/king_slime_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None
    
    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "BLOCK":
            self.DEF += self.BLOCK
        if self.MOVE == "SUMMON":
            slime = Slime(gameData, True)
            enemies.current.append(slime)
        self.MOVE_IDX += 1
        if self.MOVE_IDX > len(self.ABILITIES) - 1:
            self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

class RatKing:
    TYPE = "Rat King"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 20 + int(20 * multi)
        
        self.MAX_HP = max(50, int(50 * multi))
        self.HP = self.MAX_HP
        self.HEAL = 1
        
        self.DEF = 0
        self.BLOCK = 1

        self.STR = 5 + int(5 * multi)
        self.ABILITIES = ["ATTACK", "ATTACK", "PASS"]
        self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/rat_king.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/rat_king_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None
    
    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        self.MOVE_IDX += 1
        if self.MOVE_IDX > len(self.ABILITIES) - 1:
            self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

class RoyalBoar:
    TYPE = "Royal Boar"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 20 + int(20 * multi)
        
        self.MAX_HP = 50 + int(50 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1
        
        self.DEF = 0
        self.BLOCK = 10 + int(10 * multi)
        
        self.STR = 2 + int(4 * multi)
        self.ABILITIES = ["PASS", "BLOCK", "ATTACK", "ATTACK"]
        self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/royal_boar.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/royal_boar_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None
    
    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        if self.MOVE == "BLOCK":
            self.DEF += self.BLOCK
        self.MOVE_IDX += 1
        if self.MOVE_IDX > len(self.ABILITIES) - 1:
            self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

class GoblinGeneral:
    TYPE = "Goblin General"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 20 + int(20 * multi)
        
        self.MAX_HP = 50 + int(50 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1
        
        self.DEF = 0
        self.BLOCK = 1
        
        self.STR = 5 + int(5 * multi)
        self.ABILITIES = ["ATTACK", "ATTACK", "PASS"]
        self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/goblin_general.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/goblin_general_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None
    
    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        self.MOVE_IDX += 1
        if self.MOVE_IDX > len(self.ABILITIES) - 1:
            self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

class Lich:
    TYPE = "Lich"
    def __init__(self, gameData, summoned = False):
        multi = gameData.floor / 2
        if summoned:
            self.EXP = 0
        else:
            self.EXP = 20 + int(20 * multi)
        
        self.MAX_HP = 50 + int(50 * multi)
        self.HP = self.MAX_HP
        self.HEAL = 1
        
        self.DEF = 0
        self.BLOCK = 1
        
        self.STR = 5 + int(5 * multi)
        self.ABILITIES = ["ATTACK", "ATTACK", "PASS", "PASS", "PASS", "SUMMON"]
        self.MOVE_IDX = 0
        self.MOVE = self.ABILITIES[self.MOVE_IDX]

        self.IMG = pygame.image.load(ResourcePath("assets/img/enemies/lich.png")).convert_alpha()
        self.IMG = pygame.transform.scale(self.IMG, (200, 200))
        self.SELECTED_IMG = pygame.image.load(ResourcePath("assets/img/enemies/lich_selected.png")).convert_alpha()
        self.SELECTED_IMG = pygame.transform.scale(self.SELECTED_IMG, (200, 200))
        self.rect = None
    
    def Move(self, player, enemies, gameData):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        if self.MOVE == "ATTACK":
            Attack(self.STR, player)
        self.MOVE_IDX += 1
        if self.MOVE_IDX > len(self.ABILITIES) - 1:
            self.MOVE_IDX = 0
        if self.MOVE == "SUMMON":
            idx = rng.randint(1, 4)
            if idx == 1:
                boss = KingSlime(gameData, True)
            elif idx == 1:
                boss = RatKing(gameData, True)
            enemies.current.append(boss)
        self.MOVE = self.ABILITIES[self.MOVE_IDX]