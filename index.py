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

# ======================================
# SECTION: LVL LOGIC
# ======================================

def play(player, enemies, gameData):
    runing = True
    selected_index = None
    
    buttons = [
        Button(f"attack", pygame.Rect(32, BASE_HEIGHT-64, 100, 30), CO.RED[2]),
        Button(f"heal", pygame.Rect(164, BASE_HEIGHT-64, 100, 30), CO.GREEN[2]),
        Button(f"block", pygame.Rect(296, BASE_HEIGHT-64, 100, 30), CO.BLUE[2]),
        Button(f"rest", pygame.Rect(428, BASE_HEIGHT-64, 100, 30), CO.YELLOW[1]),
        create_back_button()
    ]

    status_bars = [
        (Bar(CO.BLACK[1], 98, 98, 304, 34, None)),
        (Bar(CO.GREEN[3], 100, 100, 300, 30, (player, "HP", "MAX_HP"))),
        (Bar(CO.BLACK[1], 98, 198, 304, 34, None)),
        (Bar(CO.YELLOW[1], 100, 200, 300, 30, (player, "STAMINA", "MAX_STAMINA")))
    ]
    # status_bars = [
    #     (Bar(CO.BLACK[1], 98, 98, 304, 34)),
    #     (Bar(CO.GREEN[3], 100, 100, 300, 30)),
    #     (Bar(CO.BLACK[1], 98, 198, 304, 34)),
    #     (Bar(CO.YELLOW[1], 200, 200, 300, 30))
    # ]

    while runing:
        clock.tick(30)
        screen.fill(CO.BLACK[3])

        for i, btn in enumerate(buttons):
            is_selected = (i == selected_index)
            btn.draw(screen, is_selected=is_selected)
        
        for bar in status_bars:
            bar.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                is_hovering = False
                for i, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selected_index = i
                        is_hovering = True
                    elif is_hovering == False:
                        selected_index = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selected_index = i
                        break
            
                if selected_index == len(buttons) - 1:
                    return

                elif selected_index == 0:
                    player.Attack()

                elif selected_index == 1:
                    player.Heal()

                elif selected_index == 2:
                    player.Block()

                elif selected_index == 3:
                    player.Rest()

                elif selected_index == 4:
                    pass

                elif selected_index == 5:
                    pass

        pygame.display.flip()

# ======================================
# SECTION: PRE/POST GAME
# ======================================

def Won():
    pass

def Dead():
    pass
    # death in endless should be separate

def GameManager(file):
    player, enemies, gameData = Defult()
    player, enemies, gameData = Load(player, enemies, gameData, file)
    if gameData.endless or gameData.floor < 6:
        if gameData.part == 11:
            gameData.part = 0
            enemies.generateBoss(gameData)
            gameData.floor += 1
        elif not enemies.current:
            enemies.generate(gameData)
        result = play(player, enemies, gameData)
        if result == "dead":
            Dead()
            return
        elif gameData.part == 0:
            Save(player, enemies, gameData, file)
        elif gameData.part == 5:
            enemies.difficultyUp(gameData)
        gameData.part += 1
    else:
        pass

def GameMenu():
    runing = True
    selected_index = None

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
        screen.fill(CO.BLACK[3])
        screen.blit(title, (BASE_WIDTH//2 - title.get_width()//2, 50))

        for i, btn in enumerate(buttons):
            is_selected = (i == selected_index)
            btn.draw(screen, is_selected=is_selected)
        
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
                is_hovering = False
                for i, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selected_index = i
                        is_hovering = True
                    elif is_hovering == False:
                        selected_index = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selected_index = i
                        break

                if selected_index == len(buttons) - 1:
                    return
            
                elif selected_index == 0:
                    GameManager(0)

                elif selected_index == 1:
                    GameManager(1)

                elif selected_index == 2:
                    GameManager(2)

        pygame.display.flip()

def Start():
    selected_index = None
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
            is_selected = (i == selected_index)
            btn.draw(screen, is_selected=is_selected)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                is_hovering = False
                for i, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selected_index = i
                        last_selected_index = i
                        is_hovering = True
                    elif is_hovering == False:
                        selected_index = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selected_index = i
                        break

                if selected_index == len(buttons) - 1:
                    pygame.quit()
                    sys.exit()

                elif selected_index == 0:
                    GameMenu()

                elif selected_index == 1:
                    pass

        pygame.display.flip()

if __name__ == "__main__":
    Start()