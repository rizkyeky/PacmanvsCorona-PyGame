# Import model dan view
import model
import view
import engine
from pygame import init, time
from settings import *
from ai import *

from numpy import loadtxt, array, empty, append
matrix = array([[char for char in line if char != '\n'] for line in open(MAP_LEVEL1)])
maze = empty((20,40), dtype=object)

walls = []
paths = []

i = 0
for y, row in enumerate(matrix):
    for x, cell in enumerate(row):
        if cell == '#':
            maze[y,x] = model.Wall(i, (x,y), color=(0,0,255))
            walls.append(maze[y,x])
        elif cell == '-':
            maze[y,x] = model.Path(i, (x,y), color=(0,0,255))
            paths.append(maze[y,x])
        i += 1

for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if type(cell) is model.Path:
            if type(maze[y,x+1]) is model.Path:
                cell.neighbors["right"] = maze[y,x+1]
            if type(maze[y,x-1]) is model.Path:
                cell.neighbors["left"] = maze[y,x-1]
            if type(maze[y-1,x]) is model.Path:
                cell.neighbors["up"] = maze[y-1,x]
            if type(maze[y+1,x]) is model.Path:
                cell.neighbors["down"] = maze[y+1,x]

init()
                    
screen = view.Screen(TITLE, (WIDTH, HEIGHT))
state = "PLAYING"

controller = engine.Controller()
pacMan = model.PacMan(paths[0], speed=2)
virus = model.Virus(paths[381], speed=1)

starPath = aStar(paths[0], paths[381])
bestPath = bestFirstSearch(paths[0], paths[381])

while state == "PLAYING":
            
    screen.showWall(walls)
    screen.drawPaths(bestPath, (0,255,0))
    screen.drawPaths(starPath, (255,0,0))
    
    screen.showObj(pacMan)
    screen.showObj(virus)
    
    pacMan.move(controller.key)  
    pacMan.update()
    
    screen.refresh()
    time.Clock().tick(120)
    
    if controller.event == "quit":
        state = "CLOSE"

quit()