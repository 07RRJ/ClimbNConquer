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
    playerTurn = True
    selectedIdx = None
    selectedEnemyIdx = None
    
    bg = pygame.image.load(ResourcePath("assets/img/ability_menu.png")).convert_alpha()
    bg = pygame.transform.scale(bg, (BASE_WIDTH, BASE_HEIGHT))
    block = pygame.image.load(ResourcePath("assets/img/block.png")).convert_alpha()
    block = pygame.transform.scale(block, (78, 78))

    buttons = [
        # row 1
        Button(f"attack", pygame.Rect(32, BASE_HEIGHT-62, 100, 30), CO.RED[2]),
        Button(f"heal", pygame.Rect(164, BASE_HEIGHT-62, 100, 30), CO.GREEN[2]),
        Button(f"block", pygame.Rect(296, BASE_HEIGHT-62, 100, 30), CO.BLUE[2]),
        Button(f"rest", pygame.Rect(428, BASE_HEIGHT-62, 100, 30), CO.YELLOW[2]),
        # row 2
        Button(f"aoe", pygame.Rect(32, BASE_HEIGHT-102, 100, 30), CO.RED[2]),
        Button(f"regen", pygame.Rect(164, BASE_HEIGHT-102, 100, 30), CO.GREEN[2]),
        Button(f"fortress", pygame.Rect(296, BASE_HEIGHT-102, 100, 30), CO.BLUE[2]),
        Button(f"meditate", pygame.Rect(428, BASE_HEIGHT-102, 100, 30), CO.YELLOW[2]),
        # row 3
        Button(f"nuke", pygame.Rect(32, BASE_HEIGHT-144, 100, 30), CO.RED[2]),
        create_back_button()
    ]

    statusBars = [
        (Bar(CO.BLACK[1], 30, 30, 304, 34, None)),
        (Bar(CO.GREEN[3], 32, 32, 300, 30, (player, "HP", "MAX_HP"))),
        (Bar(CO.BLACK[1], 30, 76, 304, 34, None)),
        (Bar(CO.YELLOW[2], 32, 78, 300, 30, (player, "STAMINA", "MAX_STAMINA")))
    ]

    displayDef =  Data.text_font.render(f"{player.DEF}", True, (255, 255, 255))

    while runing:
        clock.tick(30)
        screen.fill(CO.BLACK[4])
        screen.blit(bg, (0, 0))
        screen.blit(block, (350, 30))

        screen.blit(displayDef, displayDef.get_rect(center=(389, 69)))

        for i, btn in enumerate(buttons):
            is_selected = (i == selectedIdx)
            btn.draw(screen, is_selected=is_selected)

        for idx, enemy in enumerate(enemies.current):
            enemyHp = Data.text_font.render(f"{enemy.HP}", True, (30, 200, 30))
            if idx % 2 == 0:
                enemy.Draw(screen, BASE_WIDTH-230-120*idx, 100)
                screen.blit(enemyHp, (BASE_WIDTH-230-120*idx, 300))
            if idx % 2 == 1:
                enemy.Draw(screen, BASE_WIDTH-230-120*idx, 260)
                screen.blit(enemyHp, (BASE_WIDTH-230-120*idx, 460))

        for bar in statusBars:
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
                        selectedIdx = i
                        is_hovering = True
                    elif is_hovering == False:
                        selectedIdx = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selectedIdx = i
                        break
            
                if selectedIdx == len(buttons) - 1:
                    return

                elif playerTurn:
                    if selectedIdx == 0:
                        player.Attack()
                        playerTurn = False

                    elif selectedIdx == 1:
                        player.Heal()
                        playerTurn = False

                    elif selectedIdx == 2:
                        player.Block()
                        playerTurn = False
                        displayDef =  Data.text_font.render(f"{player.DEF}", True, (255, 255, 255))

                    elif selectedIdx == 3:
                        player.Rest()
                        playerTurn = False

                    elif selectedIdx == 4:
                        playerTurn = False
                        pass

                    elif selectedIdx == 5:
                        playerTurn = False
                        pass
        if not playerTurn:
            for enemy in enemies.current:
                enemy.Move(player, enemies, gameData)
            displayDef =  Data.text_font.render(f"{player.DEF}", True, (255, 255, 255))
            playerTurn = True

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
            is_selected = (i == selectedIdx)
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
                        selectedIdx = i
                        is_hovering = True
                    elif is_hovering == False:
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
                    GameManager(0)
                    saveImgs, saveInfo = GetSaves()

                elif selectedIdx == 1:
                    GameManager(1)
                    saveImgs, saveInfo = GetSaves()

                elif selectedIdx == 2:
                    GameManager(2)
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
            is_selected = (i == selectedIdx)
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
                        selectedIdx = i
                        last_selected_index = i
                        is_hovering = True
                    elif is_hovering == False:
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