import pygame
import sys, os
from sokoban import Sokoban_Game
from prototype import Prototype_Game
from platformer import Platformer_Game
from lvls.sokoban.sokoban_lvl import maps
from scripts.level_state import load_level_state, is_level_unlocked, reset_progress
from scripts.utils import resource_path, get_levels

# Inicializácia Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Main Menu")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Farby
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 200, 0)
LOCKED_COLOR = (100, 100, 100)
BG_COLOR = (30, 30, 30)

# Trieda pre tlačidlo
class Button:
    def __init__(self, rect, text, callback, locked=False, font_size=36):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.locked = locked
        self.font = pygame.font.Font(None, font_size)

    def draw(self, surf):
        mouse_pos = pygame.mouse.get_pos()
        if self.locked:
            color = LOCKED_COLOR
        else:
            color = HIGHLIGHT if self.rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(surf, color, self.rect, 2)
        label = self.font.render(self.text, True, color)
        surf.blit(label, (self.rect.x + 10, self.rect.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and not self.locked:
                self.callback()

# Stav menu
current_state = "mode"
buttons = []
selected_mode = None
level_dict = {}  

# Tlačidlá módov
def build_mode_buttons():
    global buttons, level_dict
    level_dict = get_levels()
    buttons = []

    start_x = 150
    spacing = 300

    for i, mode in enumerate(level_dict):
        btn_rect = (start_x + i * spacing, 250, 240, 120)
        buttons.append(Button(btn_rect, mode, lambda m=mode: select_mode(m)))

    # Tlačidlo v pravom dolnom rohu
    buttons.append(Button((1020, 720, 160, 40), "Reset Progress", reset_and_reload, font_size=22))


# Po kliknutí na mód
def select_mode(mode):
    global current_state, selected_mode
    selected_mode = mode
    current_state = "level"
    build_level_buttons(mode)

# Tlačidlá levelov
def build_level_buttons(mode):
    global buttons
    buttons = []
    lvl_list = level_dict[mode]
    state = load_level_state()

    for i, lvl in enumerate(lvl_list):
        x = 100 + (i % 6) * 170
        y = 200 + (i // 6) * 110
        level_label = f"Level {i+1}"

        unlocked = is_level_unlocked(mode, level_label, i)

        if unlocked:
            callback = lambda l=lvl, n=i+1: start_game(mode, l, n)
        else:
            callback = lambda: None

        buttons.append(Button((x, y, 150, 90), level_label, callback, locked=not unlocked))

    buttons.append(Button((20, 20, 100, 40), "Back", go_back))


# Späť na výber módu
def go_back():
    global current_state
    current_state = "mode"
    build_mode_buttons()

# Spustenie hry
def start_game(mode, level_id, level_num):
    if mode == "Sokoban":
        Sokoban_Game(level_index=level_num - 1).run()
    elif mode == "Platformer":
        Platformer_Game(level_index=level_num - 1).run()
    elif mode == "Prototype":
        Prototype_Game(level_index=level_num - 1).run()

    # Po návrate z hry znova obnoví menu
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Main Menu")
    build_mode_buttons() if current_state == "mode" else build_level_buttons(mode)


def reset_and_reload():
    reset_progress()
    build_mode_buttons()


# Spustenie menu
build_mode_buttons()

while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for btn in buttons:
            btn.handle_event(event)

    title = "Select Game Mode" if current_state == "mode" else f"{selected_mode} - Select Level"
    title_surface = font.render(title, True, WHITE)
    screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

    for btn in buttons:
        btn.draw(screen)

    pygame.display.update()
    clock.tick(60)
