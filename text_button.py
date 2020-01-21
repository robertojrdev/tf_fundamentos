from button import Button
from text import Text
from rect import Rect

class TextButton(Button):
    """A button with text
    
    to change the text you must use instance.text.text (the instance.text is an text object)
    """
    def __init__(self, position, size, text = "Button", color = (255,255,0)):
        super().__init__(position, size, color)
        self.outline = 2
        self.text = Text(Rect(position, size), text, color=(self.color))
        self.childs.append(self.text)
