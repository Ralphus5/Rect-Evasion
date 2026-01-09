from utils import *
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, game, groups, pos):
        self.game = game
        super().__init__(groups)
        self.image = pygame.Surface((30, 30))
        self.image.fill('blue')
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

    def apply_movement(self, dt):
        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()
        self.rect.center += dt * self.speed * self.direction
    
class Object(pygame.sprite.Sprite):
    def __init__(self, groups, color, size, anchor, pos):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill(color)
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

class HealingItem(Object):
    def __init__(self, game, size, anchor, pos):
        self.game = game
        groups = (self.game.all_sprites, self.game.healing_sprites)
        color = (0, 255, 0)
        super().__init__(groups, color, size, anchor, pos)

class Goal(Object):
    def __init__(self, game, size, anchor, pos):
        self.game = game
        groups = (self.game.all_sprites, self.game.goal_sprites)
        color = (255, 215, 0)
        super().__init__(groups, color, size, anchor, pos)