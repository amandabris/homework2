
#Maximum flow (and minimum cut) algorithms on capacitated graphs.

import networkx as nx
from networkx.algorithms.flow.utils import *

__all__ = ['dijkstra_maximum_flow',
           'dijkstra_maximum_flow_value',
           'dijkstra_minimum_cut',
           'dijkstra_minimum_cut_value']


def dijkstra_maximum_flow(G, s, t, capacity='capacity', flow_func=None, **kwargs):

    if flow_func is None:
        if kwargs:
            raise nx.NetworkXError("You have to explicitly set a flow_func if"
                                   " you need to pass parameters via kwargs.")
        flow_func = default_flow_func

    if not callable(flow_func):
        raise nx.NetworkXError("flow_func has to be callable.")

    R = flow_func(G, s, t, capacity=capacity, value_only=False, **kwargs)
    flow_dict = build_flow_dict(G, R)

    return (R.graph['flow_value'], flow_dict)


def dijkstra_maximum_flow_value(G, s, t, capacity='capacity', flow_func=None, **kwargs):

    if flow_func is None:
        if kwargs:
            raise nx.NetworkXError("You have to explicitly set a flow_func if"
                                   " you need to pass parameters via kwargs.")
        flow_func = default_flow_func

    if not callable(flow_func):
        raise nx.NetworkXError("flow_func has to be callable.")

    R = flow_func(G, s, t, capacity='capacity', value_only=True, **kwargs)

    return R.graph['flow_value']


def dijkstra_minimum_cut(G, s, t, capacity='capacity', flow_func=None, **kwargs):

    if flow_func is None:
        if kwargs:
            raise nx.NetworkXError("You have to explicitly set a flow_func if"
                                   " you need to pass parameters via kwargs.")
        flow_func = default_flow_func

    if not callable(flow_func):
        raise nx.NetworkXError("flow_func has to be callable.")

    R = flow_func(G, s, t, capacity=capacity, value_only=True, **kwargs)
    
    cutset = [(u, v, d) for u, v, d in R.edges(data=True)
              if d['flow'] == d['capacity']]
    R.remove_edges_from(cutset)

    non_reachable = set(nx.shortest_path_length(R, target=t))
    partition = (set(G) - non_reachable, non_reachable)

    if cutset is not None:
        R.add_edges_from(cutset)
    return (R.graph['flow_value'], partition)


def dijkstra_minimum_cut_value(G, s, t, capacity='capacity', flow_func=None, **kwargs):
    
    if flow_func is None:
        if kwargs:
            raise nx.NetworkXError("You have to explicitly set a flow_func if"
                                   " you need to pass parameters via kwargs.")
        flow_func = default_flow_func

    if not callable(flow_func):
        raise nx.NetworkXError("flow_func has to be callable.")

    if (kwargs.get('cutoff') is not None and
        flow_func in (edmonds_karp, preflow_push, shortest_augmenting_path)):
        raise nx.NetworkXError("cutoff should not be specified.")

    R = flow_func(G, s, t, capacity=capacity, value_only=True, **kwargs)

    return R.graph['flow_value']

print("\nOutput dictionary with maximum flow as values (in this case, 7 = max flow)")
print(flow_dict,"\n")

print("Value of the maximum flow :", flow_value,"\n")

print("Max flow between two nodes in the graph:")
print(" - between nodes 1 and 2 :",flow_dict['1']['2'])
print(" - between nodes 2 and 3 :",flow_dict['2']['3'])
print(" - between nodes 3 and 4 :",flow_dict['3']['4'])