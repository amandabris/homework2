"""
Maximum flow (and minimum cut) algorithms on capacitated graphs.
"""
import networkx as nx
from networkx.algorithms.flow.utils import *

# Define the default flow function for computing maximum flow.
import numpy

__all__ = ['maximum_flow',
           'maximum_flow_value',
           'minimum_cut',
           'minimum_cut_value']


def maximum_flow(G, s, t, capacity='capacity', flow_func=None, **kwargs):

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


def maximum_flow_value(G, s, t, capacity='capacity', flow_func=None, **kwargs):

    if flow_func is None:
        if kwargs:
            raise nx.NetworkXError("You have to explicitly set a flow_func if"
                                   " you need to pass parameters via kwargs.")
        flow_func = default_flow_func

    if not callable(flow_func):
        raise nx.NetworkXError("flow_func has to be callable.")

    R = flow_func(G, s, t, capacity=capacity, value_only=True, **kwargs)

    return R.graph['flow_value']


def minimum_cut(G, s, t, capacity='capacity', flow_func=None, **kwargs):

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
    # Remove saturated edges from the residual network
    cutset = [(u, v, d) for u, v, d in R.edges(data=True)
              if d['flow'] == d['capacity']]
    R.remove_edges_from(cutset)

    # Then, reachable and non reachable nodes from source in the
    # residual network form the node partition that defines
    # the minimum cut.
    non_reachable = set(nx.shortest_path_length(R, target=t))
    partition = (set(G) - non_reachable, non_reachable)
    # Finaly add again cutset edges to the residual network to make
    # sure that it is reusable.
    if cutset is not None:
        R.add_edges_from(cutset)
    return (R.graph['flow_value'], partition)


def minimum_cut_value(G, s, t, capacity='capacity', flow_func=None, **kwargs):
    
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
