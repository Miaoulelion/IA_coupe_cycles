import networkx as nx
import matplotlib.pyplot as plt

#A partir d'un graphe contenant des cycles, notre objectif est de proposer un 
#coupe-cycle en suivant l'algorithme de Hill Climbing. Le but est de proposer une liste
#de sommet "cassant" tous les cycles existants.
G=nx.erdos_renyi_graph(n=10, p=0.4, seed=10, directed=True)
cycles=list(nx.simple_cycles(G))


#Fct-score, Le score donné à chaque sommet est le nombre de cycles auxquels il appartient.
#Plus un sommet appartient à un grand nombre de cycles, plus il est susceptible d'en "casser".
def getNodesScores(Graphe,list_cycles):
    results={}
    for node in Graphe:
        node_score=0
        for cycle in list_cycles:
            node_score=node_score+cycle.count(node)
        results[node]=int(node_score)
    return results


nbr_cycles=len(cycles)
coupe_cycle=[]

#On continue tant qu'il existe des cycles. Il n'est pas possible de bloquer en amont.
#La solution voisine est la solution actuelle moins un sommet (celui avec le plus
# de cycles)
while nbr_cycles>0:
    nodes_scores=getNodesScores(G,cycles)
    node_highest_score=max(nodes_scores, key = lambda x: nodes_scores[x])
    coupe_cycle.append(node_highest_score)
    G.remove_node(node_highest_score)
    cycles=list(nx.simple_cycles(G))
    nbr_cycles=len(cycles)

#A partir de graphes de plus de 15 sommets (55 secondes d'execution
# sur une machine Ryzen 7 3700U + 8GO RAM) les temps de calculs deviennet très longs.
#--> Problématique de ce NP-problème.
#Il faut donc rechercher une fonction de score moins coûteuse.
print("coupe-cycle : ", coupe_cycle)

nx.draw(G,with_labels=True)
plt.draw()
plt.show()
