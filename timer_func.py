import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path
from networkx import get_edge_attributes
import random
import time
from networkx.algorithms.flow.utils import *

#part d:

def FFmaxflow(startgraph, resgraph, caps, start, end):

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
            #print('No connectivity; interation', iteration_num ,'!\ncut')
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

#part e:

def DJmaxflow(startgraph, resgraph, caps, start, end):

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
            split_list = nx.dijkstra_path(resgraph, start, end)
        except:
            #print('No connectivity; interation', iteration_num ,'!\ncut')
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

################################################################33

#make the graph:

times = []

for y in range(10):

    G = nx.Graph()
    resgraph = nx.Graph()
    start = 1
    end = 1000

    caps = {}
    attrs = {}
    edges = []

    for x in range(10000):
        if(x+2 > 10000):
            break
        random_edge_1 = x+1
        random_edge_2 = random.randint(x+2,10000)

        #reduces redundency:
        edges.append((random_edge_1,random_edge_2))
        edges = set(edges)
        edges = list(edges)
        
        while(random_edge_1 == random_edge_2):
            random_edge_2 = random.randint(1,10000)
        #print(random_edge_1,random_edge_2)

        random_cap = random.randint(20,100)

        G.add_edge(random_edge_1, random_edge_2, capacity = random_cap)
        resgraph.add_edge(random_edge_1, random_edge_2, capacity = random_cap)

        caps[(random_edge_1,random_edge_2)] = random_cap
        attrs[(random_edge_1,random_edge_2)] = { 'flow' : 0 }

    nx.set_edge_attributes(G,attrs)
    nx.set_edge_attributes(resgraph,attrs)

    #nx.draw(G)

    print("Testing...test", y+1)
    starttime = time.time()
    #print("the max flow is", FFmaxflow(G,resgraph,caps,start,end)[2])
    FFmf = FFmaxflow(G,resgraph,caps,start,end)[2]
    endtime = time.time()
    #print(endtime - starttime)

    starttime2 = time.time()
    #print("the max flow is", DJmaxflow(G,resgraph,caps,start,end)[2])
    DJmf = DJmaxflow(G,resgraph,caps,start,end)[2]
    endtime2 = time.time()
    #print(endtime2 - starttime2)

    #print(FFmf,DJmf)

    FFtime = endtime - starttime
    DJtime = endtime2 - starttime2
    times.append((FFtime,DJtime))

for time in times:
    print(time)
