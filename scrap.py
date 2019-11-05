def mst(nodes):
    #will return list of edges
    #uses prims algorithm
    visited = []
    visited.append(nodes[0])
    unVisitedNodes = copy.deepcopy(nodes[1:])
    edges = []
    nodes.remove(nodes[0])
    closestNode = node("-1", -1,-1)
    closestEdge = edge("None", -1)
    while(len(visited) < len(nodes)):
        print("length of visited: ", str(len(visited)), " length of nodes: ", str(len(nodes)))
        for vertex in visited:
            tempClosestNode = findClosestNode(vertex, unVisitedNodes)
            print("tempClosestNode - Name: ", tempClosestNode.name, " coord: ", str(tempClosestNode.coordinates))
            if closestNode.name == "-1" or tempClosestNode.distance(vertex) < closestNode.distance(vertex):
                print("Old edge weight: " + str(closestEdge.weight) + " newEdgeWeight: " + str(vertex.distance(tempClosestNode) ))
                closestNode = tempClosestNode
                closestEdge = edge(vertex.name + "," + closestNode.name, vertex.distance(closestNode))

        print("CloseestNode - Name: ", closestNode.name, " coord: ", str(closestNode.coordinates))
        visited.append(closestNode)
        unVisitedNodes.remove(closestNode)
        edges.append(closestEdge)

    return edges

def findClosestNode(vertex, unVisitedNodes):
    #given list of all nodes as well as the list of unvisted nodes, return vertex closest to current node
    closestNode = node("-1", 0,0)
    print("Inside find closest node")
    print("Length of unvisited nodes: ", str(len(unVisitedNodes)))
    for v in unVisitedNodes:
        if closestNode.name == "-1" or vertex.distance(v) < vertex.distance(closestNode):
            print("new closest node to ", vertex.name, ": ", v.name)
            closest = v

    print("returning closest node: ", closest.name, " coord: ", str(closest.coordinates), " is closest to node: ", vertex.name)
    return closest


  def eulerianTour(edges):
    #generate the double edges
    #go in reverse so we can get a directed graph
    #initial edges remain in same order
    tempEdges = copy.deepcopy(edges)
    for tempEdge in tempEdges: 
        name = tempEdge.name.split(",")
        edges.append(edge(name[1]+ ","+ name[0], tempEdge.weight))

    if debug:
        print("**************************\nEulerian Tour, length " + str(len(edges)) + " :")
        for x in edges:
            print("edge name: " + x.name + " weight: " + str(x.weight))

    #traverse Eulerian Tour
    # tour = []
    # name = edges[0].name
    # x =0
    # while (len(tour) < 2 * len(edges)):
    #     name = name.split(",")
    #     tour.append(name[0])
    #     x += 1
    #     name = edges[x]


    # if debug:
    #     print("**************************\nEulerian Tour vertices, length " + str(len(edges)) + " :")
    #     for x in tour:
    #         print("vertex name: " + x)


    
'''    
    testing for breed
    ind = breed(sortedPopulation[0], sortedPopulation[1], 0)
    if debug:
        print("**************************\nindividual :")
        print("length of individual: " + str(len(x.tour)))
        [print(n.name, end="-") for n in ind.tour]
        print("\nweight: " + str(x.weight), end = '\n')
        
'''