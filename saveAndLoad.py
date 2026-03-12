from dataclasses import asdict
from player import Player
from enemies import Enemies
from gameData import GameData
import json
import sys, os

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

save_files = (
    os.path.join(get_game_folder(), "virus_aka_dont_tuch.json"),
    os.path.join(get_game_folder(), "virus_aka_dont_tuch1.json"),
    os.path.join(get_game_folder(), "virus_aka_dont_tuch2.json")
)

def Defult():
    player = Player()
    enemies = Enemies()
    gameData = GameData()
    return player, enemies, gameData

def Save(player, enemies, gameData, file):
    if player.HP > 0:
        saveData = {
            "player": asdict(player),
            "enemies": asdict(enemies),
            "gameData": asdict(gameData)
        }
    else:
        saveData = []
    with open(save_files[file], "w", encoding="utf-8") as f:
        json.dump(saveData, f, indent=4)

def Load(player, enemies, gameData, file):
    try:
        with open(save_files[file], 'r') as f:
            save_object = json.load(f)

        player = Player(**save_object["player"])
        enemies = Enemies(**save_object["enemies"])
        gameData = GameData(**save_object["gameData"])
        return player, enemies, gameData
    except:
        Save(player, enemies, gameData, file)
        return player, enemies, gameData

def GetSaveData(file):
    try:
        with open(save_files[file], 'r') as f:
            save_object = json.load(f)

        playerData = save_object["player"]
        gameData = save_object["gameData"]

        data = [
            ("Player Info:", False),
            ("Floor", f"({gameData['floor']}-{gameData['part']})"),
            ("Total turns", f"({gameData['totalTurns']})"),
            ("Lvl", f"{playerData['LVL']}"),
            ("Exp", f"{playerData['EXP']}/{playerData['NEXT_LVL']}"),
            ("Hp", f"{playerData['HP']}/{playerData['MAX_HP']}"),
            ("Heal", f"{playerData['HEAL']}"),
            ("Str", f"{playerData['STR']}"),
            ("Def", f"{playerData['BLOCK']}"),
            ("Stamina", f"{playerData['STAMINA']}/{playerData['MAX_STAMINA']}"),
            ("Slaughter Tome:", False)
        ]

        for enemy in gameData["enemiesKilled"]:
            data.append((f"{enemy}", f"{gameData['enemiesKilled'][enemy]}"))

        return data
    except Exception as e:
        print(e)
        return None