from imports import *


# --- VISUALS ---
# display
GAME_NAME: str = "Rectangle Evasion"
WINDOW_WIDTH: int = 1280 
WINDOW_HEIGHT: int = 720
WINDOW_CENTER = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
BASE_RESOLUTION = (WINDOW_WIDTH, WINDOW_HEIGHT)
FPS: Annotated[int, (25-120)] = 60

COLOR: dict = {'start_screen_bg': "#440083",
               'gameplay_bg': "#000000",
               'game_over_bg': "#1B0000",
               'stats_text': "#FFFFFF",
               'publisher': "#0066FF",
               'start_hint': "#D50303",
               'game_over_hint': "#FF0000",
               'title': "#00EAFF",
               'game_over': "#FF0000"}

STATS_TEXT_FONT_SIZE: int = 25
PUBLISHER_FONT_SIZE: int = 25
HINT_FONT_SITZE: int = 25
TITLE_FONT_SIZE: int = 100
GAME_OVER_FONT_SIZE: int = 100


# --- AUDIO ---
# sound effect volumes
HIT_SOUND_VOLUME: Annotated[float, (0.0-1.0)] = 1.0
DEATH_SOUND_VOLUME: Annotated[float, (0.0-1.0)] = 1.0
REACH_GOAL_SOUND_VOLUME: Annotated[float, (0.0-1.0)] = 1.0


# --- Gameplay ---
PLAYER_HEALTH: int = 3
PLAYER_SPEED: Annotated[float, (50.0-1000.0)] = 550.0


# --- DEFAULT KEY BINDINGS ---
KEY_BINDINGS: dict[str:int] = {'move_left': pygame.K_a,
                               'move_right': pygame.K_d,
                               'move_up': pygame.K_w,
                               'move_down': pygame.K_s,
                               'fullscreen': pygame.K_F11}

