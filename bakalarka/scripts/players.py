import pygame
import pymunk

# Hráč pre Sokoban mód (grid-based pohyb)
class SokobanPlayer:
    def __init__(self, game, row, col, symbol, image):
        self.game = game
        self.row = row
        self.col = col
        self.symbol = symbol
        self.target_row, self.target_col = row, col
        self.moving = False

        self.image = image
        self.x = col * 25 + 100
        self.y = row * 25 + 100

    # Plynulý pohyb smerom k cieľovej pozícii
    def update(self):
        if self.moving:
            target_x = self.target_col * 25 + 100
            target_y = self.target_row * 25 + 100
            self.x += (target_x - self.x) * 0.2
            self.y += (target_y - self.y) * 0.2
            if abs(self.x - target_x) < 1 and abs(self.y - target_y) < 1:
                self.x, self.y = target_x, target_y
                self.moving = False

    # Pohyb hráča a interakcia s boxami
    def move(self, direction, level_map):
        if self.moving:
            return

        new_row = self.row + direction[0]
        new_col = self.col + direction[1]

        if level_map[new_row][new_col] in [" ", "."]:
            if (self.row, self.col) in self.game.target_cords:
                level_map[self.row][self.col] = "."
            else:
                level_map[self.row][self.col] = " "

            level_map[new_row][new_col] = self.symbol
            self.target_row, self.target_col = new_row, new_col
            self.moving = True
            self.row, self.col = new_row, new_col

        elif level_map[new_row][new_col] == "B":
            box_new_row = new_row + direction[0]
            box_new_col = new_col + direction[1]

            if level_map[box_new_row][box_new_col] in [" ", "."]:
                if (new_row, new_col) in self.game.target_cords:
                    level_map[new_row][new_col] = "."
                else:
                    level_map[new_row][new_col] = " "

                level_map[box_new_row][box_new_col] = "B"

                if (self.row, self.col) in self.game.target_cords:
                    level_map[self.row][self.col] = "."
                else:
                    level_map[self.row][self.col] = " "

                level_map[new_row][new_col] = self.symbol
                self.target_row, self.target_col = new_row, new_col
                self.moving = True
                self.row, self.col = new_row, new_col

    # Vykreslenie hráča
    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))


# Hráč pre Platformer mód (2D skákačka)
class PlatformerPlayer:
    def __init__(self, game, e_type, pos, size, color = 'white'):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        self.air_time = 0
        self.grounded = True
        self.color = color

    # Návrat rektanglu hráča pre kolízie
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    # Aktualizácia pohybu hráča vrátane kolízií s dlaždicami a iným hráčom
    def update(self, tilemap, movement=(0, 0), other_player=None):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        
        # Horizontálny pohyb a kolízie
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos) + [d.rect for d in self.game.doors if not d.opened]:
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        if other_player and entity_rect.colliderect(other_player.rect()):
            if frame_movement[0] > 0:
                self.pos[0] = other_player.rect().left - self.size[0]
                self.collisions['right'] = True
            if frame_movement[0] < 0:
                self.pos[0] = other_player.rect().right
                self.collisions['left'] = True

        # Vertikálny pohyb a kolízie
        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos) + [d.rect for d in self.game.doors if not d.opened]:
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if other_player and entity_rect.colliderect(other_player.rect()):
            if frame_movement[1] > 0:
                self.pos[1] = other_player.rect().top - self.size[1]
                self.collisions['down'] = True
            if frame_movement[1] < 0:
                self.pos[1] = other_player.rect().bottom
                self.collisions['up'] = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down']:
            self.grounded = True
            self.air_time = 0

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.velocity[1] = min(5, self.velocity[1] + 0.05)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    # Debugovací výkres hitboxu hráča
    def debug_draw_hitbox(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), self.rect(), 2)

    # Vykreslenie hráča
    def render(self, surf):
        if self.color == 'red':
            surf.blit(self.game.assets['player1'], (int(self.pos[0]), int(self.pos[1])))
        elif self.color == 'green':
            surf.blit(self.game.assets['player2'], (int(self.pos[0]), int(self.pos[1])))
        else:
            surf.blit(self.game.assets['player2'], (int(self.pos[0]), int(self.pos[1])))


    # Skok hráča (len ak je na zemi)
    def jump(self):
        if self.grounded:
            self.velocity[1] = -3
            self.grounded = False
            self.air_time = 5


# Hráč pre Prototype mód (ovládaný pomocou fyziky cez Pymunk)
class PrototypePlayer:
    def __init__(self, game, x, y, color, controls, rotate=False):
        self.game = game
        self.controls = controls
        self.color = pygame.Color(color)
        self.rotate = rotate

        # Vytvorenie fyzikálneho tela hráča
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y

        # Segmentový tvar pre kolízie – otočený alebo zrkadlený
        if self.rotate:
            self.shape = pymunk.Segment(self.body, (-20, -20), (20, 20), 8)
        else:
            self.shape = pymunk.Segment(self.body, (-20, 20), (20, -20), 8)

        self.shape.friction = 0.9
        self.shape.color = self.color

        game.space.add(self.body, self.shape)

        self.speed = 300
        print(f"🟥 Player collider from {self.shape.a} to {self.shape.b} (Rotated: {self.rotate})")

    # Ovládanie hráča pomocou klávesnice
    def handle_input(self):
        keys = pygame.key.get_pressed()
        velocity = pymunk.Vec2d(0, 0)

        if keys[self.controls['up']]:
            velocity += (0, -self.speed)
        if keys[self.controls['down']]:
            velocity += (0, self.speed)
        if keys[self.controls['left']]:
            velocity += (-self.speed, 0)
        if keys[self.controls['right']]:
            velocity += (self.speed, 0)

        self.body.velocity = velocity

    # Vykreslenie hráča ako diagonálnej čiary
    def render(self, surf):
        x, y = self.body.position
        x = int(x / self.game.render_scale)
        y = int(y / self.game.render_scale)

        player_surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        if self.rotate:
            start_pos = (0, 0)
            end_pos = (40, 40)
        else:
            start_pos = (0, 40)
            end_pos = (40, 0)

        pygame.draw.line(player_surface, self.color, start_pos, end_pos, 5)

        # Vykreslenie fyzikálneho segmentu pre debugging
        collider_start = (int(self.shape.a.x / self.game.render_scale), int(self.shape.a.y / self.game.render_scale))
        collider_end = (int(self.shape.b.x / self.game.render_scale), int(self.shape.b.y / self.game.render_scale))
        pygame.draw.line(surf, (0, 0, 0), collider_start, collider_end, 2)

        rect = player_surface.get_rect(center=(x, y))
        surf.blit(player_surface, rect.topleft)
