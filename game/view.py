from settings import *

class Display(object):
    
    from pygame import display, draw
      
    def __init__(self):
        self._setSurface()
    
    def _getSurface(self):
        return self._surface
    def _setSurface(self):
        self._surface = self.display.get_surface()
        
    surface = property(_getSurface)
        
    def showObj(self, *objs):
        for obj in objs:
            self._surface.blit(obj.source, obj.dest)
            
    def showWall(self, walls):
        for wall in walls:            
            self.draw.rect(self._surface, wall.color, wall.rect, 2)
    
    def drawPaths(self, paths, color):
        for i, path in enumerate(paths):
            if i < len(paths)-1:
                self.draw.line(self._surface, color, path.rect.center, paths[i+1].rect.center, 2)
          

class Screen(Display):
    
    def __init__(self):
        Display.__init__(self)
          
        self.__title = TITLE
        self.__size = (WIDTH, HEIGHT)
        self.__color = (0,0,0)

        self.__setMode()
        self.__setTitle()
    
    def __setMode(self):
        self._surface = self.display.set_mode(self.__size)
        
    def __setTitle(self):
        self.display.set_caption(self.__title)
        
    def refresh(self):
        self.display.update()
        self._surface.fill(self.__color)
    
class StartGame(Display):
    
    from model import Title, Subtitle
     
    def __init__(self):
        Display.__init__(self)
    
        self.__titleText = self.Title(TITLE)
        self.__subtitleText = self.Subtitle("Press Space to Start")
     
    def show(self):
        Display.showObj(self, self.__titleText, self.__subtitleText)

class Score(Display):

    from model import Text
    
    def __init__(self):
        Display.__init__(self)
        
        self.__number = 0                 
        self.__text = self.Text("score: " + str(self.__number), (50, HEIGHT-25), 20)    
    
    def update(self, val):
        self.__number += val
        self.__text.update("score: " + str(self.__number))
    
    def show(self):
        Display.showObj(self, self.__text)
