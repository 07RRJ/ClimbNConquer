import os, sys
import random as rng
import time
from gameFuncs import GetTime
from dataclasses import dataclass, asdict
from saveAndLoad import Defult, Save, Load
import pygame
from uiData import Colours as CO
from uiElements import Button, Bar, create_back_button, GetSaves
from gameFuncs import GetGameFolder, ResourcePath
from uiData import Data
from gameLogic import GameManager

# ======================================
# SECTION: BASE
# ======================================

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

clock = pygame.time.Clock()

# ======================================
# SECTION: FUNCS
# ======================================

# def MenuLoop():

# ======================================
# SECTION: THE GAME LOOP STUFF
# ======================================

# def playFloor(player, enemies, gameData):
#     player.DEF = 0
#     gameData.turn = 0
#     player.STAMINA = player.BASE_STAMINA
#     while True:
#         if enemies.current and player.HP > 0:
#             gameData.turn += 1
#             if gameData.part != 0:
#                 pass
#             else:
#                 pass
#             enemies.GetEnemyStats()
#             player.Move(gameData, enemies)

#             for enemy in enemies.current:
#                 enemy.Move(player, enemies, gameData)

#         gameData.totalTurns += gameData.turn
#         if not enemies.current:
#             player.ExpUp()
#             return "won"
#         elif player.HP <= 0:
#             return "dead"

def GameMenu():
    runing = True
    selectedIdx = None

    title = Data.title_font.render("SELECT SAVE", True, (255, 255, 255))

    buttons = [
        Button(f"Load Save 1", pygame.Rect(BASE_WIDTH//5-100, BASE_HEIGHT-150, 200, 60), CO.BLUE[2]),
        Button(f"Load Save 2", pygame.Rect(BASE_WIDTH//2-100, BASE_HEIGHT-150, 200, 60), CO.BLUE[2]),
        Button(f"Load Save 3", pygame.Rect(BASE_WIDTH//5*4-100, BASE_HEIGHT-150, 200, 60), CO.BLUE[2]),
        create_back_button()
    ]

# https://stackoverflow.com/questions/36272029/clickable-images-in-pygame

    saveImgs, saveInfo = GetSaves()

    while runing:
        clock.tick(30)
        screen.fill(CO.BLACK[4])
        screen.blit(title, (BASE_WIDTH//2 - title.get_width()//2, 50))

        for i, btn in enumerate(buttons):
            isSelected = (i == selectedIdx)
            btn.draw(screen, isSelected)
        
        for data in saveImgs:
            img, xy = data
            screen.blit(img, xy)

        for idx, info in enumerate(saveInfo):
            item, xy = info
            screen.blit(item, xy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                isHovering = False
                for i, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selectedIdx = i
                        isHovering = True
                    elif isHovering == False:
                        selectedIdx = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selectedIdx = i
                        break

                if selectedIdx == len(buttons) - 1:
                    return
            
                elif selectedIdx == 0:
                    GameManager(0, screen)
                    saveImgs, saveInfo = GetSaves()

                elif selectedIdx == 1:
                    GameManager(1, screen)
                    saveImgs, saveInfo = GetSaves()

                elif selectedIdx == 2:
                    GameManager(2, screen)
                    saveImgs, saveInfo = GetSaves()

        pygame.display.flip()

def Start():
    selectedIdx = None
    last_selected_index = 0

    runing = True

    bg = pygame.image.load(ResourcePath("assets/img/mainMenu.png")).convert_alpha()
    bg = pygame.transform.scale(bg, (BASE_WIDTH, BASE_HEIGHT))

    buttons = [
        Button(f"Start Game", pygame.Rect(BASE_WIDTH//2-100, BASE_HEIGHT//2-60, 200, 60), CO.BLUE[2]),
        Button(f"no clue", pygame.Rect(BASE_WIDTH//2-100, BASE_HEIGHT//2+60, 200, 60), CO.BLUE[2]),
        create_back_button(back=False)
    ]

    title = Data.title_font.render("Climb N Conquer", True, (255, 255, 255))

    while runing:
        clock.tick(30)
        screen.blit(bg, (0, 0))
        screen.blit(title, (BASE_WIDTH//2-title.get_width()//2, 50))

        for i, btn in enumerate(buttons):
            isSelected = (i == selectedIdx)
            btn.draw(screen, isSelected)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                isHovering = False
                for i, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selectedIdx = i
                        last_selected_index = i
                        isHovering = True
                    elif isHovering == False:
                        selectedIdx = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selectedIdx = i
                        break

                if selectedIdx == len(buttons) - 1:
                    pygame.quit()
                    sys.exit()

                elif selectedIdx == 0:
                    GameMenu()

                elif selectedIdx == 1:
                    pass

        pygame.display.flip()

if __name__ == "__main__":
    Start()