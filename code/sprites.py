from utils import *
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, game, groups, pos):
        self.game = game
        super().__init__(groups)
        self.image = pygame.Surface((30, 30))
        self.image.fill('blue')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED

    def update(self, dt):
        self.get_input()
        self.apply_movement(dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()

        # --- movement ---
        self.direction.x = int(keys[KEY_BINDINGS["move_right"]]) - int(keys[KEY_BINDINGS["move_left"]])
        self.direction.y = int(keys[KEY_BINDINGS["move_down"]]) - int(keys[KEY_BINDINGS["move_up"]])

        # --- slow down ---
        self.speed = PLAYER_SLOWED_SPEED if keys[KEY_BINDINGS["slow_down"]] else PLAYER_SPEED

    def apply_movement(self, dt):
        if self.game.hit_time and self.game.runtime - self.game.hit_time < UNMOVABLE_AFTER_HIT_TIME:
            return
        else: 
            self.game.hit_time = 0
        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += dt * self.speed * self.direction
    
class Object(pygame.sprite.Sprite):
    def __init__(self, groups, color, size, anchor, pos):
        super().__init__(groups)
        self.image = pygame.Surface(size, pygame.SRCALPHA).convert_alpha()
        self.image.fill(color)
        self.mask = pygame.mask.from_surface(self.image)
        match anchor:
            case 'center':
                self.rect = self.image.get_rect(center=pos)
            case 'topleft':
                self.rect = self.image.get_rect(topleft=pos)
            case 'midleft':
                self.rect = self.image.get_rect(midleft=pos)
            case 'bottomleft':
                self.rect = self.image.get_rect(bottomleft=pos)
            case 'midbottom':
                self.rect = self.image.get_rect(midbottom=pos)
            case 'bottomright':
                self.rect = self.image.get_rect(bottomright=pos)
            case 'midright':
                self.rect = self.image.get_rect(midright=pos)
            case 'topright':
                self.rect = self.image.get_rect(topright=pos)
            case 'midtop':
                self.rect = self.image.get_rect(midtop=pos)

class Obstacle(Object):
    def __init__(self, game, color, size, anchor, pos):
        self.game = game
        groups = (self.game.all_sprites, self.game.obstacle_sprites)
        super().__init__(groups, color, size, anchor, pos)

class RotatingObstacle(Object):
    def __init__(self, game, color, size, anchor, pos, start_rotation=0, rotation_speed=100):
        self.game = game
        groups = (self.game.all_sprites, self.game.obstacle_sprites)
        super().__init__(groups, color, size, anchor, pos)
        self.rotation_speed = rotation_speed
        self.original_image = self.image.copy()
        self.angle = start_rotation
        self._center = self.rect.center

    def update(self, dt):
        self.angle = (self.angle + self.rotation_speed * dt) % 360
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self._center)
        self.mask = pygame.mask.from_surface(self.image)

class HorizontalMovingObstacle(Object):
    def __init__(self, game, color, size, anchor, pos, move_range, speed):
        self.game = game
        groups = (self.game.all_sprites, self.game.obstacle_sprites)
        super().__init__(groups, color, size, anchor, pos)
        self.start_x = self.rect.x
        self.move_range = move_range
        self.speed = speed
        self.direction = 1  # 1: right, -1: left

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt
        if self.rect.x < self.start_x:
            self.rect.x = self.start_x
            self.direction = 1
        elif self.rect.x > self.start_x + self.move_range:
            self.rect.x = self.start_x + self.move_range
            self.direction = -1

class VerticalMovingObstacle(Object):
    def __init__(self, game, color, size, anchor, pos, move_range, speed=150):
        self.game = game
        groups = (self.game.all_sprites, self.game.obstacle_sprites)
        super().__init__(groups, color, size, anchor, pos)
        self.start_y = self.rect.y
        self.move_range = move_range
        self.speed = speed
        self.direction = 1
        self.hight = size[1]

    def update(self, dt):
        self.rect.y += self.direction * self.speed * dt
        if self.rect.y < self.start_y:
            self.rect.y = self.start_y
            self.direction = 1
        elif self.rect.y > self.start_y + self.move_range:
            self.rect.y = self.start_y + self.move_range
            self.direction = -1
        if self.rect.y > WINDOW_HEIGHT+self.hight:
            self.rect.y = -self.hight

class HealingItem(Object):
    def __init__(self, game, size, anchor, pos):
        self.game = game
        groups = (self.game.all_sprites, self.game.healing_sprites)
        color = (0, 255, 0)
        super().__init__(groups, color, size, anchor, pos)
        self.base_y = self.rect.y

    def update(self, dt):
        # slowly move up and down
        t = perf_counter()
        self.rect.y = self.base_y + abs(int(sin(t * 2) * 6))

class Goal(Object):
    def __init__(self, game, size, anchor, pos):
        self.game = game
        groups = (self.game.all_sprites, self.game.goal_sprites)
        color = (255, 215, 0)
        super().__init__(groups, color, size, anchor, pos)