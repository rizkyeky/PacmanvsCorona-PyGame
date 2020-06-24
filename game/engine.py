import model
import view

from settings import *

class Game:

    from pygame import init, time, mixer

    def __init__(self):
        
        self.init()
        self.state = "START"

        self.controller = Controller()
        
        self.screen = view.Screen()
        self.startMenu = view.StartGame()
        
        self.map = Map()        
        
        self.playMusic()
    
    def run(self):
        
        self.pacMan = model.PacMan(self.map.paths[0], speed=2)
        self.viruses = [model.Virus(self.map.paths[i*50+150], speed=1) for i in range(5)]
        
        self.score = view.Score()
        
        if self.state == "START":
            self.startGame()
        
        while self.state == "PLAYING":
             
            self.screen.showWall(self.map.walls)
            self.screen.showObj(self.pacMan)
            self.score.show()
            
            if self.getTime() % 10 == 0:
                self.score.update(10)
            
            for virus in self.viruses:
                self.screen.showObj(virus)
                virus.moveSearch(self.pacMan)
            
            self.pacMan.move(self.controller.key)
            
            for virus in self.viruses:
                if self.interact(self.pacMan, virus):
                    self.viruses.pop(self.viruses.index(virus))
                    self.state = "START"
                    self.startGame()
                    break
            
            self.pacMan.update()
            
            for virus in self.viruses:
                virus.update()
                
            self.screen.refresh()
            self.lockFPS(144)
            
            if self.controller.event == "quit":
                self.state = "CLOSE"
        
        if self.state == "CLOSE":
            self.close()

    def startGame(self):

        while self.state == "START":
            
            self.startMenu.show()
            self.mixer.music.play(-1)
            
            if self.controller.key == "space":
                self.state = "PLAYING"
            
            self.screen.refresh()
            self.lockFPS(30)
        
            if self.controller.event == "quit":
                self.state = "CLOSE"
                     
    def interact(self, char1, char2):
        return char1.rect.colliderect(char2.rect)     
    
    def lockFPS(self, fps):
        self.time.Clock().tick(fps)

    def getTime(self):
        return self.time.get_ticks()
    
    def close(self):
        from pygame import quit
        from sys import exit
        quit()
        exit()
    
    def playMusic(self, music=BACKSOUND):
        self.mixer.init()
        self.mixer.music.load(music)

class Controller:
    
    from pygame import event as ev, key as ky
    from pygame import QUIT, K_SPACE, K_RIGHT, K_LEFT, K_UP, K_DOWN
    
    def __getEvent(self):
        for event in self.ev.get():
            if event.type == self.QUIT:
                return "quit"
        else:
            return None
      
    event = property(__getEvent)

    def __getKey(self):

        arrow = self.ky.get_pressed()

        if arrow[self.K_LEFT]:
            return "left"
        elif arrow[self.K_RIGHT]:
            return "right"
        elif arrow[self.K_UP]:
            return "up"
        elif arrow[self.K_DOWN]:
            return "down"
        elif arrow[self.K_SPACE]:
            return "space"
        else:
            return False
   
    key = property(__getKey)

class Map():
   
    from numpy import array, empty
    
    def __init__(self):

        self.__matrix = self.array([[char for char in line if char != '\n'] for line in open(MAP_LEVEL1)])
        self.__maze = self.empty((20,40), dtype=object)
        
        self.__walls = list()
        self.__paths = list()
        
        self.__crateMaze()
    
    def __crateMaze(self):
        i = 0
        for y, row in enumerate(self.__matrix):
            for x, cell in enumerate(row):
                if cell == '#':
                    self.__maze[y,x] = model.Wall(i, (x,y), color=(0,0,255))
                    self.__walls.append(self.__maze[y,x])
                elif cell == '-':
                    self.__maze[y,x] = model.Path(i, (x,y), color=(0,0,255))
                    self.__paths.append(self.__maze[y,x])
                i += 1

        for y, row in enumerate(self.__maze):
            for x, cell in enumerate(row):
                if type(cell) is model.Path:
                    if type(self.__maze[y,x+1]) is model.Path:
                        cell.neighbors["right"] = self.__maze[y,x+1]
                    if type(self.__maze[y,x-1]) is model.Path:
                        cell.neighbors["left"] = self.__maze[y,x-1]
                    if type(self.__maze[y-1,x]) is model.Path:
                        cell.neighbors["up"] = self.__maze[y-1,x]
                    if type(self.__maze[y+1,x]) is model.Path:
                        cell.neighbors["down"] = self.__maze[y+1,x]
    
    def __getWalls(self):
        return self.__walls
    def __getPaths(self):
        return self.__paths

    walls = property(__getWalls)
    paths = property(__getPaths)
