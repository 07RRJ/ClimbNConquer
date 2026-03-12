import os, sys
import random as rng
from msvcrt import getwch
import time
from gameFuncs import cls, GetTime, Comfirm
from dataclasses import dataclass, asdict
from saveAndLoad import Defult, Save, Load

# ======================================
# SECTION: BASE
# ======================================

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

runing = True

player, enemies, gameData = Defult()
player, enemies, gameData = Load(player, enemies, gameData)

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

# ======================================
# SECTION: LVL LOGIC
# ======================================

def play():
    if player.HP > 0:
        if gameData.floor > 5:
            print("do you want to continue the game in endles (y/n)?")
            if Comfirm("y"):
                gameData.endless = True
            elif Comfirm("n"):
                return "won"
    else:
        return "dead"
    while True:
        if gameData.endless or gameData.floor < 6:
            if gameData.part == 11:
                gameData.part = 0
                enemies.generateBoss(gameData)
                gameData.floor += 1
            elif not enemies.current:
                enemies.generate(gameData)
            result = playFloor()
            if result == "dead":
                return "dead"
            elif gameData.part == 0:
                Save(player, enemies, gameData)
            elif gameData.part == 5:
                enemies.difficultyUp(gameData)
            gameData.part += 1
        else:
            cls()
            print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
            print("Do you want to continue this run in endless (y/n)?")
            if Comfirm("y"):
                gameData.endless = True
            elif Comfirm("n"):
                return "won"

# ======================================
# SECTION: PRE/POST GAME
# ======================================

while runing:
    cls()
    result = play()
    if result == "won":
        print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
    else:
        if gameData.floor > 5:
            print(f"You won and died in endless on floor: ({gameData.floor}-{gameData.part})\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
            print("=" * 22)
            for enemy in gameData.enemiesKilled:
                print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
            print("=" * 22)
        else:
            print(f"You died, floor: ({gameData.floor}-{gameData.part}), total turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
            print("=" * 22)
            for enemy in gameData.enemiesKilled:
                print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
            print("=" * 22)
    player, enemies, gameData = Defult()
    Save(player, enemies, gameData)
    print("play again (y/n):")
    while True: 
        if Comfirm("y"):
            break
        elif Comfirm("n"):
            runing = False
            break