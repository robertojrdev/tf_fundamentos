import random
from view import View
from vector2 import vector2
from text import Text
from rect import Rect
from text_button import TextButton
from figure_button import FigureButton
from routines import Routine

class Game(View):
    defaultScoreText = "Score: "

    def __init__(self, screen, rows = 0, columns=0):
        super().__init__()
        self.cards = []
        self.screen = screen
        self.cards_offset = 10
        self.card_size = vector2(70, 100)
        self.selected_cards = []
        self.on_exit = None
        self.score = 0
        self.wrong_attempts = 0

        # SCORE TEXT
        self.score_text = Text(Rect(vector2(20,20), vector2(150,50)), Game.defaultScoreText + str(self.score))
        self.score_text.justify = Text.justify_up
        self.score_text.align = Text.align_left
        self.childs.append(self.score_text)

        # EXIT BUTTON
        x, y = screen.get_size()
        exit_button = TextButton(vector2(20, y -70), vector2(150, 50), "Exit")
        exit_button.on_click = lambda game = self : game.on_exit_game()
        self.childs.append(exit_button)

        # WIN TEXT
        self.win_text = Text(Rect(vector2(0, 0), vector2(x,y)), "Congratulations!")
        self.childs.append(self.win_text)

        if rows != 0 and columns != 0:
            self.new_game(rows, columns)
        else:
            self.is_visible = False

    def new_game(self, columns, rows):
        #RESET GAME
        self.cards.clear()
        self.score = 0
        self.selected_cards.clear()
        self.wrong_attempts = 0
        self.score_text.text = Game.defaultScoreText + "0"
        self.win_text.is_visible = False

        #get window size
        sHeight = self.screen.get_height()
        sWidth = self.screen.get_width()

        #set cards size relative to screen
        self.card_size.y = (sHeight * 0.8) / rows
        self.card_size.x = (sHeight * 0.6) / columns

        #offset to center all cards
        offset = vector2()
        offset.x = (sWidth - ((columns -1) * self.cards_offset + columns * self.card_size.x)) / 2
        offset.y = (sHeight - ((rows -1) * self.cards_offset + rows * self.card_size.y)) / 2

        #instantiate cards
        for x in range(columns):
            for y in range(rows):
                #card position
                p = vector2()
                p.x = x * (self.cards_offset + self.card_size.x) + offset.x
                p.y = y * (self.cards_offset + self.card_size.y) + offset.y
                #instantiate
                c = FigureButton(p, self.card_size, str(y * columns + x))
                #define onclick
                # call select card as routine to prevent locking the application with a thread.sleep() 
                # and have a nice delay before hiding back or removing the cards
                c.on_click = lambda c=c : Routine.start_coroutine(self.select_card(c))
                self.cards.append(c)

        #mix them
        random.shuffle(self.cards)
        random.shuffle(self.cards) #twice to get a better mix

        #define available figures and colors
        colors = [(255, 0, 0), (0,255,0), (0,0,255), (255, 0, 255), (255,255,0), (0,255,255)]
        figures = [0,1,2]

        total = rows * columns

        #add colors and figures
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
        #Prevent misselection
        isSame = len(self.selected_cards) != 0 and self.selected_cards[0] == card
        hasTwo = len(self.selected_cards) >= 2
        if isSame or hasTwo:
            return

        #Show card content and add to pool
        card.set_shape_visible(True)
        self.selected_cards.append(card)

        #check if has two cards
        if len(self.selected_cards) == 2:
            
            #wait a bit before display result
            w = Routine.wait_for_seconds(1)
            r = True
            while r != False:
                yield True
                r = next(w, False)

            #Check result
            same_shape = self.selected_cards[0].shape == self.selected_cards[1].shape
            same_color = self.selected_cards[0].shape_color == self.selected_cards[1].shape_color

            if same_shape and same_color:  #RIGHT CARDS
                #remove cards from game
                for c in self.selected_cards:
                    self.cards.remove(c)
                self.on_correct()
            else:                          #WRONG CARDS
                #hide cards shapes
                for c in self.selected_cards:
                    c.set_shape_visible(False)
                self.on_wrong()

            #clear pool
            self.selected_cards.clear()

        #if has no more cards it means that game has ended... right???
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
        #YOU WON, NICE...
        self.win_text.is_visible = True
        self.cards.clear()
        
    def on_exit_game(self):
        #Back to menu - or whatever it is on self.on_exit....
        self.is_visible = False
        if(self.on_exit and callable(self.on_exit) == True):
            self.on_exit()

    def on_draw(self, screen):
        for c in self.cards:
            c.draw(screen)
