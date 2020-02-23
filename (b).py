import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

G=nx.Graph()
G=nx.read_edgelist("inputfile.edgelist",create_using=nx.DiGraph())


nx.draw(G)
plt.show()
print(G.nodes)
