import pygame
import json
import pymunk
from scripts.entities import *
from lvls.sokoban.sokoban_lvl import maps
from scripts.utils import resource_path


# ─────────────── SOKOBAN MAP LOADER ─────────────── #
class SokobanMapLoader:
    def __init__(self):
        self.level_map = []
        self.target_cords = []

    # Načítanie konkrétnej úrovne zo súboru maps()
    def load(self, level_name):
        self.level_map = getattr(maps(), level_name)
        self.find_targets()

    # Vyhľadanie cieľových pozícií (bodky)
    def find_targets(self):
        self.target_cords = []
        for row_idx, row in enumerate(self.level_map):
            for col_idx, tile in enumerate(row):
                if tile == ".":
                    self.target_cords.append((row_idx, col_idx))

    def get_map(self):
        return self.level_map

    def get_target(self):
        return self.target_cords


# ─────────────── SPOLOČNÉ PRE PLATFORMER A PROTOTYPE ─────────────── #
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1),
                    (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

PHYSICS_TILES = {'grass', 'stone'}
PHYSICS_OBJECTS = {'boxes'}

# Základný loader – načítanie dlaždíc, objektov a ich pozícií
class BaseMapLoader:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.objects = {}

    # Získanie susedných dlaždíc okolo pozície (na kolízie)
    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = f"{tile_loc[0] + offset[0]};{tile_loc[1] + offset[1]}"
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles

    # Načítanie zdieľaných údajov z JSON súboru
    def load_common(self, map_data):
        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data.get('offgrid', [])
        self.objects = map_data.get('objects', {})

    # Príprava dát na uloženie do JSON súboru
    def save_common(self):
        return {
            'tilemap': self.tilemap,
            'tile_size': self.tile_size,
            'offgrid': self.offgrid_tiles,
            'objects': self.objects
        }

    # Vykreslenie všetkých dlaždíc na plochu
    def render_tiles(self, surf):
        for loc, tile in self.tilemap.items():
            surf.blit(self.game.assets[tile["type"]][tile["variant"]],
                      (tile["pos"][0] * self.tile_size, tile["pos"][1] * self.tile_size))
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile["type"]][tile["variant"]],
                      tile["pos"])

    # Získanie všetkých obdlžníkov pevných dlaždíc pre kolízie
    def get_all_physics_rects(self):
        return [
            pygame.Rect(tile['pos'][0] * self.tile_size,
                        tile['pos'][1] * self.tile_size,
                        self.tile_size, self.tile_size)
            for tile in self.tilemap.values()
            if tile['type'] in PHYSICS_TILES
        ]

    # Získanie kolíznych rectov len okolo konkrétnej pozície
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(tile['pos'][0] * self.tile_size,
                                tile['pos'][1] * self.tile_size,
                                self.tile_size, self.tile_size)
                )
        return rects


# ─────────────── PLATFORMER MAP LOADER ─────────────── #
class PlatformerMapLoader(BaseMapLoader):
    def __init__(self, game, tile_size=16):
        super().__init__(game, tile_size)
        self.doors = []
        self.buttons = []

    # Načítanie mapy a inicializácia dverí a tlačidiel
    def load(self, path):
        with open(resource_path('lvls/' + path), 'r') as f:
            map_data = json.load(f)
        self.load_common(map_data)

        self.doors = []
        self.buttons = []

        for door in self.objects.get('doors', []):
            self.doors.append(Door(door['x'], door['y'], self.tile_size, tuple(door['color'])))

        for button in self.objects.get('buttons', []):
            self.buttons.append(Button(button['x'], button['y'], self.tile_size, tuple(button['color'])))

    # Uloženie mapy do JSON súboru
    def save(self, path):
        with open(resource_path(path), 'w') as f:
            json.dump(self.save_common(), f)

    # Vykreslenie mapy vrátane objektov
    def render(self, surf):
        self.render_tiles(surf)
        for door in self.doors:
            door.render(surf)
        for button in self.buttons:
            button.render(surf)

    # Vykreslenie farebných placeholderov v editore
    def render_placeholders(self, surf):
        for button in self.objects.get("buttons", []):
            pygame.draw.rect(surf, (255, 0, 0),
                             (button["x"] * self.tile_size, button["y"] * self.tile_size,
                              self.tile_size, self.tile_size))
        for door in self.objects.get("doors", []):
            pygame.draw.rect(surf, (0, 0, 255),
                             (door["x"] * self.tile_size, door["y"] * self.tile_size,
                              self.tile_size, self.tile_size))

        if "finish" in self.objects:
            finishes = self.objects["finish"]
            if isinstance(finishes, dict):
                finishes = [finishes]
            for finish in finishes:
                pygame.draw.rect(surf, (0, 255, 0),
                                 (finish["x"] * self.tile_size, finish["y"] * self.tile_size,
                                  self.tile_size, self.tile_size))

        for player_key, color in [("P1", (255, 255, 0)), ("P2", (0, 255, 255))]:
            if self.objects.get(player_key):
                pos = self.objects[player_key]
                pygame.draw.rect(surf, color,
                                 (pos["x"] * self.tile_size, pos["y"] * self.tile_size,
                                  self.tile_size, self.tile_size))


# ─────────────── PROTOTYPE MAP LOADER (rozšírenie Platformer loadera) ─────────────── #
class PrototypeMapLoader(PlatformerMapLoader):
    def __init__(self, game, tile_size=16):
        super().__init__(game, tile_size)
        self.physics_objects = []

    # Načítanie dát z JSON vrátane physics_objects
    def load(self, path):
        with open(resource_path('lvls/' + path), 'r') as f:
            map_data = json.load(f)
        self.physics_objects = map_data.get('physics_objects', [])
        self.load_common(map_data)

    # Uloženie mapy + physics_objects do súboru
    def save(self, path):
        for key in ["buttons", "doors", "finish", "P1", "P2"]:
            if key not in self.objects:
                self.objects[key] = [] if key in ["buttons", "doors", "finish"] else {}

        with open(resource_path(path), 'w') as f:
            json.dump({
                **self.save_common(),
                'physics_objects': [tile for tile in self.tilemap.values() if tile['type'] in PHYSICS_OBJECTS]
            }, f)

    # Vytvorenie pevných kolíznych objektov (dynamické dlaždice typu grass/stone)
    def create_static_collision(self, space):
        for tile in self.tilemap.values():
            if tile["type"] in PHYSICS_TILES:
                x, y = tile["pos"]
                px = x * self.tile_size * 2
                py = y * self.tile_size * 2

                body = pymunk.Body(body_type=pymunk.Body.STATIC)
                body.position = (px, py)

                shape = pymunk.Poly.create_box(body, (self.tile_size, self.tile_size))
                shape.friction = 1.0
                space.add(body, shape)

    # Načítanie pohyblivých objektov (napr. boxy)
    def create_dynamic_objects(self):
        for tile in self.tilemap.values():
            if tile["type"] == "boxes":
                x, y = tile["pos"]
                box = BoxEntity(self.game, x * 2, y * 2)
                self.game.dynamic_objects.append(box)

    # Vykreslenie mapy (boxy sa nevykresľujú tu – robí to entita)
    def render(self, surf):
        for tile in self.tilemap.values():
            if tile["type"] != "boxes":
                x, y = tile["pos"]
                surf.blit(self.game.assets[tile["type"]][tile["variant"]],
                          (x * self.tile_size, y * self.tile_size))

    # Editorový render – zobrazí aj boxy
    def render_editor(self, surf):
        for tile in self.tilemap.values():
            x, y = tile["pos"]
            surf.blit(self.game.assets[tile["type"]][tile["variant"]],
                      (x * self.tile_size, y * self.tile_size))
