import os, sys
import random as rng
from msvcrt import getwch
import time
from player import Player
from enemies import Enemies
from gameFuncs import cls, Attack, Limit, Comfirm, GetTime

# ======================================
# SECTION: BASE
# ======================================

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

class GameData:
    def __init__(self):
        self.startTime = time.time()
        self.floor = 1
        self.part = 1
        self.totalTurns = 0
        self.turn = 0
        self.enemiesKilled = {
            "Slime": 0, "Rat": 0, "Boar": 0, "Goblin": 0, "Zombie": 0,
            "King Slime": 0, "Rat King": 0, "Royal Boar": 0, "Goblin General": 0, "Lich": 0
        }

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
            if gameData.part != 0:
                print(f"Floor {gameData.floor}-{gameData.part}, Turn: ({gameData.turn})")
            else:
                print(f"Boss battle, Turn: ({gameData.turn})")
            enemies.GetEnemyStats()
            player.Move(gameData, enemies)

            for enemy in enemies.current:
                enemy.Move(player, enemies, gameData)

            cls()
        gameData.totalTurns += gameData.turn
        if not enemies.current:
            player.ExpUp()
            return "won"
        elif player.HP <= 0:
            return "dead"

runing = True

def play():
    endless = False
    while True:
        if endless or gameData.floor < 6:
            if gameData.part == 11:
                gameData.part = 0
                enemies.generateBoss(gameData)
                gameData.floor += 1
            elif not enemies.current:
                enemies.generate(gameData)
            result = playFloor()
            gameData.part += 1
            if result == "dead":
                return "dead"
            elif gameData.part == 5:
                enemies.difficultyUp(gameData)
        else:
            return "won"

runing = True

while runing:
    cls()
    player = Player()
    enemies = Enemies()
    gameData = GameData()
    result = play()
    if result == "won":
        print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
    else:
        print(f"you died, floor: ({gameData.floor}-{gameData.part}), total turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
        print("=" * 22)
        for enemy in gameData.enemiesKilled:
            print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
        print("=" * 22)
    print("play again (y/n):")
    while True: 
        if getwch().lower() == "y":
            break
        elif getwch().lower() == "n":
            runing = False
            break