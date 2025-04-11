import pygame
import sys, os
from scripts.mapLoader import PlatformerMapLoader
from scripts.players import PlatformerPlayer
from scripts.entities import Finish, Button, Door
from scripts.utils import load_image, load_images, fade_transition
from scripts.ui import HUD
from scripts.level_state import mark_level_completed


class Platformer_Game:
    def __init__(self,level_index=0):
        # Inicializácia hry (obrazovka, assets, načítanie levelu, hráči, objekty, HUD)
        pygame.init()
        pygame.display.set_caption("Platformer")
        self.screen = pygame.display.set_mode((1200, 800)) 
        self.display = pygame.Surface((600, 400))
        self.clock = pygame.Clock()
        self.render_scale = 2
        self.level_index = level_index
        self.levels = sorted([f for f in os.listdir("lvls/platformer") if f.endswith(".json")])
        self.level_id = self.levels[level_index]
        self.level_label = f"Level {level_index + 1}"
        pygame.display.set_mode((1200, 800), flags=pygame.SCALED, vsync=1)
        self.running = True



        # Načítanie assets
        self.assets = {
            'stone': load_images('tiles/stone'),
            'grass': load_images('tiles/grass'),
            "player1": load_image("character/idle/player_green.png"),
            "player2": load_image("character/idle/player_red.png")
        }

        print(self.assets)

        # Načítanie tilemap and objects
        self.tilemap = PlatformerMapLoader(self)
        self.tilemap.load(f"platformer/{self.level_id}")

        # Načítanie hráčov zo súboru – ak chýbajú, vytvoria sa na pozícii (0, 0)
        p1_data = self.tilemap.objects.get("P1")
        p2_data = self.tilemap.objects.get("P2")

        if p1_data:
            self.player1 = PlatformerPlayer(self, "P1", (p1_data["x"] * self.tilemap.tile_size, p1_data["y"] * self.tilemap.tile_size), (14, 16), color='red')
        else:
            print("⚠ Warning: P1 not defined in map!")
            self.player1 = PlatformerPlayer(self, "P1", (0, 0), (14, 16))

        if p2_data:
            self.player2 = PlatformerPlayer(self, "P2", (p2_data["x"] * self.tilemap.tile_size, p2_data["y"] * self.tilemap.tile_size), (14, 16), color='green')
        else:
            print("⚠ Warning: P2 not defined in map!")
            self.player2 = PlatformerPlayer(self, "P2", (0, 0), (14, 16))

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


        # Načítanie tlačidiel a dverí z JSON súboru

        self.buttons = []
        for b in self.tilemap.objects.get("buttons", []):
            self.buttons.append(Button(b["x"], b["y"], self.tilemap.tile_size, tuple(b["color"])))

        self.doors = []
        for d in self.tilemap.objects.get("doors", []):
            self.doors.append(Door(d["x"], d["y"], self.tilemap.tile_size, color=tuple(d["color"])))

        # HUD
        self.hud = HUD(self, self.level_label)

    # Reštart aktuálneho levelu – spustí znova rovnakú úroveň
    def restart_level(self):
        print("Restarting level...")
        new_game = Platformer_Game(level_index=self.level_index)
        new_game.run()
        self.running = False

    # Načíta ďalší level, ak existuje, inak ukončí hru
    def load_next_level(self):
        next_index = self.level_index + 1
        if next_index < len(self.levels):
            fade_transition(self.screen, self.clock, show_level_complete_message=True)

            # Spusti ďalší level
            Platformer_Game(level_index=next_index).run()

            # Ukonči aktuálny loop
            self.running = False
        else:
            print("🎉 All platformer levels complete!")
            self.running = False






    

    # Hlavný herný cyklus (vykresľovanie, vstupy, logika tlačidiel, výhra)
    def run(self):
        """Main game loop."""
        while self.running:
            self.display.fill((100, 149, 237))  # Pozadie

            # Vykresľovanie tiles
            self.tilemap.render(self.display)

            # Update logic
            self.handle_events()
            keys = pygame.key.get_pressed()

            self.player1.update(self.tilemap, movement=(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], 0), other_player=self.player2)
            self.player2.update(self.tilemap, movement=(keys[pygame.K_d] - keys[pygame.K_a], 0), other_player=self.player1)

            for door in self.doors:
                # Dvere sa zavrú, ak na nich práve nikto nestojí

                if not (door.is_player_inside(self.player1) or door.is_player_inside(self.player2)):
                    door.opened = False
                else:
                    door.opened = True   



            # Check buttons
            for button in self.buttons:
                button.activated = False
                # Overenie, či niektorý hráč aktivuje tlačidlo – otvorí priradené dvere
                button.check_activation(self.player1, self.doors)
                button.check_activation(self.player2, self.doors)



            # Ak obaja hráči stoja na finish dlaždiciach, spustí sa ďalší level
            for finish in self.finish_tiles:
                if finish.check_players(self.player1, self.player2):
                    mark_level_completed("Platformer", self.level_label, self.level_id)
                    self.load_next_level()
                    break



            # Render players
            self.player1.render(self.display)
            self.player2.render(self.display)

            # Render finish, buttons, doors
            for finish in self.finish_tiles:
                finish.render(self.display)

            for button in self.buttons:
                button.render(self.display)
            for door in self.doors:
                door.render(self.display)

            # Scale a show display
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.hud.render(self.screen)
            pygame.display.update()
            self.clock.tick(60)
            print("FPS:", self.clock.get_fps())

    # Spracovanie používateľských vstupov (skok, reštart, návrat do menu)
    def handle_events(self):
        """Handles user input (quit event, jumping)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:    # Player 1 jump
                    self.player1.jump()
                elif event.key == pygame.K_w:    # Player 2 jump
                    self.player2.jump()
                elif event.key == pygame.K_r:    # Restart level
                    self.restart_level()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

# Run the game
if __name__ == "__main__":
    game = Platformer_Game()
    game.run()
