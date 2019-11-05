import sys
import math
import copy

'''Helper Globals'''
debug = False
printing = True
'''Data Globals'''
tour = []


class node:
    def __init__(self, name, xCoord, yCoord):
        self.name = name
        self.coordinates = (int(xCoord), int(yCoord))
        self.linkedNodes = []

    def distance(self, node):
        return math.sqrt(math.pow((self.coordinates[0] - node.coordinates[0]), 2) + math.pow((self.coordinates[1]- node.coordinates[1]), 2))
    
    def addNode(self, child):
        self.linkedNodes.append(child)
    


    def __eq__(self, other):
        return self.name == other.name

class edge:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight



def main(args):
    #edges is a dictionary with all of the edges
    #key is node1 name, node 2 name, 
    #value is edge weight 
    nodes = []
    edges = []
    #read from file:
    nodes = readFromFile("a280.tsp")

    if debug: print(str(len(nodes)) + " nodes")
    if debug:
        for x in nodes:
            print("node: ", x.name, "coordinates: ", x.coordinates)

    #start finding MST
    edges = mst(nodes)
    if debug: print("\n\n"+ str(len(edges)), "Edges:")
    if debug: 
        for x in edges:
            print("edge name: " + x.name + " weight: " + str(x.weight))


    #generate Euler Tour
    #list of vertices visited in order

    eulerianTour(nodes, nodes[0])
    tour.append(nodes[0].name)
    if printing: print(tour)
    weight = getTotalWeight(tour, nodes)
    if printing: print("Total Weight: " + str(weight))


def readFromFile(fileName):
    nodes = []
    with open(fileName, 'r') as f:
        curLine = f.readline()
        while "EOF" not in curLine:
            stripped = curLine.strip().split()
            if len(stripped) == 3 and stripped[1].isdigit() and stripped[2].isdigit:
                nodes.append(node(stripped[0], stripped[1], stripped[2]))
            curLine = f.readline() 
    return nodes  


def mst(nodes):
    visitedNodes = [nodes[0]]
    edges = []
    unvisitedNodes = copy.deepcopy(nodes[1:])

    while (len(visitedNodes)) < len(nodes):
        newClosestSet = findClosestNode(visitedNodes, unvisitedNodes)
        edges.append(edge(newClosestSet[0].name + "," + newClosestSet[1].name, newClosestSet[0].distance(newClosestSet[1])))
        visitedNodes.append(newClosestSet[1])
        unvisitedNodes.remove(newClosestSet[1])

    for e in edges:
        name = e.name.split(',')
        getNode(nodes, name[0]).addNode(getNode(nodes, name[1]))
            

    return edges



def findClosestNode(visitedNodes, unvisitedNodes):
    closestNode = node("-1", 0, 0)
    originNode = node("-1", 0, 0)
    for origin in visitedNodes:
        for destination in unvisitedNodes:
            if closestNode.name == "-1" or origin.distance(destination) <= originNode.distance(closestNode):
                originNode = origin
                closestNode = destination
    return [originNode, closestNode]

def eulerianTour(nodes, n):
    
    tour.append(n.name)

    for linkedNode in n.linkedNodes:
        eulerianTour(nodes, linkedNode)

def traverseEdges(edges):
    bigTour = []
    bigTour.append(edges[0].name.split(',')[0])
    for x in range(edges):
        bigTour.append()


def getTotalWeight(tour, nodes):
    weight = 0
    for x in range(len(tour)-1):
        weight += getNode(nodes, tour[x]).distance(getNode(nodes, tour[x+1]))
    
    return weight
    
    
def getNode(nodes, name):
    for n in nodes:
        if n.name == name:
            return n
    
    return None



if __name__ == '__main__':
    main(sys.argv[1:])