import pygame
import math
from button import Button
from vector2 import vector2

#It is a button who has a figure drawn on it
class FigureButton(Button):
    shape_triangle = 0
    shape_square = 1
    shape_circle = 2

    def __init__(self, position, size, text = "Button", color = (150,150,150)):
        super().__init__(position, size, color)
        self.shape_visible = False
        self.shape = FigureButton.shape_square
        self.shape_color = (0,0,0)

    def draw(self, screen):
        #Change color if its hiding the figure
        default_color = self.color
        if(self.shape_visible == True):
            self.outline = 2
            self.color = self.shape_color
        else:
            self.outline = 0

        super().draw(screen)
        self.color = default_color


        if self.shape_visible == False:
            return

        #Draw figure
        size = self.size.x
        if self.size.x > self.size.y:
            size = self.size.y
        size *= 0.7
        size = int(size // 2)
            
        center = vector2(self.position.x, self.position.y)
        center += vector2(self.size.x / 2, self.size.y / 2)

        #Select the figure to draw
        if self.shape == FigureButton.shape_circle :
            pygame.draw.circle(screen, self.shape_color, center.as_int().as_tuple(), size)
        elif self.shape == FigureButton.shape_triangle:
            figure = FigureButton.get_polygon(3, center, size, -90)
            pygame.draw.polygon(screen, self.shape_color, figure)
        elif self.shape == FigureButton.shape_square:
            figure = FigureButton.get_polygon(4, center, size, -45)
            pygame.draw.polygon(screen, self.shape_color, figure)

    #Set figure visible
    def set_shape_visible(self, visible):
        self.shape_visible = visible
    
    #A nice function to generate polygons
    @staticmethod
    def get_polygon(sides, position, radius=1, rotation=0):
        points = []
        angle = 360 / sides

        for i in range(sides):
            a = i * angle + rotation
            a = math.radians(a)
            v = vector2(math.cos(a), math.sin(a))
            v *= radius
            v += position
            points.append(v.to_int().as_tuple())

        return points
