import sys
import random
import math
import csv
import time
import copy

'''global helper variables'''
debug = False
printing = True
'''Global data variables'''


'''Necesary Classes'''
class node:
    def __init__(self, name, xCoord, yCoord):
        self.name = name
        self.coordinates = (int(xCoord), int(yCoord))
        self.linkedNodes = []

    def distance(self, node):
        return math.sqrt(math.pow((self.coordinates[0] - node.coordinates[0]), 2) + math.pow((self.coordinates[1]- node.coordinates[1]), 2))

    def __eq__(self, other):
        return self.name == other.name
    def __hash__(self):
        return hash(self.name)

class indiviual:

    def getTotalWeight(self, tour):
        weight = 0
        for x in range(len(tour)-1):
            weight += tour[x].distance(tour[x+1])
        
        return weight

    def __init__(self, tour):
        self.tour = tour
        self.weight = self.getTotalWeight(tour)


    def __lt__(self, other):
        return self.weight < other.weight
    def __le__(self, other):
        return self.weight <= other.weight
    def __gt__(self, other):
        return self.weight > other.weight
    def __ge__(self, other):
        return self.weight >= other.weight
    def __eq__(self, other):
        return self.weight == other.weight
    def __ne__(self, other):
        return self.weight != other.weight
    

def main(args):
    nodes = readFromFile("a280.tsp")
    genetic(nodes, 1000, 100, .1, 10)


    return None


def genetic(nodes, iterations, populationSize, mutationRate, eliteSize):

    '''
    1.create population
    2.score and sort initial population
    3.select individuals to mate
    4.breed and mutate
    5.repeat
    '''

    population = initializePopulation(nodes, populationSize)

    for x in range(iterations):
        sortedPopulation = sortPopulation(population)
        if debug:
            print("**************************\nsorted population:")
            for x in sortedPopulation:
                print("length of individual: " + str(len(x.tour)))
                [print(n.name, end="-") for n in x.tour]
                print("weight: " + str(x.weight), end = '\n')

        #write results to csv file
        with open('Genetic.csv', 'a') as file : 
                    writer = csv.writer(file)
                    writer.writerow([x, sortedPopulation[0].weight])
        if printing:
            print("Current iteration: " + str(x))
            print("Current best solution weight: " + str(sortedPopulation[0].weight))

        population = makeNewPopulation(sortedPopulation, eliteSize, mutationRate)
        if debug:
            print("**************************\nnew population length of " + str(len(population)) + " :")
            for x in population:
                print("length of individual: " + str(len(x.tour)))
                [print(n.name, end="-") for n in x.tour]
                print("weight: " + str(x.weight), end = '\n')





    return None

def createIndividual(nodes):
    tour = random.sample(nodes,len(nodes))
    tour.append(copy.deepcopy(tour[0]))
    return indiviual(tour)

def initializePopulation(nodes, size):
    population = []
    for x in range(size):
        population.append(createIndividual(nodes))

    return population

def sortPopulation(population):
    return sorted(population)

def makeNewPopulation(population, eliteSize, mutationRate):
    '''Work with idea of elitism'''
    '''Tournament selection for rest of population'''
    #establish best part of 
    newPopulation = []
    newPopulation.extend(population[0:eliteSize+1])

    #establish parents, using tournament selection
    while len(newPopulation) < len(population):
        p1, p2 = None, None
        tournamentSize = 8
        sample = random.sample(population, tournamentSize)
        sortedSample = sorted(sample)
        p1 = sortedSample[0]
        if random.random() <= (1/tournamentSize):
            p2 = sortedSample[2]
        else:
            p2 = sortedSample[1]
        
        newPopulation.append(breed(p1,p2,mutationRate))
    
    return newPopulation

def breed(p1, p2, mutationRate):
    newTour = []
    cpyP1 = copy.deepcopy(p1)
    cpyP2 = copy.deepcopy(p2)
    del cpyP1.tour[-1]
    del cpyP2.tour[-1]

    index1 = random.randint(0, len(cpyP1.tour)-1)
    index2 = random.randint(0, len(cpyP2.tour)-1)
    while index2 == index1: 
        index2 = random.randint(0, len(cpyP1.tour)-1)

    start = min(index1, index2)
    end = max(index1, index2)
    

    p2PartialSet = cpyP2.tour[start:end]
    p1PartialSet = [node for node in cpyP1.tour if node not in p2PartialSet]
    newTour = p1PartialSet + p2PartialSet

    newTour.append(copy.deepcopy(newTour[0]))
    
    newIndividual = indiviual(newTour)

    #chance of mutation 
    if random.random() <= mutationRate:
        newIndividual = mutate(newIndividual)

    return newIndividual

def mutate(ind):
    chance = random.random()
    newTour = copy.deepcopy(ind.tour)
    
    if chance <= 0.50:
        #swap
        randIndex1 = random.randint(0, len(newTour)-2)
        randIndex2 = random.randint(0, len(newTour)-2)
        while randIndex1 == randIndex2:
            randIndex2 = random.randint(0, len(newTour)-2)
        
        newTour[randIndex1], newTour[randIndex2] = newTour[randIndex2], newTour[randIndex1]

    else:
        #reverse subsequence
        randIndex1 = random.randint(0, len(newTour)-2)
        randIndex2 = random.randint(0, len(newTour)-2)
        
        while randIndex1 == randIndex2:
            randIndex2 = random.randint(0, len(newTour)-2)

        start = min(randIndex1, randIndex2)            
        end = max(randIndex1, randIndex2)

        newTour[start:end] = newTour[start:end][::-1]
        

    return indiviual(newTour)






'''global helper methods'''
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

if __name__ == '__main__':
    main(sys.argv[1:])