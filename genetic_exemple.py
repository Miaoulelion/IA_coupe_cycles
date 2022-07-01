
import networkx as nx
import math
from random import *
import random

#from scipy.fftpack import ss_diff



#Génération d'un grapge orienté alétaoire selon le modèle Erdős–Rényi model

D = nx.erdos_renyi_graph(n=10, p=0.3, seed=10, directed=True)
#print(D.nodes)
#print(D.edges)


#trouver un cycle
#print("Voici les cycles")





#Fonction qui compte le nombre de node dans un cycle
def NumberNodeInList(graph):
    nodesInList = list()
    cycleAnalysis = sorted(nx.simple_cycles(graph))
    for cycle in cycleAnalysis:
        for node in cycle:
            if node not in nodesInList:
                nodesInList.append(node)
    return len(nodesInList)

#print(NumberNodeInList(D))


#Hill Climbing Search

#print(D.nodes)
def GetHighestValueNeighbour(graph):
    allNodesInGraph = graph.nodes
    print('allNodesInGraph',type(allNodesInGraph))
    bestNodeToErase = list(allNodesInGraph)[0]
    NumberOfNodesInNeighbourGraph = math.inf
    for node in allNodesInGraph:
        #print(node)
        a = graph.copy()        
        a.remove_node(node)
        #print('edges', a.edges)
        numberOfNodes = NumberNodeInList(a)
        #print('number of node in cycle',numberOfNodes)
        if numberOfNodes<NumberOfNodesInNeighbourGraph:
            NumberOfNodesInNeighbourGraph = numberOfNodes
            bestNodeToErase = node
        #print(a.nodes)
        a.clear()
    #print(bestNodeToErase, NumberOfNodesInNeighbourGraph)
    a = graph.copy()        
    a.remove_node(bestNodeToErase)
    return a

#print(GetHighestValueNeighbour(D))


    

#graphToTest = Hill_Climbing_method(D)
#cycleAnalysis = sorted(nx.simple_cycles(graphToTest))
#print(cycleAnalysis)




######################################################################################

def GetrandomNeighbour(graph):
    allNodesInGraph = graph.nodes
    print('allNodesInGraph',allNodesInGraph)
    #print('allNodesInGraph',type(allNodesInGraph))
    allNodes= list(allNodesInGraph)
    n = randint(0,len(allNodes)-1)
    #print('n',n)
    a = graph.copy()        
    a.remove_node(allNodes[n])
    return a

    


def Simulated_Annealing(graph, schema):
    current = graph.copy()
    T = int()

    for i in range(0,schema):
        T = 2**i
        successor = GetrandomNeighbour(current)
        deltaE = NumberNodeInList(current) - NumberNodeInList(successor)
        print('delta E', deltaE)
        print('T', T)
        if deltaE>0:
            current.clear()
            current = successor.copy()        
        else:
            aleaToPass =  math.exp(deltaE/T)
            
            alea = random.random()
            print('aleaToPass', aleaToPass)
            print('alea', alea)
            if alea >=aleaToPass:
                current.clear()
                current = successor.copy()
        successor.clear()
    return current.copy()
    """

mongraph = Simulated_Annealing(D, 20)
print(mongraph.nodes)
#print(mongraph.nodes)
cycleAnalysis = sorted(nx.simple_cycles(mongraph))
print(cycleAnalysis)
"""


#########################################################################################################





def GeneraterandomSolutions(graph):
    s = graph.copy()
    listOfNodes = list(graph.nodes)
    #print(listOfNodes)
    randomSelection = random.choices(listOfNodes, k=randint(0,len(listOfNodes)+1))
    uniqueValueRdmSelection = list(set(randomSelection))
    #print(uniqueValueRdmSelection)
    s.remove_nodes_from(uniqueValueRdmSelection)
    #print(s.nodes)
    return s.copy()
   
def Sort_Tuple(tup):
 
    
    return(sorted(tup, key = lambda x: x[0]))


#Fonction qui compte le nombre de node dans un cycle en lui donnant la liste des nodes a supprimer
def NumberNodeInListwithGraphCreation(liste, graphe):
    a = graphe.copy()
    a.remove_nodes_from(liste)
    nodesInList = list()
    cycleAnalysis = sorted(nx.simple_cycles(a))
    for cycle in cycleAnalysis:
        for node in cycle:
            if node not in nodesInList:
                nodesInList.append(node)
    return len(nodesInList)


def GeneticAlgorythm(graph):
    highestNodeNumber = graph.number_of_nodes()
    population = list()    
    #générer une population
    for s in range(1000):
        population.append(GeneraterandomSolutions(graph))    
    

    for i in range(10):
        #Faire une selection
        torankedSolutions = list()
        for s in population:
            torankedSolutions.append((NumberNodeInList(s),s))
        rankedSolutions = Sort_Tuple(torankedSolutions)      
        parents = rankedSolutions[:2]
        #print('parents',parents[0][1])     

        #crossover
        #print('directdans', )
        parent1 = parents[0][1].nodes
        parent2 = parents[1][1].nodes

        print('parent1', parent1)
        #print('type', type(parent1))
        print('parent2', parent2)
        #parentMerge = list(set(parents[0][1].nodes+parents[1][1].nodes))
        #print('parentMerge', parentMerge)

        cross_point = random.randint(0,highestNodeNumber)
        #print('cross_point', cross_point)

        parent1_1 = list(filter(lambda a: a <= cross_point, parent1))
        print('Child1_1', list(parent1_1))
        parent1_2 = list(filter(lambda a: a > cross_point, parent1))
        print('Child1_2', list(parent1_2))

        parent2_1 = list(filter(lambda a: a <= cross_point, parent2))
        print('Child2_1', list(parent2_1))
        parent2_2 = list(filter(lambda a: a > cross_point, parent2))
        print('Child2_2', list(parent2_2))

        #child1 = parents[0][1].nodes[0:cross_point+1] +  parents[1][1].nodes[cross_point+1 : ]
        nodesOfchild1 = parent1_1 + parent2_2
        nodesOfchild2 = parent2_1 + parent1_2
        children = [nodesOfchild1, nodesOfchild2]
        print('nodesOfchild1', nodesOfchild1)
        print('nodesOfchild2', nodesOfchild2)

        #print('child1', nodesOfchild1)
        #print('child2', nodesOfchild2)


        #mutate 
        #mute = 20
        mute = random.randint(0,49)
        if mute==20:
            x=random.randint(0,1)
            chosenChild = children[x]
            index = random.randrange(len(chosenChild))
            chosenChild[index] = random.randint(0, highestNodeNumber)

            
        print('children', children)

        #create and add new childen

        child1graph = graph.copy()



        #nodes to keep 
        toEraseNode1 =  set(graph.nodes()) - set(nodesOfchild1)
        toEraseNode2 =  set(graph.nodes()) - set(nodesOfchild2)

        child1graph.remove_nodes_from(toEraseNode1)
        child2graph = graph.copy()
        child2graph.remove_nodes_from(toEraseNode2)
        print('child1graph1', child1graph.nodes)
        print('child1graph2', child2graph.nodes)
        population = [child1graph.copy(), child2graph.copy()]
        child1graph.clear()
        child2graph.clear()
    

        print(population)

GeneticAlgorythm(D)