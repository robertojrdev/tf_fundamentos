import pygame
import random
import time
from vector2 import *

ROUTINES = []
DELTA_TIME = 0

def main():
    global ROUTINES
    global DELTA_TIME
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((int(800 * 1.5),int(600 * 1.5)))

    
    views = []

    game = Game(screen, 3, 4)
    game.is_visible = False
    views.append(game)

    menu = Menu(screen, game)
    views.append(menu)

    # r = Rect(vector2(200,200), vector2(100,100))
    # t = Text(screen, r)
    # views.append(t)

    finishedRoutines = []
    lastTime = time.time()
    while(True):
        # Process OS events
        evt = pygame.event.get()
        for event in evt:
            # Checks if the user closed the window
            if (event.type == pygame.QUIT):
                # Exits the application immediately
                return
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    return
                if (event.key == pygame.K_KP_ENTER):
                    game.on_finish_game()

        Input.update(evt)

        screen.fill((0,100,0))

        # update(screen)
        for v in views:
            v.draw(screen)

        pygame.display.flip()

        DELTA_TIME = time.time() - lastTime
        lastTime = time.time()

        #call coroutines
        for r in ROUTINES:
            v = next(r, False)
            if(v == False) :
                ROUTINES.remove(r)

def update(screen):
    pass
    
class View:
    is_visible = True
    def __init__(self):
        self.childs = []

    def draw(self, screen):
        if(self.is_visible == True):
            self.on_draw(screen)
            for c in self.childs:
                c.draw(screen)
    
    def on_draw(self, screen):
        pass

    def set_visible(self, visible):
        self.is_visible = visible

class Menu(View):
    def __init__(self, screen, game):
        super().__init__()
        
        self.game = game

        size = vector2(150, 50)
        gameModes = [(4,3),(4,4),(5,4),(6,5),(6,6)]
        rows = len(gameModes)
        dist_offset = 10
        offset = vector2()
        offset.x = (screen.get_width() - size.x)/2
        offset.y = (screen.get_height() - ((rows - 1) * dist_offset + rows * size.y)) / 2


        for y in range(rows):
            mode = gameModes[y]
            pos = vector2(offset.x, (y * (dist_offset + size.y) + offset.y))
            b = TextButton(pos, size, str(mode[0]) + " x " + str(mode[1]))
            b.on_click = lambda menu=self, mode=mode : menu.start_game(mode)
            self.childs.append(b)

    def start_game(self, mode):
        self.game.new_game(mode[0], mode[1])
        self.is_visible = False
        self.game.is_visible = True
        self.game.on_win = lambda game=self.game, menu=self : menu.show_menu(game)

    def show_menu(self, game):
        self.is_visible = True
        game.is_visible = False

class Text(View):
    align_left = "left"
    align_center = "center"
    align_right = "right"
    justify_up = "up"
    justify_center = "center"
    justify_bottom = "bottom"
    def __init__(self, rect, text = "Button", size = 25, color = (20,20,20)):
        super().__init__()
        self.rect = rect
        self.text = text
        self.size = size
        self.color = color
        self.justify = Text.justify_center
        self.align = Text.align_center
        self.offset = vector2()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)

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

class Game(View):
    defaultScoreText = "Score: "

    def __init__(self, screen, rows = 0, columns=0):
        super().__init__()
        self.cards = []
        self.screen = screen
        self.cards_offset = 10
        self.card_size = vector2(50, 100)
        self.selected_cards = []
        self.on_win = None
        self.score = 0
        self.wrong_attempts = 0

        self.score_text = Text(Rect(vector2(20,20), vector2(150,50)), Game.defaultScoreText + str(self.score))
        self.score_text.justify = Text.justify_up
        self.score_text.align = Text.align_left
        self.childs.append(self.score_text)

        if rows != 0 and columns != 0:
            self.new_game(rows, columns)

    def new_game(self, rows, columns):
        self.cards.clear()
        global ROUTINES

        offset = vector2()
        offset.x = (self.screen.get_width() - ((columns -1) * self.cards_offset + columns * self.card_size.x)) / 2
        offset.y = (self.screen.get_height() - ((rows -1) * self.cards_offset + rows * self.card_size.y)) / 2

        for x in range(columns):
            for y in range(rows):
                p = vector2()
                p.x = x * (self.cards_offset + self.card_size.x) + offset.x
                p.y = y * (self.cards_offset + self.card_size.y) + offset.y
                c = FigureButton(p, self.card_size, str(y * columns + x))
                c.on_click = lambda c=c : start_coroutine(self.select_card(c))
                self.cards.append(c)

        random.shuffle(self.cards)
        random.shuffle(self.cards) #twice to get a better mix

        colors = [(255, 0, 0), (0,255,0), (0,0,255), (255, 0, 255), (255,255,0), (0,255,255)]
        figures = [0,1,2]

        total = rows * columns

        i = 0
        while i // 6 < total:
            for x in range(3): #for each shape
                for y in range(2): #do it twice to have pairs
                    if(i >= total):
                        return
                    self.cards[i].shape_color = colors[(i // 6) % len(colors)] # if it exceed the amount of collors start to repeat
                    self.cards[i].shape = figures[x]
                    i += 1

    def select_card(self, card):
        isSame = len(self.selected_cards) != 0 and self.selected_cards[0] == card
        hasTwo = len(self.selected_cards) >= 2
        if isSame or hasTwo:
            return

        card.set_shape_visible(True)
        self.selected_cards.append(card)
        if len(self.selected_cards) == 2:
            sameShape = self.selected_cards[0].shape == self.selected_cards[1].shape
            sameColor = self.selected_cards[0].shape_color == self.selected_cards[1].shape_color
            
            w = wait_for_seconds(1)
            r = True
            while r != False:
                yield True
                r = next(w, False)

            if sameShape and sameColor:
                for c in self.selected_cards:
                    self.cards.remove(c)
                self.on_correct()
            else:
                for c in self.selected_cards:
                    c.set_shape_visible(False)
                self.on_wrong()

            self.selected_cards.clear()

        if len(self.cards) == 0:
            self.on_finish_game()

    def on_correct(self):
        self.score += 100
        self.score_text.text = Game.defaultScoreText + str(self.score)

    def on_wrong(self):
        self.wrong_attempts += 1
        if self.wrong_attempts >= 2:
            self.score -= 20 * self.wrong_attempts
            if self.score < 0 : self.score = 0
            self.score_text.text = Game.defaultScoreText + str(self.score)

    def on_finish_game(self):
        print("END GAME")
        if(self.on_win):
            self.on_win()

    def on_draw(self, screen):
        for c in self.cards:
            c.draw(screen)

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

    def on_draw(self, screen):
        color = self.color
        hovering = self.is_hovering()
        if(hovering == True):
            if(Input.get_mouse == True):
                color = self.mouse_down_color
                self.mouse_down = True
            else:
                if(self.mouse_down == True):
                    self.click()

                intensity = 0.7
                color = tuple(int(x * intensity) for x in self.color)
                self.mouse_down = False
        else:
            self.mouse_down = False

        p = (self.position.x, self.position.y, self.size.x, self.size.y)
        pygame.draw.rect(screen, color, p, self.outline)

    def click(self):
        if(self.on_click):
            self.on_click()

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

class TextButton(Button):
    def __init__(self, position, size, text = "Button", color = (150,150,150)):
        super().__init__(position, size, color)
        self.text = Text(Rect(position, size), text)
        self.childs.append(self.text)

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

        size = self.size.x
        if self.size.x > self.size.y:
            size = self.size.y
        size *= 0.7
        size = int(size // 2)
            
        center = vector2(self.position.x, self.position.y)
        center += vector2(self.size.x / 2, self.size.y / 2)

        if self.shape == FigureButton.shape_circle :
            pygame.draw.circle(screen, self.shape_color, center.as_int().as_tuple(), size)
        elif self.shape == FigureButton.shape_triangle:
            figure = FigureButton.get_polygon(3, center, size, -90)
            pygame.draw.polygon(screen, self.shape_color, figure)
        elif self.shape == FigureButton.shape_square:
            figure = FigureButton.get_polygon(4, center, size, -45)
            pygame.draw.polygon(screen, self.shape_color, figure)

    def set_shape_visible(self, visible):
        self.shape_visible = visible

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

class Input:
    get_mouse = False
    get_mouse_down = False
    get_mouse_up = False

    @staticmethod
    def update(evt):
        
        Input.get_mouse_down = False
        Input.get_mouse_up = False

        for e in evt:
            if e.type == pygame.MOUSEBUTTONDOWN:
                Input.get_mouse_down = True
                Input.get_mouse = True
                Input.get_mouse_up = False
            elif e.type == pygame.MOUSEBUTTONUP:
                Input.get_mouse_down = False
                Input.get_mouse = False
                Input.get_mouse_up = True

class Rect:
    def __init__(self, position, size):
        self.position = position
        self.size = size

def start_coroutine(routine):
    global ROUTINES
    ROUTINES.append(routine)
    return routine

def wait_for_seconds(time):
    timer = 0
    global DELTA_TIME
    while timer < time:
        yield True
        timer += DELTA_TIME

#Call main, because Diogo told me to do so
main()