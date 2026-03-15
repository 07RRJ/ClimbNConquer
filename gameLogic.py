from gameFuncs import ResourcePath
import pygame
from uiData import Colours as CO
import os, sys
import random as rng
from gameFuncs import GetTime
from dataclasses import dataclass, asdict
from saveAndLoad import Defult, Save, Load
from uiElements import Button, Bar, create_back_button
from gameFuncs import GetGameFolder, ResourcePath
from uiData import Data

clock = pygame.time.Clock()
BASE_WIDTH, BASE_HEIGHT = 1920, 1080

def lvlUp(screen, player):
    labels = (
        (f"Max hp", f"{player.MAX_HP}", 2),
        f"Heal" f"{player.HEAL} + 1",
        f" {player.BLOCK} + 2",
        f" {player.STR} + 1",
        f" {player.MAX_STAMINA} + 1",
        f" {player.BASE_STAMINA} + 0.2",
        f" {player.STAMINA_REGEN} + 0.2"
        # f"Max hp {player.MAX_MANA} + 1",
        # f"Max hp {player.MANA} + 1",
    )
    buttons = []

    for idx, label in enumerate(labels):
        buttons.append(Button(label, pygame.Rect(32 * idx, BASE_HEIGHT-62, 100, 30), CO.RED[2]))
    buttons.append(create_back_button())

# ("Max HP", "MAX_HP", 2),
# ("Heal", "HEAL", 1),
# ("Block", "BLOCK", 2),
# ("Strength", "STR", 1),
# ("Max Stamina", "MAX_STAMINA", 1),
# ("Start Stamina", "BASE_STAMINA", 0.2),
# ("Stamina Regen", "STAMINA_REGEN", 0.2),
# ("Max Mana", "MAX_MANA", 1),
# ("Start Mana", "MANA", 1),

    while True:
        clock.tick(30)
        screen.fill(CO.BLACK[4])

        for idx, btn in enumerate(buttons):
            isSelected = (idx == selectedIdx)
            btn.draw(screen, isSelected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                isHovering = False
                for idx, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selectedIdx = idx
                        isHovering = True
                    elif isHovering == False:
                        selectedIdx = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for idx, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selectedIdx = idx
                        break
            
                if selectedIdx == len(buttons) - 1:
                    return "quit"

                elif playerTurn:
                    if selectedIdx == 0:
                        player.MAX_HP += 2

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

        # f"Max hp {player.MAX_HP} + 2",
        # f"Max hp {player.HEAL} + 1",
        # f"Max hp {player.BLOCK} + 2",
        # f"Max hp {player.STR} + 1",
        # f"Max hp {player.MAX_STAMINA} + 1",
        # f"Max hp {player.BASE_STAMINA} + 0.2",
        # f"Max hp {player.STAMINA_REGEN} + 0.2"
        pygame.display.flip()

def play(player, enemies, gameData, screen):
    # runing = True
    playerTurn = True
    lastPlayerTurn = None
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

    while player.HP > 0 and enemies.current:
        clock.tick(30)
        screen.fill(CO.BLACK[4])
        screen.blit(bg, (0, 0))
        screen.blit(block, (350, 30))

        screen.blit(displayDef, displayDef.get_rect(center=(389, 69)))

        for idx, btn in enumerate(buttons):
            isSelected = (idx == selectedIdx)
            btn.draw(screen, isSelected)

        for idx, enemy in enumerate(enemies.current):
            isSelected = (idx == selectedEnemyIdx)
            enemyHp = Data.text_font.render(f"{enemy.HP}", True, (30, 200, 30))
            if idx % 2 == 0:
                enemies.Draw(screen, idx, BASE_WIDTH-230-120*idx, 100, isSelected)
                screen.blit(enemyHp, (BASE_WIDTH-230-120*idx, 300))
            elif idx % 2 == 1:
                enemies.Draw(screen, idx, BASE_WIDTH-230-120*idx, 320, isSelected)
                screen.blit(enemyHp, (BASE_WIDTH-230-120*idx, 520))

        for bar in statusBars:
            bar.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                isHovering = False
                for idx, btn in enumerate(buttons):
                    if btn.rect.collidepoint(pos):
                        selectedIdx = idx
                        isHovering = True
                    elif isHovering == False:
                        selectedIdx = None
                for idx, enemy in enumerate(enemies.current):
                    if enemy.rect.collidepoint(pos):
                        selectedEnemyIdx = idx
                        isHovering = True
                    elif isHovering == False:
                        selectedEnemyIdx = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for idx, btn in enumerate(buttons):
                    if btn.is_clicked(pos):
                        selectedIdx = idx
                        break
                for idx, enemy in enumerate(enemies.current):
                    if enemy.rect.collidepoint(pos):
                        selectedEnemyIdx = idx
            
                if selectedIdx == len(buttons) - 1:
                    return "quit"

                elif playerTurn:
                    if selectedIdx == 0:
                        playerTurn = "Attack"
                        lastPlayerTurn = "Attack"

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

                    elif playerTurn == "Attack" or lastPlayerTurn == "Attack":
                        if selectedEnemyIdx != None:
                            player.Attack(gameData, enemies, selectedEnemyIdx)
                            playerTurn = False
        if not playerTurn:
            for enemy in enemies.current:
                enemy.Move(player, enemies, gameData)
            displayDef =  Data.text_font.render(f"{player.DEF}", True, (255, 255, 255))
            playerTurn = True

        pygame.display.flip()
    
    if not enemies.current:
        while player.EXP >= player.NEXT_LVL:
            lvlUp(screen, player)
        return "won"
    elif player.HP <= 0:
        return "dead"

def Won():
    pass

def Dead():
    pass
    # death in endless should be separate

def GameManager(file, screen):
    runing = True
    player, enemies, gameData = Defult()
    player, enemies, gameData = Load(player, enemies, gameData, file)
    while runing:
        if gameData.endless or gameData.floor < 6:
            if gameData.part == 11:
                gameData.part = 0
                enemies.generateBoss(gameData)
                gameData.floor += 1
            elif not enemies.current:
                enemies.generate(gameData)
            result = play(player, enemies, gameData, screen)
            if result == "quit":
                return
            if result == "dead":
                Dead()
                return
            elif gameData.part == 5:
                enemies.difficultyUp(gameData)
            Save(player, enemies, gameData, file)
            gameData.part += 1
        else:
            pass