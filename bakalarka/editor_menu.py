import pygame
import sys
import os
from editor import Editor

# Inicializácia Pygame a nastavenie okna editora
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Editor Menu")
font = pygame.font.Font(None, 14)
clock = pygame.time.Clock()

# Farby
WHITE = (255, 255, 255)
HIGHLIGHT = (255, 200, 0)
BG_COLOR = (30, 30, 30)

# Načítanie všetkých dostupných máp pre editovanie
def get_editor_levels():
    return {
        "Platformer": sorted([f for f in os.listdir("lvls/platformer") if f.endswith(".json")]),
        "Prototype": sorted([f for f in os.listdir("lvls/prototype") if f.endswith(".json")]),
    }

# Trieda reprezentujúca tlačidlo v menu
class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback

    # Vykreslenie tlačidla
    def draw(self, surf):
        mouse_pos = pygame.mouse.get_pos()
        color = HIGHLIGHT if self.rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(surf, color, self.rect, 2)
        label = font.render(self.text, True, color)
        surf.blit(label, (self.rect.x + 10, self.rect.y + 10))

    # Spracovanie kliknutia
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

# Počiatočný stav menu
current_state = "mode"  # 'mode' alebo 'level'
buttons = []
selected_mode = None
level_dict = get_editor_levels()

# Vytvorenie tlačidiel pre výber módu (Platformer / Prototype)
def build_mode_buttons():
    global buttons
    buttons = []
    for i, mode in enumerate(level_dict):
        btn_rect = (100 + i * 220, 200, 200, 100)
        buttons.append(Button(btn_rect, mode, lambda m=mode: select_mode(m)))

# Po kliknutí na mód – prechod do výberu levelu
def select_mode(mode):
    global current_state, selected_mode
    selected_mode = mode
    current_state = "level"
    build_level_buttons(mode)

# Vytvorenie tlačidiel pre výber existujúcich máp alebo vytvorenie novej
def build_level_buttons(mode):
    global buttons
    buttons = []
    lvl_list = level_dict[mode]
    for i, lvl in enumerate(lvl_list):
        x = 100 + (i % 5) * 130
        y = 150 + (i // 5) * 100
        buttons.append(Button((x, y, 100, 80), f"{lvl}", lambda l=lvl: launch_editor(mode, l)))
    # Tlačidlo na vytvorenie novej mapy
    buttons.append(Button((100, 500, 200, 50), "+ New Level", lambda: launch_editor(mode, f"NewMap_{mode.lower()}.json")))
    # Tlačidlo späť
    buttons.append(Button((20, 20, 100, 40), "Back", go_back))

# Návrat do výberu módu
def go_back():
    global current_state
    current_state = "mode"
    build_mode_buttons()

# Spustenie editora pre zvolený mód a súbor mapy
def launch_editor(mode, level_path):
    pygame.quit()
    Editor(mode=mode, level_path=level_path).run()

# Inicializácia menu
build_mode_buttons()

# Hlavný cyklus menu
while True:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for btn in buttons:
            btn.handle_event(event)

    # Vykreslenie nadpisu podľa aktuálneho stavu
    title = "Editor Mode" if current_state == "mode" else f"{selected_mode} - Select/Edit Level"
    title_surface = font.render(title, True, WHITE)
    screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

    # Vykreslenie tlačidiel
    for btn in buttons:
        btn.draw(screen)

    pygame.display.update()
    clock.tick(60)
