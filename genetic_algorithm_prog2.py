import networkx as nx
import matplotlib.pyplot as plt
from random import *
import random
import math


#A partir d'un graphe contenant des cycles, notre objectif est de proposer un 
#coupe-cycle en suivant l'algorithme de simulated annealing. Le but est de proposer une liste
#de sommet "cassant" tous les cycles existants.
G=nx.erdos_renyi_graph(n=15, p=0.4, seed=10, directed=True)
cycles=list(nx.simple_cycles(G))
#La taille de l'individu doit être en correspondance avec la taille
#de la potentielle solution par rapport au graphe donné.
INDIVIDUAL_TALL=6
POPULATION_TALL=30
BAD_FITNESS_CURSOR=0.30

def selectedInitialIndividual(Graph, tall):
    graph_copy=Graph.copy()
    list_nodes=list(graph_copy.nodes)
    randomSelection=[]
    #Il faut que la taille soit inférieur au nombre de sommets du graph
    while len(randomSelection)<tall:
        selection=random.choices(list_nodes)
        if not selection[0] in randomSelection:
            randomSelection.append(int(selection[0]))
    return randomSelection


#En fonction d'un invidiu (un set de sommets) on renvoie le nombre de sommets dans une
#composante fortement connexe. Plus ce nombre est important, moins la solution est bonne.
#On cherche à minimiser la fitness
def fitnessBrutFunction(individual, Graph):
    graph_copy=Graph.copy()
    graph_copy.remove_nodes_from(individual)
    node_strongly_connected=list(nx.strongly_connected_components(graph_copy))
    list_nodes=set()
    for components in node_strongly_connected:
        if(len(components)>1):
            for node in components:
                list_nodes.add(node)
    return len(list_nodes)
           

#Les enfants sont différents des parents, un crossing over a lieu.
#On casse la chaîne 'ADN' des parents en un point (aléatoire) pour les recombiner.
def reproduce(x,y):
    crossover_point = random.randint(0,INDIVIDUAL_TALL-1)
    x_part1=x[crossover_point:]
    x_part2=x[:crossover_point]
    y_part1=y[crossover_point:]
    y_part2=y[:crossover_point]
    child1=x_part1+y_part2
    child2=y_part1+x_part2
    return child1,child2

#On classe les parents en fonction de leurs fitness, on prend les meilleurs reproducteurs
#pour les reproduire ensemble et avoir de meilleurs enfants.
def sortBestParents(list_parents, Graph):
    fitness_values=[]
    for parent in list_parents:
        fitness_values.append(fitnessBrutFunction(parent,Graph))
    sorted_parents=[x for _,x in sorted(zip(fitness_values,list_parents))]
    fitness_values_sorted=sorted(fitness_values)
    return sorted_parents, fitness_values_sorted


population=list()
#On créé une population, une liste d'individus
for i in range(POPULATION_TALL):
    population.append(selectedInitialIndividual(G,INDIVIDUAL_TALL))

while True:
    x1=random.choices(population)[0]
    y1=random.choices(population)[0]
    x2=random.choices(population)[0]
    y2=random.choices(population)[0]
    parents=[x1,y1,x2,y2]
    sorted_parents, fitness_values_sorted=sortBestParents(parents,G)
    child1, child2=reproduce(sorted_parents[0],sorted_parents[1])
    child3=[]
    child4=[]

    #Si l'un des parents a un score trop faible, on l'élimine de la reproduction
    fitness_score_last_parent=fitness_values_sorted[3]/sum(fitness_values_sorted)
    if(fitness_score_last_parent>BAD_FITNESS_CURSOR):
        child3, child4=reproduce(sorted_parents[2],sorted_parents[1])
    else:
        child3, child4=reproduce(sorted_parents[2],sorted_parents[3])
    
    if fitnessBrutFunction(child1,G)==0.0:
        print("taille solution : ",child1)
        G.remove_nodes_from(child1)
        break
    elif fitnessBrutFunction(child2,G)==0.0:
        print("taille solution : ",len(child2))
        G.remove_nodes_from(child2)
        break
    elif fitnessBrutFunction(child3,G)==0.0:
        print("taille solution : ",child3)
        G.remove_nodes_from(child3)
        break
    elif fitnessBrutFunction(child4,G)==0.0:
        print("taille solution : " ,child4)
        G.remove_nodes_from(child4)
        break

    population.append(child1)
    population.append(child2)
    population.append(child3)
    population.append(child4)
