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
        self.start_time = perf_counter()
        self.hit_time = 0

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
                    if not self.game_beaten and event.key == pygame.K_ESCAPE:
                        self.requested_state = 'stop'
                    if self.game_beaten:
                        if event.key == pygame.K_RETURN:
                            self.requested_state = 'start'
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

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
                self.play_start = perf_counter()
                pygame.mixer.music.load(join(self.AUDIO_DIR, 'play_track.wav'))
                pygame.mixer.music.play(loops=-1)
            elif old == 'stop':
                resume_play_time(self)
                pygame.mixer.music.unpause()

        elif new == 'stop':
            pause_play_time(self)
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
        update_play_time(self)
        self.screen.fill(COLOR['gameplay_bg'])
        match self.level:
            case 1:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (100, WINDOW_CENTER[1])
                    Obstacle(self, (255,0,0), (250, 400), 'center', WINDOW_CENTER)
                    HealingItem(self, (30, 30), 'topleft', (300, WINDOW_CENTER[1]))
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
                    Obstacle(self, (255,0,0), (1100, 40), 'topleft', (50, 0))
                    Obstacle(self, (255,0,0), (1100, 40), 'bottomleft', (50, WINDOW_HEIGHT))
                    Obstacle(self, (255,0,0), (400, 40), 'topleft', (400, 90))
                    Obstacle(self, (255,0,0), (600, 40), 'topleft', (300, 300))
                    Obstacle(self, (255,0,0), (600, 40), 'topleft', (300, 400))
                    Obstacle(self, (255,0,0), (40, 250), 'topleft', (100, 250))
                    Obstacle(self, (255,0,0), (50, 200), 'topleft', (200, 250))
                    Obstacle(self, (255,0,0), (500, 40), 'topleft', (100, 500))
                    Obstacle(self, (255,0,0), (250, 40), 'topleft', (150, 590))
                    Obstacle(self, (255,0,0), (100, 100), 'topleft', (900, 500))
                    Obstacle(self, (255,0,0), (100, 100), 'topleft', (100, 100))
                    Obstacle(self, (255,0,0), (80, 100), 'topleft', (250, 50))
                    Obstacle(self, (255,0,0), (80, 50), 'bottomleft', (150, WINDOW_HEIGHT - 40))
                    Obstacle(self, (255,0,0), (300, 150), 'topleft', (500, 590))
                    Obstacle(self, (255,0,0), (50, 380), 'topleft', (50, 250))
                    Obstacle(self, (255,0,0), (100, 100), 'topleft', (560, 200))
                    Obstacle(self, (255,0,0), (100, 100), 'topleft', (400, 130))
                    Obstacle(self, (255,0,0), (250, 150), 'topleft', (850, 90))
                    HealingItem(self, (30, 30), 'center', (280, 655))
                    Goal(self, (50, 720), 'midleft', (0, WINDOW_CENTER[1]))
            case 6:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (50, WINDOW_CENTER[1])
                    Obstacle(self, (255,0,0), (500, 100), 'center', (WINDOW_CENTER[0], 50))
                    Obstacle(self, (255,0,0), (500, 100), 'center', (WINDOW_CENTER[0], WINDOW_HEIGHT - 50))
                    RotatingObstacle(self, (255,100,0), (520, 40), 'center', (WINDOW_CENTER), rotation_speed=120)
                    Goal(self, (50, 150), 'midright', (WINDOW_WIDTH, WINDOW_CENTER[1]))
            case 7:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (WINDOW_WIDTH-100, WINDOW_CENTER[1])
                    Obstacle(self, (255,0,0), (WINDOW_WIDTH, 30), 'midtop', (WINDOW_CENTER[0], 0))
                    Obstacle(self, (255,0,0), (WINDOW_WIDTH, 30), 'midbottom', (WINDOW_CENTER[0], WINDOW_HEIGHT))
                    RotatingObstacle(self, (255,100,0), (250, 25), 'center', (WINDOW_CENTER[0]+200, 150), rotation_speed=250)
                    RotatingObstacle(self, (255,100,0), (250, 25), 'center', (WINDOW_CENTER[0]+200, WINDOW_CENTER[1]), rotation_speed=-250)
                    RotatingObstacle(self, (255,100,0), (250, 25), 'center', (WINDOW_CENTER[0]+200, 570), rotation_speed=250)
                    RotatingObstacle(self, (255,100,0), (250, 25), 'center', (WINDOW_CENTER[0]-200, 150), rotation_speed=-250)
                    RotatingObstacle(self, (255,100,0), (250, 25), 'center', (WINDOW_CENTER[0]-200, WINDOW_CENTER[1]), rotation_speed=250)
                    RotatingObstacle(self, (255,100,0), (250, 25), 'center', (WINDOW_CENTER[0]-200, 570), rotation_speed=-250)
                    HealingItem(self, (30, 30), 'center', (WINDOW_CENTER[0]+150, 250))
                    Goal(self, (100, 100), 'center', (50, WINDOW_CENTER[1]))
            case 8:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (80, WINDOW_CENTER[1]+50)
                    Obstacle(self, color=(255,0,0), size=(1100, 30), anchor='bottomleft', pos=(0, WINDOW_HEIGHT-150))
                    Obstacle(self, color=(255,0,0), size=(30, 400), anchor='bottomleft', pos=(200, WINDOW_HEIGHT-150))
                    Obstacle(self, color=(255,0,0), size=(900, 30), anchor='bottomleft', pos=(200, 170))
                    Obstacle(self, color=(255,0,0), size=(900, 30), anchor='bottomleft', pos=(400, 330))
                    # top row
                    RotatingObstacle(self, color=(255,100,0), size=(300,20), anchor='center', pos=(350, 150), rotation_speed=-200)
                    RotatingObstacle(self, color=(255,100,0), size=(300,20), anchor='center', pos=(650, 150), rotation_speed=-200)
                    RotatingObstacle(self, color=(255,100,0), size=(300,20), anchor='center', pos=(950, 150), rotation_speed=-200)
                    # middle row
                    RotatingObstacle(self, color=(255,100,0), size=(210,20), anchor='center', pos=(520, 435), rotation_speed=+250)
                    RotatingObstacle(self, color=(255,100,0), size=(210,20), anchor='center', pos=(750, 435), rotation_speed=+250)
                    RotatingObstacle(self, color=(255,100,0), size=(210,20), anchor='center', pos=(980, 435), rotation_speed=+250)
                    # bottom row
                    RotatingObstacle(self, color=(255,100,0), size=(160,20), anchor='center', pos=(400, 650), rotation_speed=-250)
                    RotatingObstacle(self, color=(255,100,0), size=(160,20), anchor='center', pos=(690, 650), rotation_speed=+250)
                    RotatingObstacle(self, color=(255,100,0), size=(160,20), anchor='center', pos=(980, 650), rotation_speed=-250)
                    HealingItem(self, (30,30), 'center', (750, 370))
                    Goal(self, (50, 100), 'bottomleft', (50, WINDOW_HEIGHT-25))
            case 9:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (100, WINDOW_HEIGHT-75)
                    Obstacle(self, color=(255,0,0), size=(500, 30), anchor='bottomleft', pos=(600, 600))
                    Obstacle(self, color=(255,0,0), size=(650, 30), anchor='bottomleft', pos=(600, WINDOW_HEIGHT))
                    Obstacle(self, color=(255,0,0), size=(30, 600), anchor='bottomleft', pos=(1250, WINDOW_HEIGHT))
                    Obstacle(self, color=(255,0,0), size=(650, 30), anchor='bottomleft', pos=(600, 150))
                    Obstacle(self, color=(255,0,0), size=(30, 300), anchor='bottomleft', pos=(1100, 600))
                    Obstacle(self, color=(255,0,0), size=(400, 30), anchor='bottomleft', pos=(730, 300))
                    Obstacle(self, color=(255,0,0), size=(30, 200), anchor='bottomleft', pos=(700, 470))
                    Obstacle(self, color=(255,0,0), size=(30, 450), anchor='bottomleft', pos=(600, 600))
                    Obstacle(self, color=(255,0,0), size=(300, 30), anchor='bottomleft', pos=(700, 500))
                    Obstacle(self, color=(255,0,0), size=(200, 100), anchor='bottomleft', pos=(800, 470))
                    RotatingObstacle(self, color=(255,100,0), size=(1000,20), anchor='center', pos=(WINDOW_CENTER[0]+275, WINDOW_CENTER[1]+50), rotation_speed=+125)
                    HealingItem(self, (30,30), 'center', (850, 50))
                    Goal(self, (50, 50), 'bottomleft', (740, 460))
            case 10:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (720, 400)
                    Obstacle(self, color=(255,0,0), size=(900, 30), anchor='bottomleft', pos=(150, 550))
                    Obstacle(self, color=(255,0,0), size=(1000, 30), anchor='bottomleft', pos=(300, 300))
                    Obstacle(self, color=(255,0,0), size=(1000, 30), anchor='topleft', pos=(150, 100))
                    Obstacle(self, color=(255,0,0), size=(30, 450), anchor='topleft', pos=(150, 100))
                    Obstacle(self, color=(255,0,0), size=(30, 250), anchor='topleft', pos=(830, 300))
                    RotatingObstacle(self, color=(255,100,0), size=(300,20), anchor='center', pos=(450, 535), start_rotation=50, rotation_speed=+250)
                    RotatingObstacle(self, color=(255,100,0), size=(300,20), anchor='center', pos=(300, 285), rotation_speed=-250)
                    RotatingObstacle(self, color=(255,100,0), size=(150,20), anchor='center', pos=(650, 200), rotation_speed=-200)
                    RotatingObstacle(self, color=(255,100,0), size=(150,20), anchor='center', pos=(1000, 200), rotation_speed=-250)
                    RotatingObstacle(self, color=(255,100,0), size=(100,20), anchor='center', pos=(800, 50), rotation_speed=+150)
                    RotatingObstacle(self, color=(255,100,0), size=(100,20), anchor='center', pos=(600, 50), rotation_speed=+175)
                    RotatingObstacle(self, color=(255,100,0), size=(100,20), anchor='center', pos=(400, 50), rotation_speed=+200)
                    RotatingObstacle(self, color=(255,100,0), size=(300,20), anchor='center', pos=(450, 700), start_rotation=150,rotation_speed=-250)
                    RotatingObstacle(self, color=(255,100,0), size=(200,20), anchor='center', pos=(1000, 650), rotation_speed=-500)
                    RotatingObstacle(self, color=(255,100,0), size=(180,20), anchor='center', pos=(1150, 500), start_rotation=50, rotation_speed=-500)
                    Goal(self, (100, 100), 'bottomleft', (900, 450))
            case 11:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (1000, 375)
                    Obstacle(self, (255,0,0), (1280, 30), 'topright', (1280, 550))
                    Obstacle(self, (255,0,0), (1280, 30), 'topright', (1280, 250))
                    VerticalMovingObstacle(self, (255,0,100), (30, 100), 'center', (750, WINDOW_CENTER[1]-28), move_range=166, speed=300)
                    VerticalMovingObstacle(self, (255,0,100), (30, 100), 'center', (550, WINDOW_CENTER[1]-28), move_range=166, speed=400)
                    VerticalMovingObstacle(self, (255,0,100), (30, 100), 'center', (350, WINDOW_CENTER[1]-28), move_range=166, speed=500)
                    VerticalMovingObstacle(self, (255,0,100), (30, 100), 'center', (150, WINDOW_CENTER[1]-28), move_range=166, speed=600)
                    HealingItem(self, (30, 30), 'topleft', (1160, 385))
                    Goal(self, (50, 270), 'topleft', (0, 280))
            case 12:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (50, WINDOW_CENTER[1]-20)
                    # first wave
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (400, -150), move_range=5000, speed=1600)
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (600, -150), move_range=5000, speed=1600)
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (800, -150), move_range=5000, speed=1600)
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (1000,-150), move_range=5000, speed=1600)
                    #second wave
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (500, -800), move_range=5000, speed=1600)
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (700, -800), move_range=5000, speed=1600)
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (900, -800), move_range=5000, speed=1600)
                    VerticalMovingObstacle(self, (255,0,100), (30, 250), 'center', (1100,-800), move_range=5000, speed=1600)
                    Goal(self, (100, 144), 'bottomright', (1289.9999999999998, WINDOW_HEIGHT))
            case 13:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (WINDOW_WIDTH-100, WINDOW_HEIGHT-100)
                    Obstacle(self, (255,0,0), (1280, 50), 'midtop', (WINDOW_CENTER[0], 0))
                    # first column
                    Obstacle(self, (255,0,0), (30, 550), 'topright', (1030, 200))
                    HorizontalMovingObstacle(self, (255,0,100), (100, 30), 'center', (1080, 500), move_range=150, speed=550)
                    HorizontalMovingObstacle(self, (255,0,100), (100, 30), 'center', (1080, 300), move_range=150, speed=550)
                    # second column
                    Obstacle(self, (255,0,0), (30, 550), 'topright', (730, 25))
                    HorizontalMovingObstacle(self, (255,0,100), (100, 30), 'center', (780, 500), move_range=170, speed=600)
                    HorizontalMovingObstacle(self, (255,0,100), (100, 30), 'center', (780, 300), move_range=170, speed=600)
                    # third column
                    Obstacle(self, (255,0,0), (30, 550), 'topright', (430, 200))
                    VerticalMovingObstacle(self, (255,0,100), (140, 30), 'center', (500, 215), move_range=300, init_dir=-1, speed=300)
                    VerticalMovingObstacle(self, (255,0,100), (130, 30), 'center', (635, 260), move_range=300, speed=300)
                    # left chunk
                    Obstacle(self, (255,0,0), (250, 250), 'center', (190, 500))
                    VerticalMovingObstacle(self, (255,0,100), (85, 30), 'center', (357, 215), move_range=400, speed=375)
                    VerticalMovingObstacle(self, (255,0,100), (70, 30), 'center', (30, 215), move_range=400, speed=375)
                    Goal(self, (100, 100), 'center', (190, 675))
            case 14:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (240, 650)
                    HorizontalMovingObstacle(self, (255,0,100), (200, 30), 'topleft', (0, 450), move_range=200, speed=500)
                    VerticalMovingObstacle(self, (255,0,100), (30, 180), 'bottomleft', (400, 630), move_range=90, init_dir=-1, speed=300)
                    Obstacle(self, (255,0,0), (30, 600), 'center', (WINDOW_CENTER[0], WINDOW_HEIGHT-300))
                    VerticalMovingObstacle(self, (255,0,100), (30, 30), 'center', (WINDOW_CENTER[0], 15), move_range=90, speed=300)
                    HorizontalMovingObstacle(self, (255,0,100), (200, 30), 'topright', (WINDOW_WIDTH-200, 450), move_range=200, speed=700)
                    VerticalMovingObstacle(self, (255,0,100), (30, 180), 'bottomright', (WINDOW_WIDTH-400, 630), move_range=90, init_dir=-1, speed=500)
                    Goal(self, (50, 50), 'bottomright', (WINDOW_WIDTH, WINDOW_HEIGHT))
            case 15:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (WINDOW_WIDTH-100, WINDOW_HEIGHT-100)
                    # lower row
                    Obstacle(self, (255,0,0), (1100, 30), 'topright', (WINDOW_WIDTH, 500))
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (900, 555), move_range=135, speed=350)
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (700, 555), move_range=135, speed=400)
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (500, 555), move_range=135, speed=450)
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (300, 555), move_range=135, speed=500)
                    HorizontalMovingObstacle(self, (255,0,100), (60, 30), 'topleft', (0, 500), move_range=120, speed=400)
                    # mid row
                    Obstacle(self, (255,0,0), (1100, 30), 'topleft', (0, 280))
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (300, 335), move_range=135, speed=500)
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (500, 335), move_range=135, speed=550)
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (700, 335), move_range=135, speed=600)
                    VerticalMovingObstacle(self, (255,0,100), (60, 60), 'center', (900, 335), move_range=135, speed=650)
                    HorizontalMovingObstacle(self, (255,0,100), (60, 30), 'topleft', (1100, 280), move_range=120, speed=500)
                    # upper row
                    Obstacle(self, (255,0,0), (1280, 50), 'topright', (WINDOW_WIDTH, 0))
                    VerticalMovingObstacle(self, (255,0,100), (150, 150), 'topleft', (500, 50), move_range=80, speed=175)
                    HealingItem(self, (30, 30), 'bottomleft', (60, 180))
                    Goal(self, (150, 150), 'bottomleft', (150, 240))
            case 16:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (250, 160)
                    Obstacle(self, (255,0,0), (30, 350), 'bottomleft', (0, WINDOW_HEIGHT))
                    Obstacle(self, (255,0,0), (300, 30), 'bottomleft', (0, 370))
                    Obstacle(self, (255,0,0), (30, 550), 'topleft', (400, 0))
                    Obstacle(self, (255,0,0), (1280, 30), 'bottomleft', (0, WINDOW_HEIGHT))
                    RotatingObstacle(self, (255,100,0), (350, 30), 'center', (210,530), rotation_speed=200)
                    VerticalMovingObstacle(self, (255,0,100), (30, 30), 'topleft', (400, 550), move_range=110, speed=180)
                    Obstacle(self, (255,0,0), (700, 30), 'topleft', (400, 520))
                    RotatingObstacle(self, (255,100,0), (140, 25), 'center', (750,620), rotation_speed=-250)
                    VerticalMovingObstacle(self, (255,0,100), (150, 30), 'topleft', (950, 550), move_range=110, speed=250)
                    Obstacle(self, (255,0,0), (400, 30), 'bottomleft', (430, 160))
                    Obstacle(self, (255,0,0), (380, 30), 'bottomleft', (900, 160))
                    RotatingObstacle(self, (255,100,0), (500, 30), 'center', (1030,250), rotation_speed=-220)
                    RotatingObstacle(self, (255,100,0), (350, 30), 'center', (610,340), rotation_speed=200)
                    HealingItem(self, (30, 30), 'center', (500, 450))
                    Goal(self, (100, 100), 'topleft', (500, 15))
            case 17:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (580, 50)
                    Obstacle(self, (255,0,0), (30, 720), 'topleft', (385, 0))
                    Obstacle(self, (255,0,0), (30, 620), 'topleft', (785, 0))
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (450, 200), move_range=100, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (650, 200), move_range=100, init_dir=-1, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (450, 300), move_range=100, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (650, 300), move_range=100, init_dir=-1, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (450, 400), move_range=100, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (650, 400), move_range=100, init_dir=-1, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (450, 500), move_range=100, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (650, 500), move_range=100, init_dir=-1, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (450, 600), move_range=100, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (130, 30), 'center', (650, 600), move_range=100, init_dir=-1, speed=400)
                    RotatingObstacle(self, (255,100,0), (450, 30), 'center', (1050,600), rotation_speed=260)
                    RotatingObstacle(self, (255,100,0), (450, 30), 'center', (1050,300), rotation_speed=-260)
                    Goal(self, (100, 100), 'topleft', (1000, 50))
            case 18:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (1050,100)
                    Obstacle(self, (255,0,0), (40, 620), 'topleft', (800, 0))
                    Obstacle(self, (255,0,0), (40, 620), 'topright', (1280, 0))
                    VerticalMovingObstacle(self, (255,0,100), (200, 30), 'center', (940, 300), move_range=150, speed=400)
                    VerticalMovingObstacle(self, (255,0,100), (200, 30), 'center', (1140, 402), move_range=150, init_dir=-1, speed=400)
                    HorizontalMovingObstacle(self, (255,0,100), (200, 30), 'center', (-100, 650), move_range=5000, speed=500)
                    HorizontalMovingObstacle(self, (255,0,100), (200, 30), 'center', (-600, 700), move_range=5000, speed=500)
                    HorizontalMovingObstacle(self, (255,0,100), (200, 30), 'center', (-1100, 650), move_range=5000, speed=500)
                    HorizontalMovingObstacle(self, (255,0,100), (200, 30), 'center', (-1500, 700), move_range=5000, speed=500)
                    Obstacle(self, (255,0,0), (40, 620), 'bottomleft', (400, 720))
                    RotatingObstacle(self, (255,100,0), (350, 30), 'center', (625,340), rotation_speed=400)
                    VerticalMovingObstacle(self, (255,0,100), (200, 30), 'center', (100, 330), move_range=150, speed=400)
                    VerticalMovingObstacle(self, (255,0,100), (200, 30), 'center', (300, 350), move_range=150, init_dir=-1, speed=400)
                    Goal(self, (50, 50), 'center', (200, 600))
            case 19:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (200,600)
                    Obstacle(self, (255,0,0), (1280, 30), 'bottomleft', (0, WINDOW_HEIGHT))
                    Obstacle(self, (255,0,0), (1200, 30), 'bottomleft', (0, WINDOW_HEIGHT-220))
                    Obstacle(self, (255,0,0), (1200, 30), 'bottomleft', (80, WINDOW_HEIGHT-440))
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'bottomleft', (1200, WINDOW_HEIGHT-220), move_range=50, speed=150)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'bottomleft', (0, WINDOW_HEIGHT-440), move_range=50, speed=150)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'bottomleft', (-130, WINDOW_HEIGHT-250), move_range=5000, speed=800)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'bottomleft', (-330, WINDOW_HEIGHT-300), move_range=5000, speed=800)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'bottomleft', (-530, WINDOW_HEIGHT-350), move_range=5000, speed=800)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'bottomleft', (-730, WINDOW_HEIGHT-400), move_range=5000, speed=800)
                    RotatingObstacle(self, (255,100,0), (120, 30), 'center', (400, 60), rotation_speed=-200)
                    RotatingObstacle(self, (255,100,0), (120, 30), 'center', (400, 180), rotation_speed=200)
                    RotatingObstacle(self, (255,100,0), (120, 30), 'center', (600, 60), rotation_speed=200)
                    RotatingObstacle(self, (255,100,0), (120, 30), 'center', (600, 180), rotation_speed=-200)
                    RotatingObstacle(self, (255,100,0), (120, 30), 'center', (800, 60), rotation_speed=-200)
                    RotatingObstacle(self, (255,100,0), (120, 30), 'center', (800, 180), rotation_speed=200)
                    VerticalMovingObstacle(self, (255,0,100), (30, 80), 'center', (WINDOW_CENTER[0]-50, 540), move_range=110, speed=300)
                    VerticalMovingObstacle(self, (255,0,100), (30, 80), 'center', (WINDOW_CENTER[0]+160, 540), move_range=110, init_dir=-1, speed=300)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'center', (WINDOW_CENTER[0]-20, 515), move_range=150, speed=150)
                    HorizontalMovingObstacle(self, (255,0,100), (30, 30), 'center', (WINDOW_CENTER[0]-20, 675), move_range=150, speed=150)
                    HealingItem(self, (30, 30), 'center', (600, 25))
                    Goal(self, (100, 100), 'center', (1200, 140))
            case 20:
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = (1100, 140)
                    Obstacle(self, (255,0,0), (1280, 50), 'topleft', (0, 0))
                    Obstacle(self, (255,0,0), (1280, 50), 'bottomleft', (0, 720))
                    Obstacle(self, (255,0,0), (50, 720), 'topleft', (0, 0))
                    Obstacle(self, (255,0,0), (50, 720), 'topright', (1280, 0))
                    RotatingObstacle(self, (255,100,0), (400, 20), 'center', (WINDOW_CENTER[0], WINDOW_CENTER[1]), rotation_speed=-450)
                    HealingItem(self, (30, 30), 'center', (200, 200))
                    HealingItem(self, (30, 30), 'center', (1080, 580))
                    HealingItem(self, (30, 30), 'center', (200, 580))
                    HealingItem(self, (30, 30), 'center', (1080, 200))
                    Goal(self, (60, 60), 'center', WINDOW_CENTER)
            case _:
                # --- game beaten ---
                if not self.level_set_up:
                    self.level_set_up = True
                    self.player_start_pos = None
                    self.game_beaten = True
                    self.final_time = self.play_time
                    minutes = int(self.final_time // 60)
                    seconds = float(self.final_time % 60)
                    timer_text = f"Time: {minutes:02}:{seconds:04.1f}"
                    self.text_surfaces['final_time'] = self.fonts['final_time'].render(f"Final {timer_text}", True, COLOR['final_time'])
                    self.text_rects['final_time'] = self.text_surfaces['final_time'].get_rect(center=WINDOW_CENTER)
                    pygame.mixer.music.load(join(self.AUDIO_DIR, 'game_over_track.wav'))
                    pygame.mixer.music.play()

                self.screen.fill(COLOR['game_beaten_bg'])
                self.screen.blit(self.text_surfaces['final_time'], self.text_rects['final_time'])
                self.screen.blit(self.text_surfaces['start_hint'], self.text_rects['start_hint'])

        if not self.game_beaten:
            self.all_sprites.update(dt)
            self.collisions()
            self.all_sprites.draw(self.screen)
            self.render_stats_text()
            self.render_timer_text()

    def pause_menu(self, dt):
        self.screen.fill(COLOR['gameplay_bg'])
        self.all_sprites.draw(self.screen)
        self.render_stats_text()
        self.render_timer_text()
        dim = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
        dim.fill((0, 0, 0, 125))
        self.screen.blit(dim, (0, 0))
        self.screen.blit(self.text_surfaces['paused_text'], self.text_rects['paused_text'])

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
        hit_obstacle = pygame.sprite.spritecollide(self.player, self.obstacle_sprites, False, pygame.sprite.collide_mask)
        if hit_obstacle:
            self.player.health -= 1
            if self.player.health >= 1:
                self.hit_sound.play()
                self.player.rect.topleft = self.player_start_pos
                self.hit_time = self.runtime
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

        # --- heal item collision ---
        hit_heal_item = pygame.sprite.spritecollideany(self.player, self.healing_sprites)
        if hit_heal_item:
            self.heal_sound.play()
            self.player.health += 1
            hit_heal_item.kill()

    def render_stats_text(self):
        self.text_surfaces['stats'] = self.fonts['stats'].render(f"Level: {self.level}    Health: {self.player.health}", True, COLOR['stats_text'])
        self.screen.blit(self.text_surfaces['stats'], self.text_rects['stats'])

    def render_timer_text(self):
        minutes = int(self.play_time // 60)
        seconds = float(self.play_time % 60)
        timer_text = f"Time: {minutes:02}:{seconds:04.1f}"

        self.text_surfaces['timer'] = self.fonts['timer'].render(timer_text, True, COLOR['timer_text'])
        self.screen.blit(self.text_surfaces['timer'], self.text_rects['timer'])

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
        self.heal_sound: pygame.mixer.Sound = pygame.mixer.Sound(join(self.AUDIO_DIR, 'heal_sound.wav'))

    def set_all_volumes(self):
        # --- game music ---
        pygame.mixer.music.set_volume(1)

        # --- sound effects ---
        self.hit_sound.set_volume(HIT_SOUND_VOLUME)
        self.death_sound.set_volume(DEATH_SOUND_VOLUME)
        self.reach_goal_sound.set_volume(REACH_GOAL_SOUND_VOLUME)
        self.heal_sound.set_volume(HEAL_SOUND_VOLUME)

    def load_graphics(self):
        self.font_1 = join(self.FONT_DIR,'gomarice_no_continue.ttf')
        self.font_2 = join(self.FONT_DIR,'slkscr.ttf')

        self.fonts = {'stats': pygame.font.Font(self.font_1, STATS_TEXT_FONT_SIZE),
                      'publisher': pygame.font.Font(self.font_2, PUBLISHER_FONT_SIZE),
                      'hint': pygame.font.Font(self.font_2, HINT_FONT_SITZE),
                      'title': pygame.font.Font(self.font_1, TITLE_FONT_SIZE),
                      'game_over': pygame.font.Font(self.font_1, GAME_OVER_FONT_SIZE),
                      'timer': pygame.font.Font(self.font_1, TIMER_FONT_SIZE),
                      'final_time': pygame.font.Font(self.font_1, FINAL_TIME_FONT_SIZE),
                      'paused_text': pygame.font.Font(self.font_1, PAUSED_TEXT_FONT_SIZE)}

        self.text_surfaces = {'stats': self.fonts['stats'].render(f"Level: 1 Health: {PLAYER_HEALTH}", True, COLOR['stats_text']),
                              'publisher': self.fonts['publisher'].render("Ralphus Studios", True, COLOR['publisher']),
                              'start_hint': self.fonts['hint'].render("Start game: RETURN\nClose game: ESC", True, COLOR['start_hint']),
                              'game_over_hint': self.fonts['hint'].render("Play again: RETURN\nClose game: ESC", True, COLOR['game_over_hint']),
                              'title': self.fonts['title'].render(GAME_NAME, True, COLOR['title']),
                              'game_over': self.fonts['game_over'].render("GAME OVER", True, COLOR['game_over']),
                              'timer': self.fonts['timer'].render("Time: 00:00.0", True, COLOR['final_time']),
                              'final_time': self.fonts['final_time'].render("Final Time: 00:00.0", True, COLOR['final_time']),
                              'paused_text': self.fonts['paused_text'].render("PAUSED", True, COLOR['paused_text'])}

        self.text_rects = {'stats': self.text_surfaces['stats'].get_rect(topleft=(10, 10)),
                           'publisher': self.text_surfaces['publisher'].get_rect(bottomright=(WINDOW_WIDTH-10, WINDOW_HEIGHT-10)),
                           'start_hint': self.text_surfaces['start_hint'].get_rect(bottomleft=(10, WINDOW_HEIGHT-10)),
                           'game_over_hint': self.text_surfaces['game_over_hint'].get_rect(bottomleft=(10, WINDOW_HEIGHT-10)),
                           'title': self.text_surfaces['title'].get_rect(center=WINDOW_CENTER),
                           'game_over': self.text_surfaces['game_over'].get_rect(center=WINDOW_CENTER),
                           'timer': self.text_surfaces['timer'].get_rect(topright=(WINDOW_WIDTH-10, 10)),
                           'final_time': self.text_surfaces['final_time'].get_rect(topright=(WINDOW_WIDTH-10, 10)),
                           'paused_text': self.text_surfaces['paused_text'].get_rect(center=WINDOW_CENTER)}

    def init_sprites(self):
        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.goal_sprites = pygame.sprite.Group()
        self.healing_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()

    def init_game_state(self):
        self.game_beaten = False
        self.final_time = 0.0
        self.level_set_up = False
        self.level = 1
        self.show_start_hint = False
        self.show_game_over_hint = False
        if getattr(self, 'player', None):
            self.player.kill()
        self.player = Player(self, (self.all_sprites, self.player_sprites), (50, WINDOW_CENTER[1]))
        self.play_time = 0.0
        self.play_start = None
        self.pause_start = 0.0
        self.total_paused = 0.0
        self.is_paused = False

    @property
    def runtime(self):
        return perf_counter() - self.start_time

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