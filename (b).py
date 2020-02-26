import networkx as nx

G=nx.Graph()
G=nx.read_edgelist("inputfile.edgelist",create_using=nx.DiGraph())
nx.draw(G,with_labels = True,node_size=700,font_size=12)

print(G.nodes)
