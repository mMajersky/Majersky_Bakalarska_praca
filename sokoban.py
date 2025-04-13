import pygame
import sys, os
import json
from scripts.mapLoader import SokobanMapLoader
from scripts.players import SokobanPlayer
from scripts.utils import load_image , fade_transition, get_levels
from scripts.ui import HUD
from scripts.level_state import mark_level_completed

class Sokoban_Game:
    def __init__(self, level_index=0):
        pygame.init()
        pygame.display.set_caption("Sokoban")
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.mode = 'Sokoban'
        self.level_index = level_index

        # Získanie zoznamu levelov (len na počet, už nepotrebujeme názvy)
        self.levels = get_levels()["Sokoban"]
        self.level_label = f"Level {level_index + 1}"
        self.running = True

        self.assets = {
            "player1": load_image("character/idle/player_green.png", 1.6),
            "player2": load_image("character/idle/player_red.png", 1.6),
            "box": load_image("tiles/boxes/box.png", 1.6),
            "wall": load_image("tiles/stone/8.png", 1.6),
        }

        self.colors = {
            "floor": (200, 200, 200),
            "target": (200, 200, 50),
        }

        self.map_loader = SokobanMapLoader()
        self.map_loader.load(self.level_index)  # teraz podľa indexu
        self.level = self.map_loader.get_map()
        self.target_cords = self.map_loader.get_target()

        self.tile_size = 25
        map_width = len(self.level[0]) * self.tile_size
        map_height = len(self.level) * self.tile_size
        self.offset_x = (1200 - map_width) // 2
        self.offset_y = (800 - map_height) // 2

        self.hud = HUD(self, self.level_label)
        self.player1, self.player2 = self.find_players()

    def find_players(self):
        player1 = player2 = None
        for row_idx, row in enumerate(self.level):
            for col_idx, tile in enumerate(row):
                if tile == "P":
                    player1 = SokobanPlayer(self, row_idx, col_idx, "P", self.assets["player1"])
                elif tile == "Q":
                    player2 = SokobanPlayer(self, row_idx, col_idx, "Q", self.assets["player2"])
        return player1, player2

    def draw_map(self):
        for row_idx, row in enumerate(self.level):
            for col_idx, tile in enumerate(row):
                pos = (self.offset_x + col_idx * self.tile_size, self.offset_y + row_idx * self.tile_size)
                if tile == "#":
                    self.screen.blit(self.assets["wall"], pos)
                elif tile == "B":
                    self.screen.blit(self.assets["box"], pos)
                elif tile == ".":
                    pygame.draw.rect(self.screen, self.colors["target"], (*pos, self.tile_size, self.tile_size))
                else:
                    pygame.draw.rect(self.screen, self.colors["floor"], (*pos, self.tile_size, self.tile_size))

    def check_win(self):
        for row_idx, row in enumerate(self.level):
            for col_idx, tile in enumerate(row):
                if (row_idx, col_idx) in self.target_cords and tile != "B":
                    return False
        mark_level_completed("Sokoban", self.level_label)
        return True

    def load_next_level(self):
        next_index = self.level_index + 1
        if next_index < len(self.levels):
            fade_transition(self.screen, self.clock, show_level_complete_message=True)
            Sokoban_Game(level_index=next_index).run()
            self.running = False
        else:
            print("🎉 All sokoban levels complete!")
            self.running = False

    def restart_level(self):
        print("Restarting level...")
        Sokoban_Game(level_index=self.level_index).run()
        self.running = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }
        moved = False

        if keys[pygame.K_UP]: self.player1.move(directions["up"], self.level); moved = True
        elif keys[pygame.K_DOWN]: self.player1.move(directions["down"], self.level); moved = True
        elif keys[pygame.K_LEFT]: self.player1.move(directions["left"], self.level); moved = True
        elif keys[pygame.K_RIGHT]: self.player1.move(directions["right"], self.level); moved = True

        if keys[pygame.K_w]: self.player2.move(directions["up"], self.level); moved = True
        elif keys[pygame.K_s]: self.player2.move(directions["down"], self.level); moved = True
        elif keys[pygame.K_a]: self.player2.move(directions["left"], self.level); moved = True
        elif keys[pygame.K_d]: self.player2.move(directions["right"], self.level); moved = True

        if moved: self.print_map()

    def print_map(self):
        print("\nCurrent Level State:")
        for row in self.level:
            print("".join(row))
        print("\n" + "-" * 20)

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
                    elif event.key == pygame.K_r:
                        self.restart_level()

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Sokoban_Game().run()
