import pygame
from vector2 import vector2
from view import View
from input import Input

class Button(View):
    def __init__(self, position, size, color = (150,150,150)):
        super().__init__()
        self.position = position
        self.size = size
        self.color = color
        self.mouse_down_color = (0, 150, 0)
        self.mouse_down = False
        self.on_click = None
        self.outline = 0

    #draw the rectangle and check if it is being hovered or clicked - kinda messy, sry...
    def on_draw(self, screen):
        color = self.color
        hovering = self.is_hovering()
        if(hovering == True):
            if(Input.get_mouse == True):
                #change color when mouse is clicked over the button
                color = self.mouse_down_color
                self.mouse_down = True
            else:
                if(self.mouse_down == True):
                    self.click()

                #change button color on hover - just made it a bit darker
                intensity = 0.7
                color = tuple(int(x * intensity) for x in self.color)
                self.mouse_down = False
        else:
            self.mouse_down = False

        p = (self.position.x, self.position.y, self.size.x, self.size.y)
        pygame.draw.rect(screen, color, p, self.outline)

    #call on_click event
    def click(self):
        if(self.on_click and callable(self.on_click)):
            self.on_click()

    #check if is being hovered - ya it call pygame.mouse.get_pos() for each button, I have no time to change...
    def is_hovering(self):
        mousePos = pygame.mouse.get_pos()
        min_x = self.position.x
        min_y = self.position.y
        max_x = self.position.x + self.size.x
        max_y = self.position.y + self.size.y
        if(mousePos[0] > min_x) and (mousePos[0] < max_x) & (mousePos[1] > min_y) and (mousePos[1] < max_y):
            return True
        else:
            return False
