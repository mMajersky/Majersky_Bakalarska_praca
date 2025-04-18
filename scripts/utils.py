import pygame
import os, sys, json
from scripts.ui import LevelCompleteMessage

# Základná cesta ku všetkým obrázkom
base_img_path = "assets/imgs/"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller používa tento dočasný priečinok
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# Funkcia pre načítanie jedného obrázka s voliteľným zväčšením
def load_image(path, scale=1, colorkey=(0, 0, 0)):
    img = pygame.image.load(resource_path("assets/imgs/" + path)).convert()
    img.set_colorkey(colorkey)
    width, height = img.get_size()
    img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
    return img


# Funkcia pre načítanie všetkých obrázkov z daného priečinka ako zoznam
def load_images(folder):
    images = []
    full_path = "assets/imgs/" + folder
    resolved_path = resource_path(full_path)
    for img_name in sorted(os.listdir(resolved_path)):
        images.append(load_image(folder + "/" + img_name))
    return images


# v budúcnosti sa sem pridajú skripty na animácie

def fade_transition(screen, clock, duration=2500, steps=30, color=(0, 0, 0), show_level_complete_message=False):

    fade = pygame.Surface(screen.get_size())
    fade.fill(color)
    delay = duration // steps

    if show_level_complete_message:
        message = LevelCompleteMessage(screen)
        message.visible = True
        message.render()
        pygame.display.update()

    for alpha in range(0, 256, max(1, 255 // steps)):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(60)
        pygame.time.delay(delay)


def get_levels():
    def safe_listdir(folder):
        try:
            folder_path = os.path.join(os.getcwd(), folder)
            return sorted([f for f in os.listdir(folder_path) if f.endswith(".json")])
        except FileNotFoundError:
            print(f"⚠️ Warning: Folder {folder} not found.")
            return []

    # Nové: pre Sokoban z JSON-u
    sokoban_path = os.path.join(os.getcwd(), "lvls", "sokoban", "sokoban_levels.json")
    try:
        with open(sokoban_path, "r") as f:
            data = json.load(f)
            sokoban_levels = [f"lvl{i+1}" for i in range(len(data["levels"]))]
    except Exception as e:
        print("Sokoban JSON load error:", e)
        sokoban_levels = []

    return {
        "Sokoban": sokoban_levels,
        "Platformer": safe_listdir("lvls/platformer"),
        "Prototype": safe_listdir("lvls/prototype")
    }


