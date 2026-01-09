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
