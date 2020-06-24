from abc import ABC, abstractmethod, abstractproperty

from pygame.math import Vector2 as vec
from settings import *

class ObjectGeneral(object):
    
    _size = None
    _pos = None
    
    def __init__(self, position:vec, size):
        self._pos = position
        self._size = size
    
    def _getSize(self):
        return self._size
    def _setSize(self, val):
        self._size = val
    
    def _getPos(self):
        return self._pos
    def _setPos(self, val):
        self._pos = val
    
    size = property(_getSize)
    pos = property(_getPos)
    
class ObjectGame(ABC):
 
    _source = None
    _dest = None
    
    def __init__(self):
        super(ObjectGame, self).__init__()
        
    @abstractproperty    
    def source(self):
        pass 
    
    @abstractproperty    
    def dest(self):
        pass

    @abstractmethod
    def _setSource(self):
        pass
    @abstractmethod
    def _getSource(self):
        pass
    
    @abstractmethod
    def _setDest(self):
        pass
    @abstractmethod
    def _getDest(self):
        pass

class Text(ObjectGeneral, ObjectGame):
    
    from pygame import font
    
    def __init__(self, text:str, position:vec, size:tuple,
                 color:tuple=(255, 255, 255), style:str=FONT_STYLE):
        ObjectGeneral.__init__(self, position, size)
        
        self.__text = text
        self.__color = color
        self.__style = style

        self.__setFont()
        
        self._setSource()
        self._setDest()
    
    def _setSource(self):
        self._source = self.__font.render(self.__text, True, self.__color)
    def _getSource(self):
        return self._source
    
    def _setDest(self):
        self._dest = self._source.get_rect(center=self._pos)
    def _getDest(self):
        return self._dest
    
    def update(self, text):
        self.__text = text
        self._setSource()
    
    source = property(_getSource)
    dest = property(_getDest)
    
    def __setFont(self):
        self.__font = self.font.Font(self.__style, self._size)
    
class Title(Text):
    
    def __init__(self, text:str):
        Text.__init__(self, text, (WIDTH//2, HEIGHT//2), 80)

class Subtitle(Text):
    
    def __init__(self, text:str):
        Text.__init__(self, text, (WIDTH//2, HEIGHT//2 + 100), 30)

class Character(ObjectGeneral, ObjectGame):
    
    from pygame import image
    from random import choice
    
    __isMove = None
    __key = None
    
    def __init__(self, file:str, path, size:int, speed:int):
        ObjectGeneral.__init__(self, vec(path.rect.center), size)
        
        self.__imgFile = file
        self.__speed = speed
        self._path = path
    
        self._setSource()
        self.__setRect()
        self._setDest()
        
        self.__setDir()
        self.__setPrevKey()
        self.__setPrevPath()
        
    def _setSource(self):
        self._source = self.image.load(self.__imgFile)
    def _getSource(self):
        return self._source
    
    def _setDest(self):
        self._dest = self.__rect
    def _getDest(self):
        return self._dest
 
    source = property(_getSource)
    dest = property(_getDest)
    
    def __setRect(self):
        self.__rect = self._source.get_rect(center=self._pos)
    def __getRect(self):
        return self.__rect
    
    def __setDir(self):
        self.__dir = vec(0,0)
    def __getDir(self):
        return self.__dir
    
    def __setPrevKey(self):
        self._prevkey = None
    
    def __setPrevPath(self):
        self._prevpath = self._path 
        
    def __getPath(self):
        return self._path   
        
    rect = property(__getRect)
    path = property(__getPath)
    direction = property(__getDir, __setDir)
    
    def update(self):
        self.__setRect()
        self._setDest()  
    
    def _moveRight(self):
        
        if "right" in self._path.neighbors:
            path = self._path.neighbors["right"]
            
            if self._pos.x <= path.rect.center[0]:
                if round(self._pos.x) == path.rect.center[0]:
                    self._pos.x = path.rect.center[0]
                    self._path = path
                else:
                    self._pos += vec(1, 0) * self.__speed
            return True
        
        elif "right" not in self._path.neighbors:
            return False

    def _moveLeft(self):
        
        if "left" in self._path.neighbors:
            path = self._path.neighbors["left"]
            
            if self._pos.x >= path.rect.center[0]:
                if round(self._pos.x) == path.rect.center[0]:
                    self._pos.x = path.rect.center[0]
                    self._path = path
                else:
                    self._pos += vec(-1, 0) * self.__speed
            return True        
            
        elif "left" not in self._path.neighbors:
            return False
    
    def _moveUp(self):
        
        if "up" in self._path.neighbors:
            path = self._path.neighbors["up"]
            
            if self._pos.y >= path.rect.center[1]:
                if round(self._pos.y) == path.rect.center[1]:
                    self._pos.y = path.rect.center[1]
                    self._path = path  
                else:
                    self._pos += vec(0, -1) * self.__speed
            return True
        
        elif "up" not in self._path.neighbors:
            return False
    
    def _moveDown(self):
        
        if "down" in self._path.neighbors:
            path = self._path.neighbors["down"]
            
            if self._pos.y <= path.rect.center[1]:
                if round(self._pos.y) == path.rect.center[1]:
                    self._pos.y = path.rect.center[1]
                    self._path = path   
                else:  
                    self._pos += vec(0, 1) * self.__speed
            return True
        
        elif "down" not in self._path.neighbors:
            return False
    
    def moveSearch(self, char):
        from ai import aStar, bestFirstSearch
        
        if self._pos != char.pos:

            if self.__isMove:
                if self.__key == "left":
                    self.__isMove = self._moveLeft()
                elif self.__key == "right":
                    self.__isMove = self._moveRight()
                elif self.__key == "up":
                    self.__isMove = self._moveUp()
                elif self.__key == "down":
                    self.__isMove = self._moveDown()

                self._prevkey = self.__key
            
            else:
                bestpaths = bestFirstSearch(self._path, char.path, 10)
                
                if len(bestpaths) > 1:
                    for key, path in bestpaths[0].neighbors.items():
                        if path == bestpaths[1]:
                            self.__key = key
                            self.__isMove = True
                            break
                else:
                    self.__isMove = False
                
            if self._prevpath != self._path:
                if all(key in self._path.neighbors for key in ("left", "right", "up", "down")):
                    self.__isMove = False
                elif 3 == [key in self._path.neighbors for key in ("left", "right", "up", "down")].count(True):
                    self.__isMove = False
                    
                self._prevpath = self._path
                

class PacMan(Character):

    def __init__(self, position:tuple, speed:int):
        self.__imgPath = PACMAN
        self.__isMove = False

        Character.__init__(self, self.__imgPath, position, CHARACTER_SIZE, speed)
        
    def move(self, key):
        
        if self.__isMove:
            key = False
        
        if self._prevpath != self._path:
            self._prevpath = self._path
            self._prevkey = False
            self.__isMove = False    
        
        if self._prevkey != key and key != False:
            self._prevkey = key   
        
        if self._prevkey in ("left", "right", "up", "down"):     
            if self._prevkey == "left":
                self.__isMove = self._moveLeft()
            
            elif self._prevkey == "right":
                self.__isMove = self._moveRight()
            
            elif self._prevkey == "up":
                self.__isMove = self._moveUp()
            
            elif self._prevkey == "down":
                self.__isMove = self._moveDown()
                
class Virus(Character):
   
    from random import choice
    
    def __init__(self, position:tuple, speed:int):
        self.__imgPath = VIRUS
        self.__isMove = True
        
        Character.__init__(self, self.__imgPath, position, CHARACTER_SIZE, speed)
        self.__setRanKey()

    def __setRanKey(self):  
        self.__rankey = self.choice(list(self._path.neighbors))
    
    def randomMove(self):
        
        if self.__isMove:
             
            if self.__rankey == "left":
                self.__isMove = self._moveLeft()
            elif self.__rankey == "right":
                self.__isMove = self._moveRight()
            elif self.__rankey == "up":
                self.__isMove = self._moveUp()
            elif self.__rankey == "down":
                self.__isMove = self._moveDown()
            
            self._prevkey = self.__rankey
        
        elif not self.__isMove:
            
            ls = list(self._path.neighbors)
            
            if self._prevkey == "right" and "left" in ls:
                ls.pop(ls.index("left"))
            elif self._prevkey == "left" and "right" in ls:
                ls.pop(ls.index("right"))
            elif self._prevkey == "up" and "down" in ls:
                ls.pop(ls.index("down"))
            elif self._prevkey == "down" and "up" in ls:
                ls.pop(ls.index("up"))
                
            self.__rankey = self.choice(ls)
            self.__isMove = True
            
        if self._prevpath != self._path:
            if all(key in self._path.neighbors for key in ("left", "right", "up", "down")):
                self.__isMove = self.choice((True, False))
            elif 3 == [key in self._path.neighbors for key in ("left", "right", "up", "down")].count(True):
                self.__isMove = self.choice((True, False))
            self._prevpath = self._path
    
class Shape(ObjectGeneral):
    
    def __init__(self, position:vec=vec(0,0), size:int=0, color:tuple=(255,255,255)):
        ObjectGeneral.__init__(self, position, size)
        
        self.__setColor(color)
    
    def __setColor(self, val):
        self.__color = val
    
    def __getColor(self):
        return self.__color
    
    color = property(__getColor)
    

class Path(Shape):
       
    from pygame import Rect
    
    def __init__(self, num:int, position:tuple, size:int=GRID_SIZE, color:tuple=(0,0,0)): 
        Shape.__init__(self, vec(position[0] * size, position[1] * size), size, color)
        
        self.__grid = position
        self.__num = num
        
        self.__parent = None
        self.__g = 0
        self.__h = 0
        self.__f = 0
        
        self.__setRect()
        self.__setNeighbors()
    
    def __repr__(self):
        return "p%d" % (self.__num)

    def __eq__(self, other):
        if other == None:
            return False
        return self.__num == other.num
    
    def __ne__(self, other):
        if other == None:
            return False
        return self.__num != other.num
    
    def __lt__(self, other):
        return self.__f < other.__f
    
    def __getRect(self):
        return self.__rect
    def __setRect(self):
        self.__rect = self.Rect(self._pos.x, self._pos.y, self._size, self._size)
    
    def __getNum(self):
        return self.__num
    def __getGrid(self):
        return self.__grid
    
    def __getNeighbors(self):
        return self.__neighbors
    def __setNeighbors(self):
        self.__neighbors = dict()
    
    def __getParent(self):
        return self.__parent
    def __setParent(self, val):
        self.__parent = val
    
    def __getH(self):
        return self.__h
    def __setH(self, val):
        self.__h = val
        
    def __getG(self):
        return self.__g
    def __setG(self, val):
        self.__g = val
        
    def __getF(self):
        return self.__f
    def __setF(self, val):
        self.__f = val
    
    rect = property(__getRect)
    num = property(__getNum)
    neighbors = property(__getNeighbors)
    grid = property(__getGrid)
    
    parent = property(__getParent, __setParent)
    h = property(__getH, __setH)
    g = property(__getG, __setG)
    f = property(__getF, __setF)
    
class Wall(Shape):
    
    from pygame import Rect
    
    def __init__(self, num:int, position:tuple, size:int=GRID_SIZE, color:tuple=(0,0,0)): 
        Shape.__init__(self, vec(position[0] * size, position[1] * size), size, color)
        
        self.__grid = position
        self.__num = num
        
        self.__setRect()
        
    def __repr__(self):
        return "w%d" % (self.__num)    
    
    def __setRect(self):
        self.__rect = self.Rect(self._pos.x, self._pos.y, self._size, self._size)
    def __getRect(self):
        return self.__rect
    
    rect = property(__getRect)
    
class Circle(Shape):

    from pygame import Rect

    def __init__(self, path, size:int=15, color:tuple=(0,0,0)):
        Shape.__init__(self, vec(path.rect.center[0], path.rect.center[1]), size, color)
        self.__setRect()
    
    def __setRect(self):
        self.__rect = self.Rect(self._pos.x, self._pos.y, self._size, self._size)
    def __getRect(self):
        return self.__rect

    rect = property(__getRect)
    