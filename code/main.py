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
        self.init_game_state()
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

    def play_loop(self, dt):
        self.screen.fill(COLOR['gameplay_bg'])
        match self.level:
            case 1:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (100, 100)
                    self.player = Player((self.all_sprites, self.player_sprites), self.player_start_pos)
                    Obstacle((self.all_sprites, self.obstacle_sprites), 'red', (300, 200), (200, 50))
                    Goal((self.all_sprites, self.goal_sprites), (1100, 600))
            case 2:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (100, WINDOW_HEIGHT - 100)
                    self.player.rect.topleft = self.player_start_pos
                    Obstacle((self.all_sprites, self.obstacle_sprites), 'red', (500, 400), (100, 200))
            case 3:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (100, WINDOW_HEIGHT - 100)
                    self.player.rect.topleft = self.player_start_pos
                    Obstacle((self.all_sprites, self.obstacle_sprites), 'red', (800, 100), (150, 150))
        self.all_sprites.update(dt)
        self.collisions()
        self.all_sprites.draw(self.screen)
        self.render_stats_text()

    def pause_menu(self, dt):
        pass

    def settings_menu(self, dt):
        pass

    def game_over_screen(self, dt):
        self.screen.fill(COLOR['game_over_bg'])

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
        self.text_surfaces['stats'] = self.fonts['stats'].render(f"Level: {self.level} Health: {self.player.health}", True, COLOR['stats_text'])
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
        self.font = join(self.FONT_DIR, 'BlockCraft.otf')

        self.fonts = {'stats': pygame.font.Font(self.font, 24)}

        self.text_surfaces = {'stats': self.fonts['stats'].render("Level: 1 Health: 5", True, COLOR['stats_text'])}

        self.text_rects = {'stats': self.text_surfaces['stats'].get_rect(topleft=(10, 10))}

    def init_sprites(self):
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.goal_sprites = pygame.sprite.Group()

    def init_game_state(self):
        self.level_set_up = False
        self.level = 1

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