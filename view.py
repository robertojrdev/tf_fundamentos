class View:
    """
    Class to nest and draw objects,
    the children will not be drawn if the parent is not visible
    """
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
