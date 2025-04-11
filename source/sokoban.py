import pygame
import sys, os
from scripts.mapLoader import SokobanMapLoader
from scripts.players import SokobanPlayer
from scripts.utils import load_image , fade_transition
from scripts.ui import HUD
from scripts.level_state import mark_level_completed


class Sokoban_Game:
    def __init__(self,level_index=0):
        # Inicializácia hry (nastavenie okna, assetov, načítanie mapy, hráči, HUD)
        pygame.init()
        pygame.display.set_caption("Sokoban")
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.mode = 'Sokoban'
        self.level_index = level_index

        from lvls.sokoban.skoban_lvl import maps  # Načítanie dostupných levelov
        self.levels = [attr for attr in dir(maps()) if attr.startswith("lvl")]
        self.levels.sort()  # Usporiadanie levelov podľa názvu

        self.level_id = self.levels[level_index]
        self.level_label = f"Level {level_index + 1}"
        self.running = True


        # Načítanie assetov (obrázky pre hráča, box a stenu)
        self.assets = {
            "player1": load_image("character/idle/player_green.png",1.6),
            "player2": load_image("character/idle/player_red.png",1.6),
            "box": load_image("tiles/boxes/box.png",1.6),
            "wall": load_image("tiles/stone/8.png",1.6),
        }

        # Farby pre podlahu a cieľové miesta
        self.colors = {
            "floor": (200, 200, 200),   # Sivá
            "target": (200, 200, 50),   # Žltá
        }

        # Načítanie mapy a cieľových polí
        self.map_loader = SokobanMapLoader()
        self.map_loader.load(self.level_id)
        self.level = self.map_loader.get_map()
        self.target_cords = self.map_loader.get_target()

        # Inicializácia HUD a hráčov
        self.hud = HUD(self, self.level_label)
        self.player1, self.player2 = self.find_players()

    # Vyhľadanie pozícií hráčov v mape a ich inicializácia
    def find_players(self):
        player1 = player2 = None
        for row_idx, row in enumerate(self.level):
            for col_idx, tile in enumerate(row):
                if tile == "P":
                    player1 = SokobanPlayer(self, row_idx, col_idx, "P", self.assets["player1"])
                elif tile == "Q":
                    player2 = SokobanPlayer(self, row_idx, col_idx, "Q", self.assets["player2"])
        return player1, player2

    # Vykreslenie mapy (dlaždice, boxy, cieľové miesta)
    def draw_map(self):
        tile_size = 25
        for row_idx, row in enumerate(self.level):
            for col_idx, tile in enumerate(row):
                pos = (100 + col_idx * tile_size, 100 + row_idx * tile_size)

                if tile == "#":
                    self.screen.blit(self.assets["wall"], pos)
                elif tile == "B":
                    self.screen.blit(self.assets["box"], pos)
                elif tile == ".":
                    pygame.draw.rect(self.screen, self.colors["target"], (*pos, tile_size, tile_size))
                else:
                    pygame.draw.rect(self.screen, self.colors["floor"], (*pos, tile_size, tile_size))

    # Kontrola výhry – všetky cieľové miesta musia byť pokryté boxom
    def check_win(self):
        for row_idx, row in enumerate(self.level):
            for col_idx, tile in enumerate(row):
                if (row_idx, col_idx) in self.target_cords and tile != "B":
                    return False

        # ✅ Zapíš úspešne dokončený level
        mark_level_completed("Sokoban", self.level_label)

        return True


    # Načíta ďalší level, ak existuje, inak ukončí hru
    def load_next_level(self):
        next_index = self.level_index + 1
        if next_index < len(self.levels):
            fade_transition(self.screen, self.clock, show_level_complete_message=True)

            # Spusti ďalší level ako novú inštanciu
            Sokoban_Game(level_index=next_index).run()

            # Ukonči aktuálny level, aby sa nebežal ďalej
            self.running = False
        else:
            print("🎉 All sokoban levels complete!")
            self.running = False


    # Reštart aktuálneho levelu
    def restart_level(self):
        print("Restarting level...")
        new_game = Sokoban_Game(level_index=self.level_index)
        new_game.run()
        self.running = False

    # Spracovanie pohybu hráčov podľa klávesnice
    def handle_input(self):
        keys = pygame.key.get_pressed()

        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        moved = False

        # Ovládanie hráča 1 – šípky
        if keys[pygame.K_UP]:
            self.player1.move(directions["up"], self.level)
            moved = True
        elif keys[pygame.K_DOWN]:
            self.player1.move(directions["down"], self.level)
            moved = True
        elif keys[pygame.K_LEFT]:
            self.player1.move(directions["left"], self.level)
            moved = True
        elif keys[pygame.K_RIGHT]:
            self.player1.move(directions["right"], self.level)
            moved = True

        # Ovládanie hráča 2 – WASD
        if keys[pygame.K_w]:
            self.player2.move(directions["up"], self.level)
            moved = True
        elif keys[pygame.K_s]:
            self.player2.move(directions["down"], self.level)
            moved = True
        elif keys[pygame.K_a]:
            self.player2.move(directions["left"], self.level)
            moved = True
        elif keys[pygame.K_d]:
            self.player2.move(directions["right"], self.level)
            moved = True

        # Debug výpis stavu mapy po pohybe
        if moved:
            self.print_map()

    # Výpis mapy do konzoly pre ladenie
    def print_map(self):
        print("\nCurrent Level State:")
        for row in self.level:
            print("".join(row))
        print("\n" + "-" * 20)

    # Hlavný herný cyklus
    def run(self):
        while self.running:
            self.screen.fill((150, 50, 50))

            self.handle_input()
            self.player1.update()
            self.player2.update()

            self.draw_map()
            self.player1.render(self.screen)
            self.player2.render(self.screen)
            self.hud.render(self.screen)

            if self.check_win():
                print("✅ Level Complete!")
                self.load_next_level()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:    # Reštart levelu
                        self.restart_level()

            pygame.display.update()
            self.clock.tick(60)

# Spustenie hry
if __name__ == "__main__":
    Sokoban_Game().run()
