import networkx as nx
import matplotlib.pyplot as plt
import random
import math

#A partir d'un graphe contenant des cycles, notre objectif est de proposer un 
#coupe-cycle en suivant l'algorithme de simulated annealing. Le but est de proposer une liste
#de sommet "cassant" tous les cycles existants.
G=nx.erdos_renyi_graph(n=8, p=0.4, seed=10, directed=True)
cycles=list(nx.simple_cycles(G))


#Fct-score, Le score donné à chaque sommet est le nombre de cycles auxquels il appartient.
#Plus un sommet appartient à un grand nombre de cycles, plus il est susceptible d'en "casser".
def getFonctionCout(graph):
    results={}
    current_graph=graph.copy()
    graph_copy=graph.copy()
    for node in graph_copy.nodes:
        current_graph.remove_node(node)
        results[node]=int(len(list(nx.simple_cycles(current_graph))))
        current_graph=graph_copy.copy()
    return results

def getFonctionCout(graph,node):
    current_graph=graph.copy()
    current_graph.remove_node(node)
    return int(len(list(nx.simple_cycles(current_graph))))

current_value_cycles=len(cycles)
coupe_cycle=[]

initial_temp = 0.8
final_temp = 0
alpha = 0.04
current_temp = initial_temp
#L'état but est de ne plus avoir de cycles.
#La solution voisine est la solution actuelle moins un sommet tiré aléatoirement et qui supprime un cycle
# ou bien qui est conservé selon une certaines probabilité dans le cas contraire.
while current_temp > final_temp: 
    alea_neighbor_state_node=random.choice(list(G.nodes))
    next_cost=getFonctionCout(G, alea_neighbor_state_node)
    delta_E=next_cost - current_value_cycles
    #On inverse la logique par rapport à l'algo original car c'est une fonction coût et non une fonction objectif.
    if delta_E<0:
        G.remove_node(alea_neighbor_state_node)
        coupe_cycle.append(alea_neighbor_state_node)
        current_value_cycles=next_cost
    else:
        if random.uniform(0, 1) < math.exp(delta_E-1/ current_temp):
            #Comme la logique est inversée avec une fonction coût, il est nécessaire de prendre l'opposé de notre delta_E.
            #On soustrait par -1 pour que lorsque delta_e soit égal à 0, l'intérieur de l'exposant reste négatif
            #et que plus current_temp tend vers 0, plus la probabilité diminue.
            G.remove_node(alea_neighbor_state_node)
            coupe_cycle.append(alea_neighbor_state_node)
            current_value_cycles=next_cost
    current_temp -= alpha


print("coupe-cycle : ", coupe_cycle)

#nx.draw(G,with_labels=True)
#plt.draw()
#plt.show()

#A partir de graphes d'un certain nombr ede sommets, les calculs sont très longs,(5 secondes d'execution pour 15 sommets)
#sur une machine Ryzen 7 3700U + 8GO RAM) les temps de calculs deviennet très longs.
#Le temps d'execution de annealing est moins long car il demande de calculer le coût d'un unique état tiré au sort.
#  
