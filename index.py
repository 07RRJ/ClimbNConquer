import os, sys
import random as rng
import time
from gameFuncs import GetTime
from dataclasses import dataclass, asdict
from saveAndLoad import Defult, Save, Load
import pygame
from colours import Colours as CO
from uiElements import Button
from uiData import Data

# ======================================
# SECTION: BASE
# ======================================

pygame.init()

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

def resource_path(relative_path):
    return os.path.join(get_game_folder(), relative_path)

game_folder = get_game_folder()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

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


def GameMenu():
    runing = True
    selected_index = None
    buttons = [
        Button(f"{i}", pygame.Rect(150 * i, 150, 200, 60), CO.BLUE[2]) for i in range(10)
    ]
    print("init")
    while runing:
        clock.tick(30)
        screen.fill(CO.BLACK[3])

        # result = play()
        # if result == "won":
        #     pass
        #     print(f"You won!\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}")
        # else:
        #     if gameData.floor > 5:
        #         pass
        #         print(f"You won and died in endless on floor: ({gameData.floor}-{gameData.part})\ntotal turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
        #         print("=" * 22)
        #         for enemy in gameData.enemiesKilled:
        #             print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
        #         print("=" * 22)
            # else:
            #     pass
        #         print(f"You died, floor: ({gameData.floor}-{gameData.part}), total turns: {gameData.totalTurns}\nTime passed: {GetTime(gameData.startTime, time.time())}\nEnemies killed:")
        #         print("=" * 22)
        #         for enemy in gameData.enemiesKilled:
        #             print(f"- {enemy:<15}: {gameData.enemiesKilled[enemy]}")
        #         print("=" * 22)
        # player, enemies, gameData = Defult()
        # Save(player, enemies, gameData)
        # print("play again (y/n):")
        # while True: 
        #     if Comfirm("y"):
        #         break
        #     elif Comfirm("n"):
        #         runing = False
        #         break

        for i, btn in enumerate(buttons):
            is_selected = (i == selected_index)
            btn.draw(screen, is_selected=is_selected)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selected_index = i
                        break

        pygame.display.flip()

def Start():
    selected_index = None
    buttons = [
        Button(f"Start Game", pygame.Rect(BASE_WIDTH // 2 - 100, BASE_HEIGHT // 2 - 60, 200, 60), CO.BLUE[2]),
        Button(f"no clue", pygame.Rect(BASE_WIDTH // 2 - 100, BASE_HEIGHT // 2 + 60, 200, 60), CO.BLUE[2])
        # Button(f"Start Game", pygame.Rect(BASE_WIDTH // 2 + 100, BASE_HEIGHT // 2, 200, 60), CO.BLUE[2])
    ]

    title = Data.title_font.render("Card N Dungeon", True, (255, 255, 255))

    while runing:
        clock.tick(30)
        screen.fill(CO.BLACK[3])

        screen.blit(title, (BASE_WIDTH//2 - title.get_width()//2, 50))

        for i, btn in enumerate(buttons):
            is_selected = (i == selected_index)
            btn.draw(screen, is_selected=is_selected)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selected_index = i
                        break

                if selected_index == 0:
                    print("start")
                    GameMenu()

                elif selected_index == 1:
                    print("btn 1")
                    # GameMenu()

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                is_hovering = False
                for i, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selected_index = i
                        is_hovering = True
                    elif is_hovering == False:
                        selected_index = None

        pygame.display.flip()

if __name__ == "__main__":
    Start()