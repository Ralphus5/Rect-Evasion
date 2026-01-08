from settings import *
import settings

# --- essential game utilities ---
def clear_input():
    """Use this to prevent input from carrying over to the next screen."""

    pygame.event.clear()
    pygame.key.get_pressed()
    pygame.mouse.get_pressed()

def kill_sprites(group, exceptions: tuple = (), space=None):
    for sprite in group:
        if sprite not in exceptions:
            if hasattr(sprite, 'body') and hasattr(sprite, 'shape'):
                space.remove(sprite.body, sprite.shape)
            sprite.kill()

def close_game():
    pygame.quit()
    sys.exit()

def get_scaled_mouse_pos(game):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    scale_x = BASE_RESOLUTION[0] / game.window.get_width()
    scale_y = BASE_RESOLUTION[1] / game.window.get_height()
    return int(mouse_x * scale_x), int(mouse_y * scale_y)

def fade_to_black(game, duration, smoothness):
    """Fade the screen to black over a fixed duration (seconds), with given smoothness."""
    
    bar_width = WINDOW_WIDTH / smoothness
    start_time = perf_counter()

    while True:
        game.clock.tick(FPS)      # keeps dt stable after fade

        elapsed = perf_counter() - start_time
        progress = min(elapsed / duration, 1.0)

        # --- draw progressive black bars ---
        filled = int(progress * smoothness)
        pygame.draw.rect(game.screen, 'black', (0, 0, int(bar_width * filled), WINDOW_HEIGHT))
        present_frame(game)

        if progress >= 1.0:
            break

def present_frame(game):
    window_w, window_h = game.window.get_size()
    scaled = pygame.transform.smoothscale(game.screen, (window_w, window_h))
    game.window.blit(scaled, (0, 0))
    pygame.display.flip()

def toggle_fullscreen(game):
    game.fullscreen = not getattr(game, 'fullscreen', True)
    if game.fullscreen:
        game.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        game.window = pygame.display.set_mode(BASE_RESOLUTION)

# --- randomizers ---
def random_of_spectrum(start: int|float, end: int|float, as_float=False, bias: float=None) -> int|float:
    """Return random number from [start, end].
    - as_float: True → return float, False → return integer
    - bias: if given (0.0–1.0), biases result toward one end
      e.g. bias=0.2 favors start, bias=0.8 favors end"""
    
    if bias is not None:
        value = triangular(start, end, start + (end - start) * bias)
        return value if as_float else int(value)
    return uniform(start, end) if as_float else randint(start, end)

def random_of_selection(selection: Sequence, weights: Optional[Sequence[float]] =None, unique: bool=False) -> Sequence[Any]:
    """Return random element from a collection.
    - weights: optional list of probabilities (must match len(selection))
    - unique: if True, convert to set before choice (removes duplicates)"""

    seq = list(set(selection)) if unique else list(selection)
    if weights:
        return choices(seq, weights=weights, k=1)[0]
    return choice(seq)

# --- time system ---
def update_play_time(game):
    if not game.is_paused and game.play_start is not None:
        game.play_time = perf_counter() - game.play_start - game.total_paused

def pause_play_time(game):
    if not game.is_paused:
        game.pause_start = perf_counter()
        game.is_paused = True

def resume_play_time(game):
    if game.is_paused:
        game.total_paused += perf_counter() - game.pause_start
        game.is_paused = False

# --- UI elements ---
class ClickableIcon:
    """Clickable image button used in the pause menu."""

    def __init__(self, image, pos: tuple, anchor: str = "center", hover_scale_factor: float = 1.1):
        self.base_image = image
        self.rect = image.get_rect()
        setattr(self.rect, anchor, pos)
        self.scale_factor = hover_scale_factor

        self.controller_hovered = False
        self.controller_clicked = False
        self.hovered = False
        self.hover_changed = False
        self.clicked = False

    def update(self, mouse_pos: tuple[float, float], mouse_click: bool):
        prev_hover = self.hovered
        self.hovered = any((self.rect.collidepoint(mouse_pos), self.controller_hovered))
        self.controller_hovered = False if self.rect.collidepoint(mouse_pos) else self.controller_hovered
        self.hover_changed = (self.hovered != prev_hover)
        self.clicked = mouse_click and not self.controller_hovered and self.hovered

    def draw(self, screen):
        scale = self.scale_factor if self.hovered else 1.0
        surf = pygame.transform.rotozoom(self.base_image, 0, scale)
        rect = surf.get_rect(center=self.rect.center)
        screen.blit(surf, rect)

class ClickableText:
    """Clickable text button that changes color when hovered."""

    def __init__(self, text, font, pos, color, hover_color, click_sound=None, hover_sound=None, anchor="center"):
        self.font = font
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.pos = pos
        self.anchor = anchor
        self.click_sound = click_sound
        self.hover_sound = hover_sound

        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        setattr(self.rect, self.anchor, self.pos)

        self.controller_hovered = False
        self.controller_clicked = False
        self.hovered = False
        self.hover_changed = False
        self.clicked = False

    def update(self, mouse_pos, mouse_click):
        prev_hover = self.hovered
        self.hovered = any((self.rect.collidepoint(mouse_pos), self.controller_hovered))
        self.controller_hovered = False if self.rect.collidepoint(mouse_pos) else self.controller_hovered
        self.hover_changed = (self.hovered != prev_hover)

        if self.hover_changed and self.hovered and self.hover_sound:
            self.hover_sound.play()

        color = self.hover_color if self.hovered else self.color
        self.surface = self.font.render(self.text, True, color)

        self.clicked = mouse_click and not self.controller_hovered and self.hovered
        if self.clicked and self.click_sound:
            self.click_sound.play()

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
