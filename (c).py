import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

G=nx.Graph()
G=nx.read_edgelist("inputfile.edgelist",create_using=nx.DiGraph())

nx.draw(G,with_labels = True,node_size=700,font_size=12)
plt.show()

def BreadthFirstLevels(G,root):
    """
    Generate a sequence of bipartite directed graphs, each consisting
    of the edges from level i to level i+1 of G. Edges that connect
    vertices within the same level are not included in the output.
    The vertices in each level can be listed by iterating over each
    output graph.
    """
    visited = set()                  #create array Visited 
    currentLevel = [root]    #make the root (u) in pseudocode
    while currentLevel:       #list is non-empty
        for v in currentLevel:   #checks the edges in the list
            visited.add(v)          #add the node to the set of visited nodes
        nextLevel = set()         #moves to the next level of the tree, creates list for nodes here
        levelGraph = {v:set() for v in currentLevel} #creates graph of nodes in level
        for v in currentLevel: #checks the nodes in the first level
            for w in G[v]:         #checks if nodes in first level connected to nodes in next level
                if w not in visited:  #if nodes in the next level after first level have not been visited yet
                    levelGraph[v].add(w) #if not visited, add to graph of next level
                    nextLevel.add(w)  #mark it as visited and put in set
        yield levelGraph           #give the graph of successor level
        currentLevel = nextLevel  #previous next level now becomes current level, new next level
print(list(BreadthFirstLevels(G,'1'))) #prints graph as tree traversal by BFS

