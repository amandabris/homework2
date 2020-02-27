import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path
from networkx import get_edge_attributes

def maxflow(startgraph, resgraph, caps, start, end):

    """
    startgraph is the graph
    resgraph is the residual graph, identical to startgraph at first
    caps is a dictionary: edges are keys, and their capacity is the value
    start, end, are the start and end nodes
    """
    
    done = False
    iteration_num = 1
    maxflow = 0

    while(not done): 
        try:
            split_list = nx.shortest_path(resgraph, start, end)
        except:
            print('No connectivity; interation', iteration_num ,'!\ncut')
            break

        tlist = split_list[:]
        pathcaps = {}
        while(len(tlist) > 1):
            o = tlist.pop(0)
            d = tlist[0]
            if(caps.get((o,d)) != None):
                pathcaps.update({(o,d):caps.get((o,d))})
            else:
                pathcaps.update({(o,d):caps.get((d,o))})
         
        low_edge = min(pathcaps, key=pathcaps.get) 
        residual = caps.get(low_edge)
        if(residual == None):
            residual = caps.get((low_edge[-1], low_edge[0]))
            
        for i in pathcaps.keys():
            pathcaps[i] = pathcaps[i] - residual
            #print(*i)
            if pathcaps[i] == 0:
                if(i[1] in resgraph.get_edge_data(*i)): 
                    resgraph.remove_edge(i[1],i[0])
                    startgraph[i[1]][i[0]]['flow'] += residual
                    #m += residual
                    #attribute = {(*i[1],*i[0]): { 'flow' : m }}
                    #get_edge_attributes(startgraph,attribute)
                    #startgraph.edge[i[0]][i[1]]['flow'] += residual 
                else: 
                    resgraph.remove_edge(i[1],i[0])
                    #m = get_edge_attributes(startgraph,'flow')
                    #print(get_edge_attributes(startgraph,'flow'))
                    #print(i)
                    m = get_edge_attributes(startgraph,'flow').get(i)
                    #print(m)
                    startgraph[i[1]][i[0]]['flow'] += residual
                    #m += residual
                    #attribute = {(*i[1],*i[0]): { 'flow' : m }}
                    #get_edge_attributes(startgraph,attribute)
                    #startgraph.edge[i[1]][i[0]]['flow'] += residual           
            else:
                if(i[1] in resgraph.get_edge_data(*i)):
                    #capacity = {capacity : pathcaps[i]}
                    #set_edge_attributes(resgraph, capacity) #[i[0]][i[1]]['cap'] = pathcaps[i] 
                    resgraph.remove_edge(*i)
                    resgraph.add_edge(i[1],i[0], capacity = pathcaps[i])
                    #startgraph.edge[i[0]][i[1]]['flow'] += residual
                else:
                    #resgraph.edge[i[1]][i[0]]['cap'] = pathcaps[i]
                    #capacity = {capacity : pathcaps[i]}
                    #set_edge_attributes(resgraph, capacity) #[i[0]][i[1]]['cap'] = pathcaps[i] 
                    resgraph.remove_edge(*i)
                    resgraph.add_edge(i[1],i[0], capacity = pathcaps[i])
                    #startgraph.edge[i[1]][i[0]]['flow'] += residual
        
        maxflow += residual
        iteration_num = iteration_num + 1
    
    return startgraph, resgraph, maxflow

#####################################

def graph_maker():
    start = 1
    end = 7

    G = nx.Graph()
    G.add_edge(1,2, capacity=3.0)
    G.add_edge(1,3, capacity=1.0)
    G.add_edge(2,4, capacity=3.0)
    G.add_edge(3,4, capacity=5.0)
    G.add_edge(3,5, capacity=4.0)
    G.add_edge(5,6, capacity=2.0)
    G.add_edge(4,7, capacity=2.0)
    G.add_edge(6,7, capacity=3.0)

    attrs = { (1,2) : { 'flow' : 0},
              (1,3) : { 'flow' : 0},
              (2,4) : { 'flow' : 0},
              (3,4) : { 'flow' : 0},
              (3,5) : { 'flow' : 0},
              (5,6) : { 'flow' : 0},
              (4,7) : { 'flow' : 0},
              (6,7) : { 'flow' : 0}
        }

    #print(G.edges())
    nx.set_edge_attributes(G,attrs)

    caps = {
        (1,2) : 3,
        (1,3) : 1,
        (2,4) : 3,
        (3,4) : 5,
        (3,5) : 4,
        (5,6) : 2,
        (4,7) : 2,
        (6,7) : 3
    }

    resgraph = nx.Graph()
    resgraph.add_edge(1,2, capacity=3.0)
    resgraph.add_edge(1,3, capacity=1.0)
    resgraph.add_edge(2,4, capacity=3.0)
    resgraph.add_edge(3,4, capacity=5.0)
    resgraph.add_edge(3,5, capacity=4.0)
    resgraph.add_edge(5,6, capacity=2.0)
    resgraph.add_edge(4,7, capacity=2.0)
    resgraph.add_edge(6,7, capacity=3.0)
    #print(G.edges())
    nx.set_edge_attributes(resgraph,attrs)
    
    print("the max flow is", maxflow(G,resgraph,caps,start,end)[2])
