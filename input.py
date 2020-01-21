import pygame

class Input:
    get_mouse = False
    get_mouse_down = False
    get_mouse_up = False

    @staticmethod
    def update(evt):
        """        
        Arguments:
            evt {pygame events} -- get it from pygame.event.get()
        """
        
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
