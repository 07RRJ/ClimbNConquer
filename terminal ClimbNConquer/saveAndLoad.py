from dataclasses import asdict
from player import Player
from enemies import Enemies
from gameData import GameData
import json
import sys, os

def get_game_folder():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

SAVE_FILE = os.path.join(get_game_folder(), "virus_aka_dont_tuch.json")

def Defult():
    player = Player()
    enemies = Enemies()
    gameData = GameData()
    return player, enemies, gameData

def Save(player, enemies, gameData):
    saveData = {
        "player": asdict(player),
        "enemies": asdict(enemies),
        "gameData": asdict(gameData)
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(saveData, f, indent=4)

from time import sleep

def Load(player, enemies, gameData):
    try:
        with open(SAVE_FILE, 'r') as f:
            save_object = json.load(f)

        player = Player(**save_object["player"])
        enemies = Enemies(**save_object["enemies"])
        gameData = GameData(**save_object["gameData"])
        return player, enemies, gameData
    except:
        Save(player, enemies, gameData)
        return player, enemies, gameData