    def render_timer_text(self):
        minutes = int(self.play_time // 60)
        seconds = self.play_time % 60

        text = f"TIME: {minutes:02d}:{seconds:04.1f}"
        text_surf = self.fonts["timer"].render(text, True, COLOR["timer_text"])

        # fixed width based on a template string with the max characters you’ll show
        template = "TIME: 00:00.0"
        box_w, box_h = self.fonts["timer"].size(template)

        box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        # right-align text inside the box
        box.blit(text_surf, (box_w - text_surf.get_width(), 0))

        box_rect = box.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        self.screen.blit(box, box_rect)