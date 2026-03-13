import pygame, os
from dataclasses import dataclass
from gameFuncs import GetGameFolder, ResourcePath
from saveAndLoad import GetSaveData
from uiData import Data
from uiData import Colours as CO

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080

# title_font = pygame.font.SysFont("Copperplate Gothic", 64, bold=True)
# text_font = pygame.font.SysFont("Arial", 24, bold=True)

# PLAYER_SIZE = 30

# images_folder = os.path.join(GetGameFolder(), "img")
# player_img = pygame.image.load(ResourcePath("player.png")).convert_alpha()
# player_img = pygame.transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))

@dataclass(slots=True)
class Button:
    text: str
    rect: pygame.Rect
    color: tuple
    font: pygame.font.Font = Data.text_font
    label: pygame.Surface = None
    label_rect: pygame.Rect = None

    def __post_init__(self):
        self.label = self.font.render(self.text, True, (255, 255, 255))
        self.label_rect = self.label.get_rect(center=self.rect.center)

    def draw(self, screen, is_selected=False):
        if is_selected:
            highlight_rect = self.rect.inflate(12, 12)
            pygame.draw.rect(screen, (255, 200, 0), highlight_rect, border_radius=8)

        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)

        screen.blit(self.label, self.label_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def create_back_button(back = True):
    button_width, button_height = 120, 60
    button_x = BASE_WIDTH - button_width - 20
    button_y = BASE_HEIGHT - button_height - 20
    if back:
        return Button("Back", pygame.Rect(button_x, button_y, button_width, button_height), CO.RED[2])
    else:
        return Button("Quit", pygame.Rect(button_x, button_y, button_width, button_height), CO.RED[2])

@dataclass(slots=True)
class Bar:
    colour: tuple
    x: float
    y: float
    width: int
    height: int
    text: tuple
    # rect: pygame.Rect

    def draw(self, screen):
        if self.text:
            value = getattr(self.text[0], self.text[1])
            value1 = getattr(self.text[0], self.text[2])
            rect = pygame.Rect(self.x, self.y, self.width*value//value1, self.height)
            pygame.draw.rect(screen, self.colour, rect)
            
            text = Data.text_font.render(f"{value}/{value1}", True, (CO.BLACK[3]))
            screen.blit(text, text.get_rect(center=(self.x+self.width//2, self.y+self.height//2)))
        else:
            rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, self.colour, rect)

def GetSaves():
    saveInfo = []

    saveData = GetSaveData(0)
    saveData1 = GetSaveData(1)
    saveData2 = GetSaveData(2)

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
    
    return saveImgs, saveInfo