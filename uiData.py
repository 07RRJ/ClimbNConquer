import pygame, os
from gameFuncs import GetGameFolder, ResourcePath

class Colours():
    BLACK   = ((10, 10, 10), (50, 50, 50), (100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250))
    RED     = ((100, 30, 30), (150, 50, 50), (200, 50, 50), (250, 75, 75))
    GREEN   = ((30, 100, 30), (30, 150, 30), (30, 200, 30), (50, 250, 50))
    BLUE    = ((30, 30, 100), (30, 30, 150), (30, 30, 200), (30, 30, 250), (173, 216, 230))

pygame.init()

class Data:
    ASSETS = ResourcePath("assets")
    FONTS = ResourcePath("fonts", ASSETS)

    title_font_path = ResourcePath("assets/fonts/COPRGTB.TTF")
    text_font_path = ResourcePath("assets/fonts/corbelb.ttf")


    title_font = pygame.font.Font(title_font_path, 64)
    text_font = pygame.font.Font(text_font_path, 24)