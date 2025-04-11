import pygame
import os 
from scripts.ui import LevelCompleteMessage

# Základná cesta ku všetkým obrázkom
base_img_path = "assets/imgs/"

# Funkcia pre načítanie jedného obrázka s voliteľným zväčšením
def load_image(path, scale=1):
    img = pygame.image.load(base_img_path + path).convert()
    img.set_colorkey((0, 0, 0))  # Nastavenie priehľadnej farby (čierna)
    width, height = img.get_size()
    img = pygame.transform.scale(img, (width * scale, height * scale))
    return img

# Funkcia pre načítanie všetkých obrázkov z daného priečinka ako zoznam
def load_images(path):
    images = []
    for img_name in os.listdir(base_img_path + path):
        images.append(load_image(path + '/' + img_name))
    return images

# v budúcnosti sa sem pridajú skripty na animácie

def fade_transition(screen, clock, duration=2500, steps=30, color=(0, 0, 0), show_level_complete_message=False):
    """
    Prechodová animácia so zatmievaním a voliteľnou správou "Level Completed!"
    """
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
