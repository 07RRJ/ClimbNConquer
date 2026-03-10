from gameFuncs import Attack, Limit, cls, Comfirm
class Player:
    def __init__(self):
        self.MAX_HP = 20
        self.HP = self.MAX_HP
        self.HEAL = 3

        self.DEF = 0
        self.BLOCK = 3

        self.STR = 1
        self.AOE = 0
        self.MULTI_ATTACK = 0

        self.BASE_STAMINA = 1
        self.STAMINA = self.BASE_STAMINA
        self.STAMINA_REGEN = 1
        self.MAX_STAMINA = 5

        self.MAX_MANA = 5
        self.MANA = 0

        self.EXP = 0
        self.NEXT_LVL = 5
        self.LVL = 0
        self.ABILITIES = [["ATTACK", 1, True], ["AOE", 3, "King Slime"], ["MULTI SLAM", 5, "Rat King"], ["HEAL", 1, True], ["BLOCK", 1, True], ["REST", 0, True]]

    def listStats(self):
        stats = [
            "Player:",
            "\n" 
            f"HP: ({self.HP}/{self.MAX_HP})",
            f", DEF ({self.DEF}/{self.BLOCK})",
            f", STAMINA({self.STAMINA}/{self.MAX_STAMINA})",
            f", LVL ({self.LVL})",
            f", EXP ({self.EXP}/{self.NEXT_LVL})",
            "\n",
            f"STR: ({self.STR})",
            f", HEAL ({self.HEAL})",
            f", BLOCK ({self.BLOCK})",
            f", REST ({self.STAMINA_REGEN})"
        ]
        print("".join(stats))

    def Move(self, gameData, enemies):
        self.DEF -= self.DEF // 2 + 1
        if self.DEF < 0:
            self.DEF = 0
        self.listStats()
        possibleMoves = []
        moveIdx = 1
        for move in self.ABILITIES:
            if move[1] <= self.STAMINA:
                if move[2] == True or gameData.enemiesKilled[move[2]] != 0:
                    possibleMoves.append(move)
                    print(f"{moveIdx}: {move[0]}")
                    moveIdx += 1
        move = possibleMoves[Limit("your move: ", 0, len(possibleMoves) + 1) - 1]
        if move[0] == "ATTACK":
            self.STAMINA -= move[1]
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            Attack(self.STR, enemies.current[enemyToAttack])
            enemies.killed(self, gameData)
        elif move[0] == "AOE":
            self.STAMINA -= move[1]
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            listToAttack = [[enemyToAttack, 1]]
            for i in range(self.AOE):
                i += 1
                listToAttack.append([enemyToAttack + i, (i + 1) / 1.5])
                listToAttack.append([enemyToAttack - i, (i + 1) / 1.5])
            for attack in listToAttack:
                if attack[0] >= 0:
                    if attack[0] <= len(enemies.current):
                        try:
                            Attack(int(self.STR / attack[1]), enemies.current[attack[0]])
                        except:
                            pass
            enemies.killed()
        elif move[0] == "MULTI SLAM":
            enemyToAttack = Limit(f"Enemy to attack (1 - {len(enemies.current)}): ", 0, len(enemies.current) + 1) - 1
            for attack in range(self.MULTI_ATTACK):
                Attack(max(int(self.STR // 2 * (attack + 2)), 1), enemies.current[enemyToAttack])
            enemies.killed()
        elif move[0] == "HEAL":
            self.STAMINA -= move[1]
            if self.HP != self.MAX_HP and self.HP + self.HEAL < self.MAX_HP:
                self.HP += self.HEAL
            else:
                self.HP = self.MAX_HP
        elif move[0] == "BLOCK":
            self.STAMINA -= move[1]
            self.DEF += self.BLOCK
        elif move[0] == "REST":
            self.STAMINA -= move[1]
            self.STAMINA += self.STAMINA_REGEN
        self.STAMINA += 1
        if self.STAMINA > self.MAX_STAMINA:
            self.STAMINA = self.MAX_STAMINA

    def ExpUp(self):
        while self.EXP >= self.NEXT_LVL:
            self.EXP -= self.NEXT_LVL
            self.LVL += 1
            self.NEXT_LVL += self.LVL
            while True:
                cls()
                print(f"You leveled up ({self.LVL - 1} > {self.LVL}), choose stat to increase:")
                lvlUpList = [
                    ("Max HP", "MAX_HP", 2),
                    ("Heal", "HEAL", 1),
                    ("Block", "BLOCK", 2),
                    ("Strength", "STR", 1),
                    ("Max Stamina", "MAX_STAMINA", 1),
                    ("Start Stamina", "BASE_STAMINA", 0.2),
                    ("Stamina Regen", "STAMINA_REGEN", 0.2),
                    ("Max Mana", "MAX_MANA", 1),
                    ("Start Mana", "MANA", 1),
                ]
                for idx, (label, attrName, increse) in enumerate(lvlUpList, 1):
                    current = getattr(self, attrName)
                    print(f"({idx}) {label}: {current} + {increse}")

                choice = Limit(f"Stat to increse (1 - {len(lvlUpList)}): ", 0, len(lvlUpList)) - 1
                print("comfirm (y)")
                if Comfirm("y"):
                    cls()
                    break
            label, attr_name, increse = lvlUpList[choice]
            current = getattr(self, attr_name)
            setattr(self, attr_name, current + increse)