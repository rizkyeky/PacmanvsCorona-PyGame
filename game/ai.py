from numpy import math

def ManhattanDistance(pos1, pos2):
    return abs(pos1.x-pos2.x) + abs(pos1.y-pos2.y)
def ChebyshevDistance(pos1, pos2):
    return max(abs(pos1.x-pos2.x), abs(pos1.y-pos2.y))
def EuclidianDistance(pos1, pos2):    
    return math.sqrt(((pos1.x-pos2.x) ** 2) + ((pos1.y-pos2.y) ** 2))
    
def aStar(startPath, goalPath, limit=100):
    from heapq import heapify, heappush, heappop
    
    mem = []
    fringe = []
    
    heapify(fringe)
    heappush(fringe, startPath)
    
    loop = 0    
    isfound = False
    while len(fringe) > 0 and not isfound:
        currPath = heappop(fringe)
        mem.append(currPath)
        
        if currPath == goalPath or loop == limit:
            isfound = True
        else:
            for neighbor in currPath.neighbors.values():
                
                if not neighbor in mem:
                    neighbor.parent = currPath
                    
                    neighbor.g = currPath.g + ChebyshevDistance(currPath.pos, neighbor.pos)
                    neighbor.h = ChebyshevDistance(neighbor.pos, goalPath.pos)
                    neighbor.f = neighbor.g + neighbor.h
                    
                    if not any([neighbor == node and neighbor.f >= node.f for node in fringe]):
                        heappush(fringe, neighbor)
                    
        loop += 1
                
    # print("loop:", loop, end=' ')
    
    paths = []    
    while currPath != startPath:
        paths.append(currPath)
        currPath = currPath.parent
    
    paths.append(startPath)
    # print("len:", len(paths))
    return paths[::-1]

def bestFirstSearch(startPath, goalPath, limit=100):
    from numpy import math
    from heapq import heapify, heappush, heappop

    mem = [] 
    fringe = []
    
    heapify(fringe)
    heappush(fringe, startPath)
    
    loop = 0
    isfound = False
    while len(fringe) > 0 and not isfound:
        currPath = heappop(fringe)
        mem.append(currPath)
        
        if currPath == goalPath or loop == limit:
            isfound = True
        else:
            for neighbor in currPath.neighbors.values():
                
                if not neighbor in mem:
                    neighbor.parent = currPath
                    
                    neighbor.f = ManhattanDistance(neighbor.pos, goalPath.pos)
                    
                    if not any([neighbor == node and neighbor.f >= node.f for node in fringe]):
                        heappush(fringe, neighbor)
        
        loop += 1
        
    # print("loop:", loop, end=' ')
    
    paths = []    
    while currPath != startPath:
        paths.append(currPath)
        currPath = currPath.parent
    
    paths.append(startPath)
    # print("len:", len(paths))
    return paths[::-1]
