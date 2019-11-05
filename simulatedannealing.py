import sys
import math
import copy
import random
import csv
import time
'''Global Helper variables'''
debug = False
printing = True
'''Cooling Schedules'''
linear = False
quadratic = False
exponential = False
logarithmic = True
'''Global data variables'''
initTemperature = 50
alpha = 1
iterations = 10000

class node:
    def __init__(self, name, xCoord, yCoord):
        self.name = name
        self.coordinates = (int(xCoord), int(yCoord))
        self.linkedNodes = []

    def distance(self, node):
        return math.sqrt(math.pow((self.coordinates[0] - node.coordinates[0]), 2) + math.pow((self.coordinates[1]- node.coordinates[1]), 2))
    


def main(args):
    temp = 100
    '''This is all testing for setting up the paths and the nodes'''
    nodes = []
    solutions = []

    nodes = readFromFile("a280.tsp")
    solutions.append(generateFirstSolution(nodes))
    # weight = getTotalWeight(solutions[0])
   

    if debug:
        [print(n.name, end = "-") for n in solutions[0]]
        print("", end = '\n')
    # if debug: 
    #     print("Total weight: " + str(weight))
    
    for x in range(iterations):
        origSolution = solutions[-1]
        alteredSolution = alterSolution(origSolution)
        alterSolutionWeight = getTotalWeight(alteredSolution)

        if debug:
            [print(n.name, end = "-") for n in alteredSolution]
            print("", end = '\n')
        if debug:
            print("Total weight: " + str(alterSolutionWeight))

        finalSolution = compareSolution(origSolution, alteredSolution, temp)
        solutions.append(finalSolution)

        with open('SimulatedAnnealing.csv', 'a') as file : 
                    writer = csv.writer(file)
                    writer.writerow([x, getTotalWeight(finalSolution)])
        temp = cool(x, temp)
        if printing: print("temp: " + str(temp))
        if printing:
            [print(n.name, end = "-") for n in finalSolution]
            print("", end = '\n')
            print("score: " + str(getTotalWeight(finalSolution)))
    


def generateFirstSolution(nodes):
    solution = random.sample(nodes, len(nodes))
    return solution

def alterSolution(solution):
    tempSolution = copy.deepcopy(solution)
    randIndex1 = random.randint(0, len(tempSolution)-2)
    randIndex2 = random.randint(0, len(tempSolution)-2)
    while randIndex1 == randIndex2:
        randIndex2 = random.randint(0, len(tempSolution)-2)

    tempSolution[randIndex1], tempSolution[randIndex2] = tempSolution[randIndex2], tempSolution[randIndex1]
    
    if randIndex1 == 0 or randIndex2 == 0:
        del tempSolution[-1]
        tempSolution.append(copy.deepcopy(tempSolution[0]))

    return tempSolution
    
def compareSolution(originalSolution, newSolution, temp):
    originalScore = getTotalWeight(originalSolution)
    newScore = getTotalWeight(newSolution)

    if newScore <= originalScore:
         return newSolution
    else:
        #check for acceptance
        if accept(temp, originalScore, newScore):
            return newSolution
        else:
            return originalSolution

def accept(temp, originalSolutionScore, newSolutionScore):
    if random.random() <= math.exp(-abs((originalSolutionScore-newSolutionScore)/temp)):
        return True
    
    return False
    

'''Helper methods'''
def readFromFile(fileName):
    nodes = set()
    with open(fileName, 'r') as f:
        curLine = f.readline()
        while "EOF" not in curLine:
            stripped = curLine.strip().split()
            if len(stripped) == 3 and stripped[1].isdigit() and stripped[2].isdigit:
                nodes.add(node(stripped[0], stripped[1], stripped[2]))
            curLine = f.readline() 
    return nodes  

def getTotalWeight(tour):
    weight = 0
    for x in range(len(tour)-1):
        weight += tour[x].distance(tour[x+1])
    
    return weight

def cool(iteration, temp):
    global initTemperature
    global alpha

    if linear: return initTemperature/(1 + alpha * iteration)
    if quadratic: return initTemperature/(1 + alpha * math.pow(iteration, 2))
    if exponential: return initTemperature* math.pow(.8, iteration)
    if logarithmic: return initTemperature/(1 + alpha * math.log(iteration + 1))



if __name__ == '__main__':
    main(sys.argv[1:])