import pygame
from view import View

class Image(View):
    def __init__(self, img, pos):
        """
        Arguments:
            img {string} -- [path to image file]
            pos {vector2} -- [the position is relative to center of the image]
        """

        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(center=pos.as_tuple())

    def on_draw(self, screen):
        screen.blit(self.image, self.rect)
