import networkx as nx
import matplotlib.pyplot as plt

#A partir d'un graphe contenant des cycles, notre objectif est de proposer un 
#coupe-cycle en suivant l'algorithme de Hill Climbing. Le but est de proposer une liste
#de sommet "cassant" tous les cycles existants.
G=nx.erdos_renyi_graph(n=20, p=0.05, seed=15, directed=True)

def getNumberOfNodesInCycles(Graph):
    list_nodes=set()
    for node in Graph:
        if Graph.successors(node):
            return 0
    return 1





node_explored=[]
node_in_cycle=[]

nodes_visited=set()

''''def isInCycle(Graph, start_node):
    return toExplore(Graph, start_node,start_node)

def toExplore(Graph,node, start):
    nodeIsInCycle=False
    nodes_neighbors=set(Graph.neighbors(node))
    nodes_neighbors_not_explored=nodes_neighbors.difference(nodes_visited)
    for node_neighbor in nodes_neighbors_not_explored:
        print(node_neighbor)
        nodes_visited.add(node_neighbor)
        if node_neighbor==start:
            nodeIsInCycle= True
        toExplore(Graph,node_neighbor,start)
    return nodeIsInCycle


print("cycle en  : ", isInCycle(G,0))
'''

def isInCycle(Graph, node):
    for element in nx.dfs_successors(Graph,node):
        print(element)
        for e in nx.dfs_successors(Graph,node)[element]:
            print(e)

print(nx.dfs_successors(G,0))
isInCycle(G,0)

'''
nodes_strongly_connected=list(nx.strongly_connected_components(G))
list_nodes=set()
for components in nodes_strongly_connected:
    if(len(components)>1):
        for node in components:
            list_nodes.add(node)
number_of_nodes_strongly_connected=list(list_nodes)



#La solution précédente hill_climbing_prog1 s'appuyant sur Networkx et la recherche de tous les 
#cycles du graphe pour notre fonction score était trop coûteuse. 
#Un cycle est une composante connexe (l'inverse n'est pas forcément vrai) de taille supérieure à 1.
#L'algorithme de Tarjan de Networkx permet de trouver les composantes fortemements connexes avec un coût (calculs...) moindre.
#Ainsi, on peut retrouver les sommets les plus à même de faire partie d'une CFN, donc d'un cycle, avec une complexité moindre.


#On renvoie le nombre de sommets appartennant à une composante fortement connexe dans le graphe de taille supérieure à 1 sommet.
def getNumberOfNodesStronglyConnected(Graph):
    nodes_strongly_connected=list(nx.strongly_connected_components(Graph))
    list_nodes=set()
    for components in nodes_strongly_connected:
        if(len(components)>1):
            for node in components:
                list_nodes.add(node)
    return len(list_nodes)




#Cette fonction coût retourne un dictionnaire avec pour clef les sommets
#et pour valeur le nombre de sommets restant dans une composante fortement connexe après suppression dudit sommet
#On recherche à minimiser cette valeur, nous utiliserons la fonction min() dans l'algo principal pour cela.
def getFonctionCout(graph):
    results={}
    current_graph=graph.copy()
    graph_copy=graph.copy()
    for node in graph_copy.nodes:
        current_graph.remove_node(node)
        results[node]=int(getNumberOfNodesStronglyConnected(current_graph))
        current_graph=graph_copy.copy()
    return results




current_value_nodes_strongly_connected=len(number_of_nodes_strongly_connected)
coupe_cycle=[]

#L'état but est de ne plus avoir de cycles.
#La solution voisine est la solution actuelle moins le sommet qui lors de sa suppression permet 
#la sortie du plus grand nombre de sommets d'une composante fortement connexe de taille supérieure à 1.
while True: 
    states_nodes_costs=getFonctionCout(G)
    best_neighbor_state_node=min(states_nodes_costs, key = lambda x: states_nodes_costs[x])
    #Ici on vérifie qu'en supprimant ce sommet, on a bien une solution meilleure que la précédente
    #Comparaison entre les deux fonctions coûts "le nombre de cycles restants" 
    #Si ce n'est pas le cas on s'arrête à l'état courant
    if states_nodes_costs[best_neighbor_state_node] >= current_value_nodes_strongly_connected: 
        break
    G.remove_node(best_neighbor_state_node)
    coupe_cycle.append(best_neighbor_state_node)
    current_value_nodes_strongly_connected=states_nodes_costs[best_neighbor_state_node]
    

#A partir de graphes de plus de 15 sommets : 15.4 secondes d'execution avec l'ancienne fct coût, 2.5 sec maintenant.
#sur une machine Ryzen 7 3700U + 8GO RAM) 
print("coupe-cycle : ", len(coupe_cycle))
'''
nx.draw(G,with_labels=True)
plt.draw()
plt.show()
