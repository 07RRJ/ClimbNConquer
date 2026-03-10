import os, sys
import random as rng
from msvcrt import getwch
import time
from player import Player
from enemies import Enemies
from gameData import GameData
from gameFuncs import cls, GetTime, Comfirm

# ======================================
# SECTION: BASE
# ======================================

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

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
    if player.HP > 0:
        if gameData.floor > 5:
            print("do you want to continue the game in endless?")
            if Comfirm("y"):
                gameData.endless = True
            else:
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
            gameData.part += 1
            if result == "dead":
                return "dead"
            elif gameData.part == 5:
                enemies.difficultyUp(gameData)
        else:
            cls()
            print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
            print("Do you want to continue this run in endless?")
            if Comfirm("y"):
                gameData.endless = True
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