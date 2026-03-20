from gameFuncs import ResourcePath
import pygame
from uiData import Colours as CO
import os, sys
from saveAndLoad import Defult, Save, Load
from uiElements import Button, Bar, DamageText, create_back_button
from gameFuncs import ResourcePath
from uiData import Data
from time import sleep

clock = pygame.time.Clock()
BASE_WIDTH, BASE_HEIGHT = 1920, 1080

def lvlUp(screen, player):
    selectedIdx = None

    labels = (
        (
            ("Max HP", "MAX_HP", 2),
            ("Strength", "STR", 1),
            ("Max Stamina", "MAX_STAMINA", 1)
        ),
        (
            ("Start Stamina", "BASE_STAMINA", 0.2),
            ("Heal", "HEAL", 1),
            ("Block", "BLOCK", 2)
        ),
        (
            ("Stamina Regen", "STAMINA_REGEN", 0.2),
            ("Max Mana", "MAX_MANA", 1),
            ("Start Mana", "MANA", 1)
        )
    )
    buttonPos = (
        [(BASE_WIDTH//10+BASE_WIDTH//3*i, BASE_HEIGHT//5)for i in range(3)],
        [(BASE_WIDTH//10+BASE_WIDTH//3*i, BASE_HEIGHT//2)for i in range(3)],
        [(BASE_WIDTH//10+BASE_WIDTH//3*i, BASE_HEIGHT//5*4)for i in range(3)],
    )

    buttons = []

    for rowIdx, row in enumerate(labels):
        for idx, label in enumerate(row):
            text, attr, increse = label
            x, y = buttonPos[rowIdx][idx]
            label = f"{text} {getattr(player, attr)} + {increse}"
            buttons.append(Button(label, pygame.Rect(x, y, 200, 60), CO.RED[2]))
    buttons.append(create_back_button())

    while player.EXP >= player.NEXT_LVL:
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

                elif selectedIdx != None:
                    label, attr_name, increse = labels[(selectedIdx//3)%3][selectedIdx%3]
                    current = getattr(player, attr_name)
                    setattr(player, attr_name, current + increse)
                    player.EXP -= player.NEXT_LVL
                    player.LVL += 1
                    player.NEXT_LVL += player.LVL

        pygame.display.flip()

def play(player, enemies, gameData, screen):
    playerTurn = True
    lastPlayerTurn = None
    selectedIdx = None
    selectedEnemyIdx = None
    
    player.DEF = 0
    player.STAMINA = player.BASE_STAMINA

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

    enemyPos = []
    for i in range(9):
        if i % 2 == 0:
            enemyPos.append(i, BASE_WIDTH-230-120*i, 100)
        elif i % 2 == 1:
            enemyPos.append(i, BASE_WIDTH-230-120*i, 320)

    dmgText = []

    displayDef =  Data.text_font.render(f"{player.DEF}", True, (CO.BLUE[2]))
    if gameData.part == 0:
        floor =  Data.title_font.render(f"Boss battle", True, (CO.BLACK[2]))
    else:
        floor =  Data.title_font.render(f"floor {gameData.floor}-{gameData.part}", True, (CO.BLACK[2]))

    while player.HP > 0 and enemies.current:
        clock.tick(30)
        screen.fill(CO.BLACK[4])
        screen.blit(bg, (0, 0))
        screen.blit(block, (350, 30))

        screen.blit(displayDef, displayDef.get_rect(center=(389, 69)))
        screen.blit(floor, (200, 200))

        for idx, btn in enumerate(buttons):
            isSelected = (idx == selectedIdx)
            btn.draw(screen, isSelected)

        for idx, enemy in enumerate(enemies.current):
            isSelected = (idx == selectedEnemyIdx)
            if idx % 2 == 0:
                enemies.Draw(screen, idx, BASE_WIDTH-230-120*idx, 100, isSelected)
            elif idx % 2 == 1:
                enemies.Draw(screen, idx, BASE_WIDTH-230-120*idx, 320, isSelected)

        for bar in statusBars:
            bar.draw(screen)

        for dt in dmgText[:]:
            if dt.alive:
                dt.draw(screen)
            else:
                dmgText.remove(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pos = pygame.mouse.get_pos()
            isHovering = False
            for idx, btn in enumerate(buttons):
                if btn.rect.collidepoint(pos):
                    selectedIdx = idx
                    isHovering = True
                elif isHovering == False:
                    selectedIdx = None
            isHoveringEnemy = False
            for idx, enemy in enumerate(enemies.current):
                if enemy.rect.collidepoint(pos):
                    selectedEnemyIdx = idx
                    isHoveringEnemy = True
                elif isHoveringEnemy == False:
                    selectedEnemyIdx = None

            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:


                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    for kb in gameData.keyBinds.values():
                        if keys[kb[0]]:
                            selectedIdx = kb[1]

                if selectedIdx == len(buttons) - 1 or selectedIdx == "quit":
                    return "quit"

                # elif playerTurn == True:
                elif selectedIdx == 0:
                    playerTurn = "Attack"
                    lastPlayerTurn = "Attack"

                elif selectedIdx == 1:
                    player.Heal()
                    playerTurn = False

                elif selectedIdx == 2:
                    player.Block()
                    playerTurn = False

                elif selectedIdx == 3:
                    player.Rest()
                    playerTurn = False

                elif selectedIdx == 4:
                    playerTurn = "Aoe"
                    lastPlayerTurn = "Aoe"

                elif selectedIdx == 5:
                    player.Regen()
                    playerTurn = False

                elif selectedIdx == 6:
                    player.Fortress()
                    playerTurn = False

                elif selectedIdx == 7:
                    player.Meditate()
                    playerTurn = False

                elif selectedIdx == 8:
                    player.Nuke()
                    playerTurn = False

                if playerTurn != False and selectedEnemyIdx != None:
                    if  lastPlayerTurn == "Attack":
                        playerTurn, theAttack = player.Attack(gameData, enemies, selectedEnemyIdx, enemyPos)
                        if theAttack:
                            dmgText.append(theAttack)

                    elif lastPlayerTurn == "Aoe":
                        playerTurn, theAttack = player.Attack(gameData, enemies, selectedEnemyIdx, enemyPos)
                        if theAttack:
                            dmgText.append(theAttack)
                        
        if not playerTurn:
            pygame.display.flip()
            for enemy in enemies.current:
                enemy.Move(player, enemies, gameData)
            displayDef =  Data.text_font.render(f"{player.DEF}", True, (CO.BLUE[2]))
            player.STAMINA += player.STAMINA_REGEN
            if player.STAMINA >= player.MAX_STAMINA:
                player.STAMINA = player.MAX_STAMINA
            player.DEF -= player.DEF // 2 + 1
            if player.DEF < 0:
                player.DEF = 0
            playerTurn = True

        pygame.display.flip()

    if not enemies.current:
        lvlUp(screen, player)
        # Won(screen)
        return "won"
    elif player.HP <= 0:
        # Dead(screen)
        return "dead"

def Won(screen):
    buttons = [
        create_back_button()
    ]
    while True:
        clock.tick(30)
        screen.fill(CO.GREEN[2])

        pygame.display.flip()

def Dead(screen):
    buttons = [
        create_back_button()
    ]
    while True:
        clock.tick(30)
        screen.fill(CO.RED[2])
        for button in buttons:
            button.draw()
    # death in endless should be separate
        pygame.display.flip()

def GameManager(file, screen):
    runing = True
    player, enemies, gameData = Defult()
    player, enemies, gameData = Load(player, enemies, gameData, file)
    while runing:
        # if gameData.endless or gameData.floor < 6:
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
            return
        elif gameData.part == 5:
            enemies.difficultyUp(gameData)
        Save(player, enemies, gameData, file)
        gameData.part += 1
        # else:
        #     pass