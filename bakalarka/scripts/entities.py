import pygame
import pymunk

# Nepoužíva sa (rezerva pre všeobecné entity)
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement=(0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        self.pos[0] += frame_movement[0]
        self.pos[1] += frame_movement[1]

    def render(self, surf):
        surf.blit(self.game.assets['Player'], self.pos)


# Objekt: Finish
# Používa sa v: Platformer, Prototype
class Finish:
    def __init__(self, x, y, tile_size):
        self.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size * 2, tile_size * 2)
        self.players_inside = set()

    def check_players(self, player1, player2):
        if self.rect.colliderect(player1.rect()):
            self.players_inside.add(player1.type)
        else:
            self.players_inside.discard(player1.type)

        if self.rect.colliderect(player2.rect()):
            self.players_inside.add(player2.type)
        else:
            self.players_inside.discard(player2.type)

        if len(self.players_inside) == 2:
            print("Level Complete!")
            return True
        return False

    def render(self, surface):
        finish_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        finish_surface.fill((0, 255, 0, 150))
        surface.blit(finish_surface, (self.rect.x, self.rect.y))


# Objekt: Button
# Používa sa v: Platformer
class Button:
    def __init__(self, x, y, tile_size, color):
        self.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        self.activated = False
        self.color = color

    def check_activation(self, player, all_doors):
        if self.rect.colliderect(player.rect()):
            self.activated = True
            for door in all_doors:
                if door.color == self.color:
                    door.open()

    def render(self, surf):
        color = self.color if self.activated else (100, 100, 100)
        pygame.draw.rect(surf, color, self.rect)


# Objekt: Door
# Používa sa v: Platformer
class Door:
    def __init__(self, x, y, tile_size, color):
        self.rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        self.opened = False
        self.color = color

    def open(self):
        self.opened = True

    def render(self, surf):
        if not self.opened:
            pygame.draw.rect(surf, self.color, self.rect)

    def is_player_inside(self, player):
        return self.rect.colliderect(player.rect())


# Objekt: BoxEntity
# Používa sa v: Prototype
class BoxEntity:
    def __init__(self, game, x, y):
        self.game = game
        self.spawn_x = x * game.tilemap.tile_size
        self.spawn_y = y * game.tilemap.tile_size
        self.in_finish = False  # nový stav



        print(f"📦 Spawning BoxEntity at: ({self.spawn_x}, {self.spawn_y})")

        self.body = pymunk.Body(mass=2, moment=pymunk.moment_for_box(1, (game.tilemap.tile_size, game.tilemap.tile_size)))
        self.body.position = (self.spawn_x, self.spawn_y)
        self.body.velocity_func = self.prevent_tunneling

        self.shape = pymunk.Poly.create_box(self.body, (game.tilemap.tile_size, game.tilemap.tile_size))
        self.shape.friction = 1
        self.shape.elasticity = 0.0

        game.space.add(self.body, self.shape)

    def render(self, surf):
        x, y = self.body.position
        x = int(x / self.game.render_scale)
        y = int(y / self.game.render_scale)

        angle = self.body.angle
        size = self.game.tilemap.tile_size

        box_surface = pygame.Surface((size, size), pygame.SRCALPHA)

        color = (255, 215, 0) if self.in_finish else (139, 69, 19)
        pygame.draw.rect(box_surface, color, (0, 0, size, size))

        rotated_surface = pygame.transform.rotate(box_surface, -angle * 57.2958)
        rotated_rect = rotated_surface.get_rect(center=(x, y))

        surf.blit(rotated_surface, rotated_rect.topleft)

        self.update()


    def check_bounds(self):
        screen_width, screen_height = self.game.screen.get_size()
        if self.body.position.y > screen_height * 2:
            print(f"🔄 Respawning box at ({self.spawn_x}, {self.spawn_y})")
            self.body.position = (self.spawn_x, self.spawn_y)
            self.body.velocity = (0, 0)

    def update_finish_state(self, finish_rects):
        half = self.game.tilemap.tile_size // 2
        box_x = int(self.body.position.x / self.game.render_scale) - half
        box_y = int(self.body.position.y / self.game.render_scale) - half
        box_rect = pygame.Rect(box_x, box_y, self.game.tilemap.tile_size, self.game.tilemap.tile_size)

        self.in_finish = any(finish_rect.colliderect(box_rect) for finish_rect in finish_rects)


    
    def set_in_finish(self, value: bool):
        self.in_finish = value

    def prevent_tunneling(self, body, gravity, damping, dt):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        max_velocity = 800
        if body.velocity.length > max_velocity:
            body.velocity = body.velocity.normalized() * max_velocity

    def update(self):
        self.check_bounds()


# Objekt: ObjectManager
# Používa sa v: Editor (iba editor)
class ObjectManager:
    def __init__(self, editor):
        self.editor = editor
        self.objects = {"players": [], "finish": None, "buttons": [], "doors": []}
        self.selected_object = "finish"

    def place_object(self, obj_type, pos):
        if obj_type == "finish":
            self.objects["finish"] = {"x": pos[0], "y": pos[1]}
        elif obj_type == "players":
            self.objects["players"].append({"id": f"P{len(self.objects['players'])+1}", "x": pos[0], "y": pos[1]})
        elif obj_type == "buttons":
            self.objects["buttons"].append({"x": pos[0], "y": pos[1], "linked_door": None, "color": [255, 0, 0]})
        elif obj_type == "doors":
            self.objects["doors"].append({"id": f"door{len(self.objects['doors'])+1}", "x": pos[0], "y": pos[1], "color": [0, 0, 255]})

    def remove_object(self, pos):
        for obj_type in self.objects:
            if isinstance(self.objects[obj_type], list):
                self.objects[obj_type] = [obj for obj in self.objects[obj_type] if not (obj["x"] == pos[0] and obj["y"] == pos[1])]
            elif self.objects[obj_type] and self.objects[obj_type]["x"] == pos[0] and self.objects[obj_type]["y"] == pos[1]:
                self.objects[obj_type] = None

    def render_preview(self, surface, pos, tile_size):
        preview_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        preview_surface.fill((255, 255, 255, 100))
        surface.blit(preview_surface, (pos[0] * tile_size, pos[1] * tile_size))

    def render_objects(self, surface, tile_size):
        for obj in self.objects["players"]:
            pygame.draw.rect(surface, (0, 0, 255), (obj["x"] * tile_size, obj["y"] * tile_size, tile_size, tile_size))
        for obj in self.objects["buttons"]:
            pygame.draw.rect(surface, (255, 0, 0), (obj["x"] * tile_size, obj["y"] * tile_size, tile_size, tile_size))
        for obj in self.objects["doors"]:
            pygame.draw.rect(surface, (0, 255, 255), (obj["x"] * tile_size, obj["y"] * tile_size, tile_size, tile_size))
        if self.objects["finish"]:
            pygame.draw.rect(surface, (0, 255, 0), (self.objects["finish"]["x"] * tile_size, self.objects["finish"]["y"] * tile_size, tile_size, tile_size))
