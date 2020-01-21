import pygame
import time
from menu import Menu
from input import Input
from game import Game
from routines import Routine

END = False

def main():
    global END
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1200 ,700))

    delta_time = 0
    
    views = []

    #Create a Game view
    game = Game(screen)
    views.append(game)

    #Create a Menu view
    menu = Menu(screen, game)
    views.append(menu)

    lastTime = time.time()
    while(END == False):
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

        #Update mouse inputs
        Input.update(evt)

        #Paint Background
        screen.fill((0,20,20))
        
        #Draw views
        for v in views:
            v.draw(screen)

        #Display result on screen
        pygame.display.flip()

        #Update delta _time
        delta_time = time.time() - lastTime
        lastTime = time.time()

        #call coroutines
        Routine.delta_time = delta_time
        for r in Routine.routines:
            v = next(r, False)
            if(v == False) :
                Routine.routines.remove(r)

def exit():
    global END
    END = True

#Call main, because Diogo told me to do so
main()