from itertools import cycle
from tracemalloc import start
import networkx as nx
import matplotlib.pyplot as plt

#A partir d'un graphe contenant des cycles, notre objectif est de proposer un 
#coupe-cycle en suivant l'algorithme de Hill Climbing. Le but est de proposer une liste
#de sommet "cassant" tous les cycles existants.
G=nx.erdos_renyi_graph(n=7, p=0.3, seed=10, directed=True)
cycles=list(nx.simple_cycles(G))
print(cycles)

node_explored=[]
node_in_cycle=[]


def toExplore(node):
    node_explored.append(node)
    if not node in node_in_cycle:
        a=1
    print("on visite : ",node)
    for node_neighbor in G.neighbors(node):
        if not node_neighbor in node_explored:
            toExplore(node_neighbor)


def dfs():
    for node in G:
        if not node in node_explored:
            toExplore(node)



dfs()



print(node_in_cycle)

#nx.draw(G,with_labels=True)
#plt.draw()
#plt.show()
