import pygame
from vector2 import vector2
from view import View
from rect import Rect

class Text(View):
    align_left = "left"
    align_center = "center"
    align_right = "right"
    justify_up = "up"
    justify_center = "center"
    justify_bottom = "bottom"
    def __init__(self, rect, text = "Button", size = 25, color = (255,255,0)):
        super().__init__()
        self.rect = rect
        self.text = text
        self.size = size
        self.color = color
        self.justify = Text.justify_center
        self.align = Text.align_center
        self.offset = vector2()
        self.font = pygame.font.Font("NotoSans-Regular.ttf", 20)

    def on_draw(self, screen):
        text = self.font.render(self.text, True, self.color)
        pos = self.get_position(text)
        screen.blit(text, pos.as_tuple())

    def get_position(self, text):
        pos = self.rect.position

        # OFFSET
        pos += self.offset
        size  = self.rect.size


        # ALIGN
        if(self.align == Text.align_center):
            pos += vector2(size.x // 2, 0)
            pos -= vector2(text.get_width() // 2, 0)
        elif(self.align == Text.align_right):
            pos += vector2(size.x, 0)
            pos -= vector2(text.get_width(), 0)
        
        #JUSTIFY
        if(self.justify == Text.justify_center):
            pos += vector2(0, size.y // 2)
            pos -= vector2(0, text.get_height() // 2)
        elif(self.justify == Text.justify_bottom):
            pos += vector2(0, size.y)
            pos -= vector2(0, text.get_height())

        return pos
