import pygame

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 60
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.bg_color = (0, 0, 0)
        self.box_color = (50, 50, 50)
        self.box_margin = 20

    def draw_hud(self, score, ammo, health):
        self._draw_info("Score: " + str(score), self.text_color, 0)
        self._draw_info("Ammo: " + str(ammo), self.text_color, 1)
        self._draw_info("Health: " + str(health), self.text_color, 2)

    def _draw_info(self, text, color, position):
        info_surface = self.font.render(text, True, color)
        info_rect = info_surface.get_rect()
        info_rect.center = ((position + 1) * self.width, self.height // 2)

        box_rect = pygame.Rect(0, 0, self.width - self.box_margin, self.height - self.box_margin)
        box_rect.center = info_rect.center
        pygame.draw.rect(self.screen, self.box_color, box_rect)

        self.screen.blit(info_surface, info_rect)
