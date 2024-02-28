# Add a Play button at start of game
import pygame


class Button():

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    # def message(self):
    #     self.msg_rect = self.msg_rect.get_rect()
    #     self.msg_rect.center = self.rect.center

    def draw2(self, surface):

        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # draw button on screen

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# pygame.display.flip()


# start_button = Button(100, 200, start_img, 0.5)
# exit_button = Button(450, 200, exit_img, 0.5)
