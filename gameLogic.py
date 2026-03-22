from gameFuncs import ResourcePath
import pygame
from uiData import Colours as CO
import sys
from saveAndLoad import Defult, Save, Load, Remove
from uiElements import Button, Bar, DamageText, create_back_button
from gameFuncs import ResourcePath
from uiData import Data
# from time import sleep

clock = pygame.time.Clock()
BASE_WIDTH, BASE_HEIGHT = 1920, 1080

def LvlUp(screen, player):
    selectedIdx = None

    lvlUpText = Data.title_font.render(f"Lvl increesed ({player.LVL} > {player.LVL+1})", True, (CO.BLACK[2]))

    labels = (
        (
            ("Max HP", "MAX_HP", 5),
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
        [(BASE_WIDTH//4+BASE_WIDTH//6*i, BASE_HEIGHT//3)for i in range(3)],
        [(BASE_WIDTH//4+BASE_WIDTH//6*i, BASE_HEIGHT//2)for i in range(3)],
        [(BASE_WIDTH//4+BASE_WIDTH//6*i, BASE_HEIGHT//3*2)for i in range(3)],
    )

    buttons = []

    for rowIdx, row in enumerate(labels):
        for idx, label in enumerate(row):
            text, attr, increse = label
            x, y = buttonPos[rowIdx][idx]
            label = f"{text} {getattr(player, attr)} + {increse}"
            buttons.append(Button(label, pygame.Rect(x, y, 250, 75), CO.RED[2]))
    buttons.append(create_back_button())

    while player.EXP >= player.NEXT_LVL:
        clock.tick(30)
        screen.fill(CO.BLACK[4])

        screen.blit(lvlUpText, lvlUpText.get_rect(center=(BASE_WIDTH//2, 69)))

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

    ButtonRect = (
        pygame.Rect(32, BASE_HEIGHT-62, 100, 30),
        pygame.Rect(164, BASE_HEIGHT-62, 100, 30),
        pygame.Rect(296, BASE_HEIGHT-62, 100, 30),
        pygame.Rect(428, BASE_HEIGHT-62, 100, 30),
        pygame.Rect(32, BASE_HEIGHT-102, 100, 30),
        pygame.Rect(164, BASE_HEIGHT-102, 100, 30),
        pygame.Rect(296, BASE_HEIGHT-102, 100, 30),
        pygame.Rect(428, BASE_HEIGHT-102, 100, 30),
        pygame.Rect(32, BASE_HEIGHT-144, 100, 30)
    )

    buttons = [
        Button(f"attack", ButtonRect[0], CO.RED[2]),
        Button(f"heal", ButtonRect[1], CO.GREEN[2]),
        Button(f"block", ButtonRect[2], CO.BLUE[2]),
        Button(f"rest", ButtonRect[3], CO.YELLOW[2])
    ]

    inactiveButtons = []

    if gameData.enemiesKilled["King Slime"]:
        buttons.append(Button(f"aoe", ButtonRect[4], CO.RED[2]))
    else:
        inactiveButtons.append(Button(f"???", ButtonRect[4], CO.BLACK[1]))
    if gameData.enemiesKilled["Rat King"]:
        buttons.append(Button(f"regen", ButtonRect[5], CO.GREEN[2]))
    else:
        inactiveButtons.append(Button(f"???", ButtonRect[5], CO.BLACK[1]))
    if gameData.enemiesKilled["Royal Boar"]:
        buttons.append(Button(f"fortress", ButtonRect[6], CO.BLUE[2]))
    else:
        inactiveButtons.append(Button(f"???", ButtonRect[6], CO.BLACK[1]))
    if gameData.enemiesKilled["Goblin General"]:
        buttons.append(Button(f"meditate", ButtonRect[7], CO.YELLOW[2]))
    else:
        inactiveButtons.append(Button(f"???", ButtonRect[7], CO.BLACK[1]))
    if gameData.enemiesKilled["Lich"]:
        buttons.append(Button(f"nuke", ButtonRect[8], CO.RED[2]))
    else:
        inactiveButtons.append(Button(f"???", ButtonRect[8], CO.BLACK[1]))
    buttons.append(create_back_button())

    statusBars = [
        (Bar(CO.BLACK[1], 30, 30, 304, 34, None)),
        (Bar(CO.GREEN[3], 32, 32, 300, 30, (player, "HP", "MAX_HP"))),
        (Bar(CO.BLACK[1], 30, 76, 304, 34, None)),
        (Bar(CO.YELLOW[2], 32, 78, 300, 30, (player, "STAMINA", "MAX_STAMINA")))
    ]

    enemyPos = []
    for i in range(9):
        if i % 2 == 0:
            enemyPos.append((BASE_WIDTH-230-120*i, 100))
        elif i % 2 == 1:
            enemyPos.append((BASE_WIDTH-230-120*i, 380))

    dmgText = []

    displayDef =  Data.text_font.render(f"{player.DEF}", True, (CO.BLUE[2]))
    if gameData.part == 0:
        floor =  Data.title_font.render(f"Boss battle", True, (CO.BLACK[2]))
    else:
        floor =  Data.title_font.render(f"floor {gameData.floor}-{gameData.part}", True, (CO.BLACK[2]))
    turn =  Data.text_font.render(f"turn: {gameData.turn}", True, (CO.BLACK[2]))

    while player.HP > 0 and enemies.current:
        clock.tick(30)
        screen.fill(CO.BLACK[4])
        screen.blit(bg, (0, 0))
        screen.blit(block, (350, 30))

        screen.blit(displayDef, displayDef.get_rect(center=(389, 69)))
        screen.blit(floor, (200, 200))
        screen.blit(turn, (200, 300))

        for idx, btn in enumerate(buttons):
            isSelected = (idx == selectedIdx)
            btn.draw(screen, isSelected)
        
        if inactiveButtons:
            for button in inactiveButtons:
                button.draw(screen)

        for idx, enemy in enumerate(enemies.current):
            isSelected = (idx == selectedEnemyIdx)
            if idx % 2 == 0:
                enemies.Draw(screen, idx, enemyPos[idx], isSelected)
            elif idx % 2 == 1:
                enemies.Draw(screen, idx, enemyPos[idx], isSelected)

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
            selectedIdx = None
            selectedEnemyIdx = None
            for idx, btn in enumerate(buttons):
                if btn.rect.collidepoint(pos):
                    selectedIdx = idx
            for idx, enemy in enumerate(enemies.current):
                if enemy.rect.collidepoint(pos):
                    selectedEnemyIdx = idx

            if event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                for kb in gameData.keyBinds.values():
                    if key[kb[0]]:
                        selectedIdx = kb[1]

            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN) and selectedIdx != None:
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
                    playerTurn = "Nuke"
                    lastPlayerTurn = "Nuke"

                if playerTurn != False and selectedEnemyIdx != None:
                    if  lastPlayerTurn == "Attack":
                        playerTurn, theAttack = player.Attack(gameData, enemies, selectedEnemyIdx, enemyPos)
                        if theAttack:
                            dmgText.append(theAttack)

                    elif lastPlayerTurn == "Aoe":
                        playerTurn, theAttacks = player.Aoe(gameData, enemies, selectedEnemyIdx, enemyPos)
                        if theAttacks:
                            for attack in theAttacks:
                                dmgText.append(attack)

                    elif lastPlayerTurn == "Nuke":
                        playerTurn, theAttacks = player.Nuke(gameData, enemies, selectedEnemyIdx, enemyPos)
                        if theAttacks:
                            for attack in theAttacks:
                                dmgText.append(attack)
                        
        if not playerTurn:
            pygame.display.flip()
            for enemy in enemies.current:
                enemy.Move(player, enemies, gameData)
            gameData.turn += 1
            player.StartOfTurn()
            turn =  Data.text_font.render(f"turn: {gameData.turn}", True, (CO.BLACK[2]))
            displayDef =  Data.text_font.render(f"{player.DEF}", True, (CO.BLUE[2]))
            playerTurn = True

        pygame.display.flip()

    if not enemies.current:
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

def BossBuffs(player, gameData):
    player.AOE = gameData.enemiesKilled["King Slime"]
    player.REGEN = gameData.enemiesKilled["Rat King"]
    player.FORTRESS = gameData.enemiesKilled["Royal Boar"]
    player.MEDITATE = gameData.enemiesKilled["Goblin General"]
    player.NUKE = gameData.enemiesKilled["Lich"]

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
        elif result == "dead":
            Remove(file)
            return
        gameData.totalTurns += gameData.turn
        gameData.turn = 0
        LvlUp(screen, player)
        if gameData.part == 5:
            enemies.difficultyUp(gameData)
        gameData.part += 1
        if gameData.part == 1 and not gameData.floor == 1:
            BossBuffs(player, gameData)
            Save(player, enemies, gameData, file)