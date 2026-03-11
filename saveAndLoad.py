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
    saveData = {
        "player": asdict(player),
        "enemies": asdict(enemies),
        "gameData": asdict(gameData)
    }
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

def DisplaySave(file):
    try:
        with open(save_files[file], 'r') as f:
            save_object = json.load(f)

        playerData = save_object["player"]
        gameData = save_object["gameData"]

        data = [
            f"FLOOR: ({gameData["floor"]}-{gameData["part"]})",
            f"LVL: {playerData["LVL"]}",
            f"EXP: {playerData["EXP"]}/{playerData["NEXT_LVL"]}",
            f"HP: {playerData["HP"]}/{playerData["MAX_HP"]}",
            f"HEAL: {playerData["HEAL"]}",
            f"STR: {playerData["STR"]}",
            f"DEF: {playerData["BLOCK"]}",
            f"STAMINA: {playerData["STAMINA"]}/{playerData["MAX_STAMINA"]}"
        ]

        return data
    except Exception as e:
        print(e)
        return None