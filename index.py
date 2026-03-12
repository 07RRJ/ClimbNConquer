import os, sys
import random as rng
import time
from gameFuncs import GetTime
from dataclasses import dataclass, asdict
from saveAndLoad import Defult, Save, Load, DisplaySave
import pygame
from uiData import Colours as CO
from uiElements import Button, create_back_button
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

def playFloor(player, enemies, gameData):
    player.DEF = 0
    gameData.turn = 0
    player.STAMINA = player.BASE_STAMINA
    while True:
        if enemies.current and player.HP > 0:
            gameData.turn += 1
            if gameData.part != 0:
                pass
            else:
                pass
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

def play(file):
    player, enemies, gameData = Defult()
    player, enemies, gameData = Load(player, enemies, gameData, file)
    runing = True
    
    buttons = [
        Button(f"Load Save 1", pygame.Rect(BASE_WIDTH//5-100, BASE_HEIGHT-150, 200, 60), CO.BLUE[2]),
        Button(f"Load Save 2", pygame.Rect(BASE_WIDTH//2-100, BASE_HEIGHT-150, 200, 60), CO.BLUE[2]),
        Button(f"Load Save 3", pygame.Rect(BASE_WIDTH//5*4-100, BASE_HEIGHT-150, 200, 60), CO.BLUE[2]),
        create_back_button()
    ]
    if player.HP > 0:
        if gameData.floor > 5:
            pass
    else:
        return "dead"
    while runing:
        clock.tick(30)
        screen.fill(CO.BLACK[3])

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
                        is_hovering = True
                    elif is_hovering == False:
                        selected_index = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selected_index = i
                        break
            
                if selected_index == 0:
                    play(0)
        if gameData.endless or gameData.floor < 6:
            if gameData.part == 11:
                gameData.part = 0
                enemies.generateBoss(gameData)
                gameData.floor += 1
            elif not enemies.current:
                enemies.generate(gameData)
            result = playFloor(player, enemies, gameData)
            if result == "dead":
                return "dead"
            elif gameData.part == 0:
                Save(player, enemies, gameData, file)
            elif gameData.part == 5:
                enemies.difficultyUp(gameData)
            gameData.part += 1
        else:
            pass

# ======================================
# SECTION: PRE/POST GAME
# ======================================

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

    saveInfo = []

    saveData = DisplaySave(0)
    saveData1 = DisplaySave(1)
    saveData2 = DisplaySave(2)

    existingSaveImg = pygame.image.load(ResourcePath("assets/img/save.png")).convert_alpha()
    existingSaveImg = pygame.transform.scale(existingSaveImg, (400, 700))

    noneExistingSaveImg = pygame.image.load(ResourcePath("assets/img/noSave.png")).convert_alpha()
    noneExistingSaveImg = pygame.transform.scale(noneExistingSaveImg, (400, 200))

    saveImgs = []

    if saveData:
        idx = 0
        saveImgs.append((existingSaveImg, (BASE_WIDTH//5-180, 180)))
        for data in saveData:
            if data[1]:
                key = Data.text_font.render(data[0], True, (0, 0, 0))
                value = Data.text_font.render(data[1], True, (0, 0, 0))
                saveInfo.append((key, (BASE_WIDTH//5-100, 200+24*idx)))
                saveInfo.append((value, (BASE_WIDTH//5+100-value.get_width(), 200+24*idx)))
            else:
                idx += 1
                key = Data.text_font1.render(data[0], True, (0, 0, 0))
                saveInfo.append((key, (BASE_WIDTH//5-100, 200+24*idx)))
                idx += 0.4
            idx += 1
    else:
        saveImgs.append((noneExistingSaveImg, (BASE_WIDTH//5-180, 180)))

    
    if saveData1:
        idx = 0
        saveImgs.append((existingSaveImg, (BASE_WIDTH//2-180, 180)))
        for data in saveData1:
            if data[1]:
                key = Data.text_font.render(data[0], True, (0, 0, 0))
                value = Data.text_font.render(data[1], True, (0, 0, 0))
                saveInfo.append((key, (BASE_WIDTH//2-100, 200+24*idx)))
                saveInfo.append((value, (BASE_WIDTH//2+100-value.get_width(), 200+24*idx)))
            else:
                idx += 1
                key = Data.text_font1.render(data[0], True, (0, 0, 0))
                saveInfo.append((key, (BASE_WIDTH//2-100, 200+24*idx)))
                idx += 0.4
            idx += 1
    else:
        saveImgs.append((noneExistingSaveImg, (BASE_WIDTH//2-180, 180)))
    
    if saveData2:
        idx = 0
        saveImgs.append((existingSaveImg, (BASE_WIDTH//5*4-180, 180)))
        for data in saveData2:
            if data[1]:
                key = Data.text_font.render(data[0], True, (0, 0, 0))
                value = Data.text_font.render(data[1], True, (0, 0, 0))
                saveInfo.append((key, (BASE_WIDTH//5*4-100, 200+24*idx)))
                saveInfo.append((value, (BASE_WIDTH//5*4+100-value.get_width(), 200+24*idx)))
            else:
                idx += 1
                key = Data.text_font1.render(data[0], True, (0, 0, 0))
                saveInfo.append((key, (BASE_WIDTH//5*4-100, 200+24*idx)))
                idx += 0.4
            idx += 1
    else:
        saveImgs.append((noneExistingSaveImg, (BASE_WIDTH//5*4-180, 180)))

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
            
                if selected_index == 0:
                    play(0)

                elif selected_index == 1:
                    play(1)

                elif selected_index == 2:
                    play(2)

                elif selected_index == len(buttons) - 1:
                    return

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

    title = Data.title_font.render("Card N Dungeon", True, (255, 255, 255))

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

                if selected_index == 0:
                    GameMenu()

                elif selected_index == 1:
                    pass

                elif selected_index == len(buttons) - 1:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    Start()