import pygame, os
from gameFuncs import GetGameFolder, ResourcePath

pygame.init()
class Data:
    ASSETS = ResourcePath("assets")
    FONTS = ResourcePath("fonts", ASSETS)

    title_font_path = ResourcePath("assets/fonts/COPRGTB.TTF")
    text_font_path = ResourcePath("assets/fonts/corbelb.ttf")


    title_font = pygame.font.Font(title_font_path, 64)
    text_font = pygame.font.Font(text_font_path, 24)