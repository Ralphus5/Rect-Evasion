from sprites import *
import settings

class Game:
    def __init__(self):
        self.init_paths()
        self.init_pygame()
        self.init_window()
        self.load_sounds()
        self.set_all_volumes()
        self.load_graphics()
        self.init_sprites()
        self.state = None
        self.requested_state = 'start'
        self.running = True

# --- Game modes ---
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events_and_input()
            self.set_game_mode()
            if self.state == 'start':
                self.start_screen(dt)
            elif self.state == 'play':
                self.play_loop(dt)
            elif self.state == 'stop':
                self.pause_menu(dt)
            elif self.state == 'game_over':
                self.game_over_screen(dt)
            elif self.state == 'settings':
                self.settings_menu(dt)
            present_frame(self)
            self.clock.tick(FPS)

    def handle_events_and_input(self):
        '''Check for user input regarding non-gameplay actions and handling timed events.'''

        for event in pygame.event.get():
        # --- General events ---
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == KEY_BINDINGS['fullscreen']:
                    toggle_fullscreen(self)

        # --- Start state ---
            if self.state == 'start':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.requested_state = 'play'
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else: self.show_start_hint = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.show_start_hint = True

        # --- Play state ---
            elif self.state == 'play':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.requested_state = 'stop'

        # --- Stop state ---
            elif self.state == 'stop':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.requested_state = 'play'

        # --- Game Over state ---
            elif self.state == 'game_over':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.requested_state = 'start'
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    else: self.show_game_over_hint = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.show_game_over_hint

    def set_game_mode(self):
        '''Switches game mode and handles necessary changes.'''

        # check for state change request
        if not self.requested_state or self.requested_state == self.state:
            return
        
        old, new = self.state, self.requested_state
        self.requested_state = None
        self.state = new
        pygame.key.get_pressed()
        clear_input()

        # --- state preparations ---
        if new == 'start':
            pygame.mixer.music.load(join(self.AUDIO_DIR, 'start_track.wav'))
            pygame.mixer.music.play()
            self.init_game_state()

        elif new == 'play':
            if old == 'start':
                pygame.mixer.music.load(join(self.AUDIO_DIR, 'play_track.wav'))
                pygame.mixer.music.play()
            elif old == 'stop':
                pygame.mixer.music.unpause()

        elif new == 'stop':
            pygame.mixer.music.pause()
            
        elif new == 'game_over':
            pygame.mixer.music.load(join(self.AUDIO_DIR, 'game_over_track.wav'))
            pygame.mixer.music.play()
            kill_sprites(self.all_sprites)
            self.level_set_up = False

        elif new == 'settings':
            pass

    def start_screen(self, dt):
        self.screen.fill(COLOR['start_screen_bg'])
        self.screen.blit(self.text_surfaces['title'], self.text_rects['title'])
        if self.show_start_hint:
            self.screen.blit(self.text_surfaces['publisher'], self.text_rects['publisher'])
            self.screen.blit(self.text_surfaces['start_hint'], self.text_rects['start_hint'])

    def play_loop(self, dt):
        self.screen.fill(COLOR['gameplay_bg'])
        match self.level:
            case 1:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (100, WINDOW_CENTER[1])
                    Obstacle(self, (255,0,0), (250, 400), 'center', WINDOW_CENTER)
                    Goal(self, (150, 150), 'midright', (WINDOW_WIDTH, WINDOW_CENTER[1]))
            case 2:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (WINDOW_WIDTH - 100, WINDOW_CENTER[1])
                    Obstacle(self, (255,0,0), (250, 600), 'topright', (WINDOW_WIDTH - 300, 0))
                    Obstacle(self, (255,0,0), (220, 100), 'topright', (300, 300))
                    Obstacle(self, (255,0,0), (150, 200), 'topright', (300, 600))
                    Obstacle(self, (255,0,0), (120, 150), 'topright', (600, 350))
                    Obstacle(self, (255,0,0), (120, 100), 'topright', (550, 600))
                    Obstacle(self, (255,0,0), (200, 200), 'topright', (500, 0))
                    Obstacle(self, (255,0,0), (200, 100), 'topright', (50, 500))
                    Goal(self, (250, 50), 'topleft', (0, 0))
            case 3:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (50, 25)
                    Obstacle(self, (255,0,0), (400, 60), 'topright', (WINDOW_WIDTH, 110))
                    Obstacle(self, (255,0,0), (800, 60), 'topleft', (0, 110))
                    Obstacle(self, (255,0,0), (805, 60), 'topright', (WINDOW_WIDTH, 260))
                    Obstacle(self, (255,0,0), (405, 60), 'topleft', (0, 260))
                    Obstacle(self, (255,0,0), (410, 60), 'topright', (WINDOW_WIDTH, 410))
                    Obstacle(self, (255,0,0), (810, 60), 'topleft', (0, 410))
                    Obstacle(self, (255,0,0), (812, 60), 'topright', (WINDOW_WIDTH, 560))
                    Obstacle(self, (255,0,0), (412, 60), 'topleft', (0, 560))
                    Goal(self, (100,100), 'bottomleft', (0,WINDOW_HEIGHT))
            case 4:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (23, WINDOW_HEIGHT - 50)
                    Obstacle(self, (255,0,0), (150, 400), 'topleft', (0, 0))
                    Obstacle(self, (255,0,0), (150, 400), 'bottomleft', (250, WINDOW_HEIGHT))
                    Obstacle(self, (255,0,0), (150, 400), 'topleft', (470, 0))
                    Obstacle(self, (255,0,0), (150, 400), 'bottomleft', (680, WINDOW_HEIGHT))
                    Obstacle(self, (255,0,0), (150, 400), 'topleft', (880, 0))
                    Goal(self, (100,100), 'midright', (WINDOW_WIDTH, WINDOW_CENTER[1]))
            case 5:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (WINDOW_WIDTH - 60, WINDOW_CENTER[1])

        self.all_sprites.update(dt)
        self.collisions()
        self.all_sprites.draw(self.screen)
        self.render_stats_text()

    def pause_menu(self, dt):
        self.screen.fill(COLOR['gameplay_bg'])
        self.all_sprites.draw(self.screen)
        self.render_stats_text()
        dim = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
        dim.fill((0, 0, 0, 125))
        self.screen.blit(dim, (0, 0))

    def settings_menu(self, dt):
        pass

    def game_over_screen(self, dt):
        self.screen.fill(COLOR['game_over_bg'])
        if self.show_game_over_hint:
            self.screen.blit(self.text_surfaces['game_over_hint'], self.text_rects['game_over_hint'])
        self.screen.blit(self.text_surfaces['game_over'], self.text_rects['game_over'])

# --- Main loop ---
    def collisions(self):
        if not self.player:
            return

        # --- obstacle collisions ---
        hit_obstacle = pygame.sprite.spritecollideany(self.player, self.obstacle_sprites)
        if hit_obstacle:
            self.player.health -= 1
            if self.player.health >= 1:
                self.hit_sound.play()
                self.player.rect.topleft = self.player_start_pos
            else:
                self.death_sound.play()
                self.player.kill()
                self.requested_state = 'game_over'

        # --- goal collisions ---
        hit_goal = pygame.sprite.spritecollideany(self.player, self.goal_sprites)
        if hit_goal:
            self.reach_goal_sound.play()
            self.level += 1
            self.level_set_up = False
            kill_sprites(self.all_sprites, exceptions=self.player_sprites)
            hit_goal.kill()

    def render_stats_text(self):
        self.text_surfaces['stats'] = self.fonts['stats'].render(f"Level: {self.level}    Health: {self.player.health}", True, COLOR['stats_text'])
        self.screen.blit(self.text_surfaces['stats'], self.text_rects['stats'])

# --- Initialization steps ---
    def init_paths(self):
        # --- detect running mode ---
        if getattr(sys, "frozen", False):
            base_dir = sys._MEIPASS
            user_dir = os.path.expanduser(join("~", "Documents", GAME_NAME))
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            user_dir = join(base_dir, "data")

        # --- create save directory if needed ---
        os.makedirs(user_dir, exist_ok=True)

        # --- asset file paths ---
        self.BASE_DIR = base_dir
        self.USER_DIR = user_dir
        self.IMG_DIR = join(base_dir, "assets", "images")
        self.AUDIO_DIR = join(base_dir, "assets", "audio")
        self.FONT_DIR = join(base_dir, "assets", "fonts")
        self.DATA_DIR = join(base_dir, "data")
        self.SAVE_FILE = join(user_dir, "save.json")
        self.SETTINGS_FILE = join(user_dir, "settings.json")

    def init_pygame(self):
        try:
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=256)
        except:
            print("Audio preinit failed. Using defaults.")
        pygame.init()
        pygame.mixer.set_num_channels(128)
        self.clock = pygame.time.Clock()

        # --- initialize controller ---
        pygame.joystick.init()
        self.controller = None
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            print(f"Using {self.controller.get_name()}")

    def init_window(self):
        # --- open window ---
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.Surface(BASE_RESOLUTION).convert_alpha()
        # --- set caption ---
        pygame.display.set_caption(GAME_NAME)
        # --- set icon ---
        icon = pygame.image.load(join(self.IMG_DIR, 'icon.png')).convert_alpha()
        pygame.display.set_icon(icon)

    def load_sounds(self):
        # --- sound effects ---
        self.hit_sound: pygame.mixer.Sound = pygame.mixer.Sound(join(self.AUDIO_DIR, 'hit_sound.wav'))
        self.death_sound: pygame.mixer.Sound = pygame.mixer.Sound(join(self.AUDIO_DIR, 'death_sound.wav'))
        self.reach_goal_sound: pygame.mixer.Sound = pygame.mixer.Sound(join(self.AUDIO_DIR, 'reach_goal_sound.wav'))

    def set_all_volumes(self):
        # --- game music ---
        pygame.mixer.music.set_volume(1)

        # --- sound effects ---
        self.hit_sound.set_volume(HIT_SOUND_VOLUME)
        self.death_sound.set_volume(DEATH_SOUND_VOLUME)
        self.reach_goal_sound.set_volume(REACH_GOAL_SOUND_VOLUME)

    def load_graphics(self):
        self.font_1 = join(self.FONT_DIR,'gomarice_no_continue.ttf')
        self.font_2 = join(self.FONT_DIR,'slkscr.ttf')

        self.fonts = {'stats': pygame.font.Font(self.font_1, STATS_TEXT_FONT_SIZE),
                      'publisher': pygame.font.Font(self.font_2, PUBLISHER_FONT_SIZE),
                      'hint': pygame.font.Font(self.font_2, HINT_FONT_SITZE),
                      'title': pygame.font.Font(self.font_1, TITLE_FONT_SIZE),
                      'game_over': pygame.font.Font(self.font_1, GAME_OVER_FONT_SIZE)}

        self.text_surfaces = {'stats': self.fonts['stats'].render(f"Level: 1 Health: {PLAYER_HEALTH}", True, COLOR['stats_text']),
                              'publisher': self.fonts['publisher'].render("Ralphus Studios", True, COLOR['publisher']),
                              'start_hint': self.fonts['hint'].render("Start game: RETURN\nClose game: ESC", True, COLOR['start_hint']),
                              'game_over_hint': self.fonts['hint'].render("Play again: RETURN\nClose game: ESC", True, COLOR['game_over_hint']),
                              'title': self.fonts['title'].render(GAME_NAME, True, COLOR['title']),
                              'game_over': self.fonts['game_over'].render("GAME OVER", True, COLOR['game_over'])}

        self.text_rects = {'stats': self.text_surfaces['stats'].get_rect(topleft=(10, 10)),
                           'publisher': self.text_surfaces['publisher'].get_rect(bottomright=(WINDOW_WIDTH-10, WINDOW_HEIGHT-10)),
                           'start_hint': self.text_surfaces['start_hint'].get_rect(bottomleft=(10, WINDOW_HEIGHT-10)),
                           'game_over_hint': self.text_surfaces['game_over_hint'].get_rect(bottomleft=(10, WINDOW_HEIGHT-10)),
                           'title': self.text_surfaces['title'].get_rect(center=WINDOW_CENTER),
                           'game_over': self.text_surfaces['game_over'].get_rect(center=WINDOW_CENTER)}

    def init_sprites(self):
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.goal_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()

    def init_game_state(self):
        self.level_set_up = False
        self.level = 4
        self.show_start_hint = False
        self.show_game_over_hint = False
        self.player = Player(self, (self.all_sprites, self.player_sprites), (100, WINDOW_CENTER[1]))

# --- main execution ---
def main():
    game = Game()
    atexit.register(pygame.display.quit)
    atexit.register(pygame.font.quit)
    atexit.register(pygame.mixer.quit)
    atexit.register(pygame.quit)
    game.run()

if __name__ == '__main__':
    main()