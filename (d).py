import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path

G=nx.Graph()
G=nx.read_edgelist("inputfile.edgelist",create_using=nx.DiGraph())

nx.draw(G,with_labels = True,node_size=700,font_size=12)
plt.show()

maxflow= nx.maximum_flow(G, '1', '4',capacity='weight',flow_func=shortest_augmenting_path,)[0]
print(maxflow)
