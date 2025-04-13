import pygame
import pymunk
import pymunk.pygame_util
import sys, os
from scripts.mapLoader import PrototypeMapLoader
from scripts.players import PrototypePlayer
from scripts.entities import BoxEntity, Finish
from scripts.utils import load_image, load_images, fade_transition
from scripts.ui import HUD
from scripts.level_state import mark_level_completed

class Prototype_Game:
    def __init__(self,level_index = 0):
        # Inicializácia hry (nastavenie okna, načítanie assetov, levelu, hráčov a objektov)
        pygame.init()
        pygame.display.set_caption("Prototype Mode")

        self.screen = pygame.display.set_mode((1200, 800))
        self.display = pygame.Surface((600, 400))
        self.render_scale = 2
        self.clock = pygame.time.Clock()
        self.level_index = level_index
        self.levels = sorted([f for f in os.listdir("lvls/prototype") if f.endswith(".json")])
        self.level_id = self.levels[level_index]
        self.level_label = f"Level {level_index + 1}"
        


        # Načítanie assetov pre dlaždice a boxy
        self.assets = {
            'stone': load_images('tiles/stone'),
            'grass': load_images('tiles/grass'),
            'boxes': load_images('tiles/boxes'),
        }

        # Inicializácia fyziky pomocou Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.space.iterations = 30  # ⬅️ more accurate collision resolution
        self.space.collision_slop = 0.1
        self.space.collision_bias = pow(1.0 - 0.1, 60.0)

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)

        # Načítanie mapy a vytvorenie kolízií a objektov podľa mapy
        self.tilemap = PrototypeMapLoader(self)
        self.tilemap.load(f"lvls/prototype/{self.level_id}")
        self.dynamic_objects = []
        self.tilemap.create_static_collision(self.space)
        self.tilemap.create_dynamic_objects()
        self.half = self.tilemap.tile_size // 2

        # Inicializácia hráčov
        self.player1 = PrototypePlayer(self, 300, 400, "red", {
            'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d
        }, rotate=True)

        self.player2 = PrototypePlayer(self, 600, 400, "green", {
            'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT
        }, rotate=False)

        # Načítanie cieľových polí (finish) – môže byť jeden alebo viac
        self.finish_tiles = []
        finish_data = self.tilemap.objects.get("finish")
        if isinstance(finish_data, dict):
            self.finish_tiles.append(Finish(finish_data["x"], finish_data["y"], self.tilemap.tile_size))
        elif isinstance(finish_data, list):
            for f in finish_data:
                self.finish_tiles.append(Finish(f["x"], f["y"], self.tilemap.tile_size))
        else:
            print("⚠ Warning: Finish not defined!")

        # Inicializácia HUD
        self.running = True
        self.hud = HUD(self, self.level_label)

    # Spracovanie vstupov pre oboch hráčov
    def handle_input(self):
        self.player1.handle_input()
        self.player2.handle_input()

    # Kontrola výhry – všetky boxy musia byť na cieľových pozíciách
    def check_win(self):
        finish_rects = [f.rect for f in self.finish_tiles]

        boxes_in_finish = 0
        for box in self.dynamic_objects:
            box_rect = pygame.Rect(
                int(box.body.position.x / self.render_scale) - self.half,
                int(box.body.position.y / self.render_scale) - self.half,
                self.tilemap.tile_size,
                self.tilemap.tile_size
            )
            if any(finish_rect.colliderect(box_rect) for finish_rect in finish_rects):
                if box.in_finish and abs(box.body.velocity.y) < 5:
                    boxes_in_finish += 1


        if boxes_in_finish == len(self.dynamic_objects):
            print("✅ Level Complete!")
            mark_level_completed("Prototype", self.level_label, self.level_id)
            self.load_next_level()

    
    # Načíta ďalší level, ak existuje, inak ukončí hru
    def load_next_level(self):
        next_index = self.level_index + 1
        if next_index < len(self.levels):
            fade_transition(self.screen, self.clock, show_level_complete_message=True)
            self.next_level = next_index  # ← toto je dôležité
        else:
            print("🎉 All prototype levels complete!")
        self.running = False



    # Reštart aktuálneho levelu
    def restart_level(self):
        print("Restarting level...")
        self.restart = True
        self.running = False
    # Hlavný herný cyklus
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:    # Reštart levelu
                        self.restart_level()

            self.handle_input()
            self.space.step(1 / 60)  # Aktualizácia fyziky

            self.display.fill((50, 50, 150))  # Pozadie
            self.tilemap.render(self.display)

            # Vykreslenie finish polí
            for f in self.finish_tiles:
                f.render(self.display)

            # Vykreslenie boxov
            finish_rects = [f.rect for f in self.finish_tiles]
            for box in self.dynamic_objects:
                box.update_finish_state(finish_rects)

            for box in self.dynamic_objects:
                box.render(self.display)

            # Vykreslenie hráčov
            self.player1.render(self.display)
            self.player2.render(self.display)

            # Overenie výhernej podmienky
            self.check_win()

            # Zobrazenie a škálovanie displeja
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.hud.render(self.screen)
            pygame.display.update()
            self.clock.tick(60)

        if hasattr(self, "next_level"):
            Prototype_Game(level_index=self.next_level).run()
        elif hasattr(self, "restart"):
            Prototype_Game(level_index=self.level_index).run()




# Spustenie hry
if __name__ == "__main__":
    game = Prototype_Game()
    game.run()
