import sys
from vector2 import vector2
from view import View
from text_button import TextButton
from image import Image

class Menu(View):
    def __init__(self, screen, game):
        super().__init__()
        
        self.game = game

        #BUTTONS SETTINGS
        size = vector2(150, 50)
        gameModes = [(4,3),(4,4),(5,4),(6,5),(6,6)]
        rows = len(gameModes)
        dist_offset = 10
        #offset to center on screen
        offset = vector2()
        offset.x = (screen.get_width() - size.x)/2
        offset.y = (screen.get_height() - ((rows - 1) * dist_offset + rows * size.y)) / 2
        #offset to move a bit manually
        offset += vector2(0, 30)

        #CREATE LEVEL BUTTONS
        for y in range(rows):
            mode = gameModes[y]
            pos = vector2(offset.x, (y * (dist_offset + size.y) + offset.y))
            b = TextButton(pos, size, str(mode[0]) + " x " + str(mode[1]))
            b.on_click = lambda menu=self, mode=mode : menu.start_game(mode)
            self.childs.append(b)

        #CREATE EXIT BUTTON
        pos = vector2(offset.x, ((rows +1) * (dist_offset + size.y) + offset.y))
        exit_button = TextButton(pos, size, "Exit")
        exit_button.on_click = lambda : sys.exit()
        self.childs.append(exit_button)

        #CREATE IMAGE
        img = Image("shuffle.png", offset + vector2(50, -100))
        self.childs.append(img)

    def start_game(self, mode):
        """        
        Arguments:
            mode {tuple(x,y)} -- [define columns(x) and rows(y)]
        """
        self.game.new_game(mode[0], mode[1])
        self.is_visible = False
        self.game.is_visible = True
        self.game.on_exit = lambda menu=self : menu.set_visible(True)
