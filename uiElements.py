import pygame, os
from dataclasses import dataclass
from gameFuncs import GetGameFolder, ResourcePath

ASSETS = ResourcePath("assets")
FONTS = ResourcePath("fonts", ASSETS)

title_font_path = ResourcePath("assets/fonts/COPRGTB.TTF")
text_font_path = ResourcePath("assets/fonts/corbelb.ttf")

pygame.init()

title_font = pygame.font.Font(title_font_path, 64)
text_font = pygame.font.Font(text_font_path, 24)

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
    font: pygame.font.Font = text_font
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