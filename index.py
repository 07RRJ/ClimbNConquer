import os, sys
import random as rng
import time
from gameFuncs import GetTime
from dataclasses import dataclass, asdict
from saveAndLoad import Defult, Save, Load
import pygame
from colours import Colours as CO

# ======================================
# SECTION: BASE
# ======================================

pygame.init()

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

def resource_path(relative_path):
    return os.path.join(get_game_folder(), relative_path)

game_folder = get_game_folder()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080, 
win = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

clock = pygame.time.Clock()

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
                pass
                # print(f"Floor {gameData.floor}-{gameData.part}, Turn: ({gameData.turn})")
            else:
                pass
                # print(f"Boss battle, Turn: ({gameData.turn})")
            enemies.GetEnemyStats()
            player.Move(gameData, enemies)

            for enemy in enemies.current:
                enemy.Move(player, enemies, gameData)

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
            pass
            # print("do you want to continue the game in endles (y/n)?")
            # if Comfirm("y"):
            #     gameData.endless = True
            # elif Comfirm("n"):
            #     return "won"
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
            pass
            # print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
            # print("Do you want to continue this run in endless (y/n)?")
            # if Comfirm("y"):
            #     gameData.endless = True
            # elif Comfirm("n"):
            #     return "won"

# ======================================
# SECTION: PRE/POST GAME
# ======================================

while runing:
    result = play()
    if result == "won":
        pass
    #     print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
    else:
        if gameData.floor > 5:
            pass
    #         print(f"You won and died in endless on floor: ({gameData.floor}-{gameData.part})\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
    #         print("=" * 22)
    #         for enemy in gameData.enemiesKilled:
    #             print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
    #         print("=" * 22)
        else:
            pass
    #         print(f"You died, floor: ({gameData.floor}-{gameData.part}), total turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
    #         print("=" * 22)
    #         for enemy in gameData.enemiesKilled:
    #             print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
    #         print("=" * 22)
    player, enemies, gameData = Defult()
    Save(player, enemies, gameData)
    # print("play again (y/n):")
    # while True: 
    #     if Comfirm("y"):
    #         break
    #     elif Comfirm("n"):
    #         runing = False
    #         break
    win.fill(CO.BLACK[3])
    pygame.display.flip()