import networkx as nx
import matplotlib.pyplot as plt

#A partir d'un graphe contenant des cycles, notre objectif est de proposer un 
#coupe-cycle en suivant l'algorithme de Hill Climbing. Le but est de proposer une liste
#de sommet "cassant" tous les cycles existants.
G=nx.erdos_renyi_graph(n=15, p=0.4, seed=10, directed=True)
cycles=list(nx.simple_cycles(G))


#Cette fonction coût retourne un dictionnaire avec pour clef les sommets
#et pour valeur le nombre de cycles restant dans le graph après suppression dudit sommet
#On recherche à minimiser cette valeur, nous utiliserons la fonction min() dans l'algo principal pour cela.
def getFonctionCout(graph):
    results={}
    current_graph=graph.copy()
    graph_copy=graph.copy()
    for node in graph_copy.nodes:
        current_graph.remove_node(node)
        results[node]=int(len(list(nx.simple_cycles(current_graph))))
        current_graph=graph_copy.copy()
    return results



current_value_cycles=len(cycles)
coupe_cycle=[]

#L'état but est de ne plus avoir de cycles.
#La solution voisine est la solution actuelle moins le sommet qui lors de sa suppression permet 
#la suppression du plus grand nombre de cycles possible.
while True: 
    states_nodes_costs=getFonctionCout(G)
    best_neighbor_state_node=min(states_nodes_costs, key = lambda x: states_nodes_costs[x])
    #Ici on vérifie qu'en supprimant ce sommet, on a bien une solution meilleure que la précédente
    #Comparaison entre les deux fonctions coûts "le nombre de cycles restants" 
    #Si ce n'est pas le cas on s'arrête à l'état courant
    if states_nodes_costs[best_neighbor_state_node] >= current_value_cycles: 
        break
    G.remove_node(best_neighbor_state_node)
    coupe_cycle.append(best_neighbor_state_node)
    current_value_cycles=states_nodes_costs[best_neighbor_state_node]
    

#A partir de graphes de plus de 15 sommets (15.4 secondes d'execution)
#sur une machine Ryzen 7 3700U + 8GO RAM) les temps de calculs deviennet très longs.
#La fonction coût est très coûteuse, la recherche de l'ensemble des cycles est un NP-problem
#Ainsi, l'algo serait grandement amélioré avec une fonction coût avec une complexité moindre.
#De plus, Hill Climbing nous demande à chaque itération de lancer un calcul de coût pour chacun des états-voisins.
print("coupe-cycle : ", coupe_cycle)

#nx.draw(G,with_labels=True)
#plt.draw()
#plt.show()
