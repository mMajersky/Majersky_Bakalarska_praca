import pygame
import sys, os
from scripts.mapLoader import PlatformerMapLoader, PrototypeMapLoader
from scripts.ui import HUD_Editor
from scripts.utils import load_image, load_images, resource_path

render_scale = 2

# Editor máp pre Platformer a Prototype módy
class Editor:
    def __init__(self, mode="Platformer", level_path="Pmap_new.json"):
        # Inicializácia okna a displeja
        pygame.init()
        pygame.display.set_caption("Editor")
        self.screen = pygame.display.set_mode((1200, 800))
        self.display = pygame.Surface((600, 400))
        self.clock = pygame.time.Clock()
        self.hud = HUD_Editor(self)
        self.mode = mode
        self.level_path = level_path

        # Dostupné objekty podľa herného módu
        all_objects = {
            "Platformer": ["P1", "P2", "finish", "button", "door"],
            "Prototype": ["finish"],
        }
        self.object_list = all_objects.get(self.mode, [])
        self.object_group = 0

        # Načítanie dlaždicových obrázkov
        self.assets = {
            'stone': load_images('tiles/stone'),
            'grass': load_images('tiles/grass'),
        }
        if mode == "Prototype":
            self.assets['boxes'] = load_images('tiles/boxes')

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        # Stav editora
        self.clicking = False
        self.rightclicking = False
        self.shift = False
        self.ongrid = True
        self.objectMode = False

        # Načítanie mapy podľa módu
        if mode.lower() == "prototype":
            self.tilemap = PrototypeMapLoader(self)
        else:
            self.tilemap = PlatformerMapLoader(self)

        # Pokus o načítanie existujúcej mapy, ak neexistuje, pokračuj bez chyby
        try:
            path = os.path.join("lvls", mode.lower(), level_path)
            self.tilemap.load(path)

        except FileNotFoundError:
            print(f"🟠 New map: {level_path}")

    # Uloženie mapy do súboru
    def savemap(self):
        folder = os.path.join(os.getcwd(), "lvls", self.mode.lower())
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, self.level_path)
        self.tilemap.save(path)
        print(f"💾 Saved map to {path}")


    
    def get_level_index(self):
        levels = sorted([f for f in os.listdir(f"lvls/{self.mode.lower()}") if f.endswith(".json")])
        try:
            return levels.index(self.level_path)
        except ValueError:
            print("⚠️ Level not found in list – using index 0")
            return 0

    # Hlavný editačný cyklus
    def run(self):
        while True:
            self.display.fill((100, 149, 237))

            # Vykreslenie dlaždíc
            if self.mode == "Prototype":
                self.tilemap.render_editor(self.display)
            else:
                self.tilemap.render(self.display)

            self.tilemap.render_placeholders(self.display)

            # Náhľad aktuálnej dlaždice pri myši
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / render_scale, mpos[1] / render_scale)
            tile_pos = (int(mpos[0] // self.tilemap.tile_size), int(mpos[1] // self.tilemap.tile_size))

            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size, tile_pos[1] * self.tilemap.tile_size))
            else:
                self.display.blit(current_tile_img, mpos)

            # Umiestnenie dlaždice ľavým klikom
            if self.clicking and self.ongrid:
                self.tilemap.tilemap[f"{tile_pos[0]};{tile_pos[1]}"] = {
                    'type': self.tile_list[self.tile_group],
                    'variant': self.tile_variant,
                    'pos': tile_pos
                }

            # Vymazanie dlaždice pravým klikom (grid aj off-grid)
            if self.rightclicking:
                tile_key = f"{tile_pos[0]};{tile_pos[1]}"
                self.tilemap.tilemap.pop(tile_key, None)
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0], tile['pos'][1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.handle_events(tile_pos)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.hud.render(self.screen)
            pygame.display.update()
            self.clock.tick(60)

    # Spracovanie vstupov (myš a klávesnica)
    def handle_events(self, tile_pos):
        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0] / render_scale, mpos[1] / render_scale)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Režim vkladania dlaždíc
            if not self.objectMode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({
                                'type': self.tile_list[self.tile_group],
                                'variant': self.tile_variant,
                                'pos': mpos
                            })
                    elif event.button == 3:
                        self.rightclicking = True

                    # Scrollovanie medzi variantami alebo typmi
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        elif event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        elif event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    elif event.button == 3:
                        self.rightclicking = False

            # Režim vkladania objektov (hráči, tlačidlá, dvere)
            if self.objectMode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    obj_type = self.object_list[self.object_group]
                    x, y = tile_pos

                    if event.button == 1:
                        if obj_type in ["P1", "P2"]:
                            self.tilemap.objects[obj_type] = {"x": x, "y": y}
                        elif obj_type == "finish":
                            self.tilemap.objects.setdefault("finish", []).append({"x": x, "y": y})
                        elif obj_type == "button":
                            self.tilemap.objects.setdefault("buttons", []).append({"x": x, "y": y, "color": (255, 0, 0)})
                        elif obj_type == "door":
                            self.tilemap.objects.setdefault("doors", []).append({"x": x, "y": y, "color": (0, 0, 255)})

                    elif event.button == 3:
                        if obj_type in ["P1", "P2"] and obj_type in self.tilemap.objects:
                            del self.tilemap.objects[obj_type]
                        elif obj_type == "finish":
                            self.tilemap.objects["finish"] = [
                                f for f in self.tilemap.objects.get("finish", []) if (f["x"], f["y"]) != (x, y)
                            ]
                        elif obj_type == "button":
                            self.tilemap.objects["buttons"] = [
                                b for b in self.tilemap.objects.get("buttons", []) if (b["x"], b["y"]) != (x, y)
                            ]
                        elif obj_type == "door":
                            self.tilemap.objects["doors"] = [
                                d for d in self.tilemap.objects.get("doors", []) if (d["x"], d["y"]) != (x, y)
                            ]

                # Scrollovanie medzi objektmi
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.object_group = (self.object_group - 1) % len(self.object_list)
                    elif event.button == 5:
                        self.object_group = (self.object_group + 1) % len(self.object_list)
                    print("Selected Object:", self.object_list[self.object_group])

            # Klávesové vstupy
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    self.shift = True
                elif event.key == pygame.K_g:
                    self.ongrid = not self.ongrid
                elif event.key == pygame.K_s:
                    self.savemap()
                elif event.key == pygame.K_o:
                    self.objectMode = not self.objectMode
                    print("Object mode:", self.objectMode)
                elif event.key == pygame.K_h:
                    self.hud.toggle_help()
                elif event.key == pygame.K_p:
                    print("▶️ Launching level...")
                    pygame.quit()
                    if self.mode == "Prototype":
                        from prototype import Prototype_Game
                        Prototype_Game(level_index=self.get_level_index()).run()
                    elif self.mode == "Platformer":
                        from platformer import Platformer_Game
                        Platformer_Game(level_index=self.get_level_index()).run()
                    sys.exit()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    self.shift = False

# Spustenie editora pre konkrétny mód a level
if __name__ == "__main__":
    Editor(mode="Prototype", level_path="Protomap_1.json").run()
