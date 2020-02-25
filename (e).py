from collections import deque
from heapq import heappush, heappop
from itertools import count
import numpy
import networkx as nx
from networkx.utils import generate_unique_node


__all__ = ['dijkstra_path',
           'dijkstra_path_length',
           'bidirectional_dijkstra',
           'single_source_dijkstra',
           'single_source_dijkstra_path',
           'single_source_dijkstra_path_length',
           'multi_source_dijkstra',
           'multi_source_dijkstra_path',
           'multi_source_dijkstra_path_length',
           'all_pairs_dijkstra',
           'all_pairs_dijkstra_path',
           'all_pairs_dijkstra_path_length',
           'dijkstra_predecessor_and_distance',
           'bellman_ford_path',
           'bellman_ford_path_length',
           'single_source_bellman_ford',
           'single_source_bellman_ford_path',
           'single_source_bellman_ford_path_length',
           'all_pairs_bellman_ford_path',
           'all_pairs_bellman_ford_path_length',
           'bellman_ford_predecessor_and_distance',
           'negative_edge_cycle',
           'goldberg_radzik',
           'johnson']


def _weight_function(G, weight):

    (length, path) = single_source_dijkstra(G, source, target=target,
                                            weight=weight)
    return path



def dijkstra_path_length(G, source, target, weight='weight'):

    if source == target:
        return 0
    weight = _weight_function(G, weight)
    length = _dijkstra(G, source, weight, target=target)
    try:
        return length[target]
    except KeyError:
        raise nx.NetworkXNoPath(
            "Node %s not reachable from %s" % (target, source))



def single_source_dijkstra_path(G, source, cutoff=None, weight='weight'):


    return multi_source_dijkstra_path(G, {source}, cutoff=cutoff,
                                      weight=weight)



def single_source_dijkstra_path_length(G, source, cutoff=None,
                                       weight='weight'):

    return multi_source_dijkstra_path_length(G, {source}, cutoff=cutoff,
                                             weight=weight)



def single_source_dijkstra(G, source, target=None, cutoff=None,
                           weight='weight'):

    return multi_source_dijkstra(G, {source}, cutoff=cutoff, target=target,
                                 weight=weight)



def multi_source_dijkstra_path(G, sources, cutoff=None, weight='weight'):

    length, path = multi_source_dijkstra(G, sources, cutoff=cutoff,
                                         weight=weight)
    return path



def multi_source_dijkstra_path_length(G, sources, cutoff=None,
                                      weight='weight'):

    if not sources:
        raise ValueError('sources must not be empty')
    weight = _weight_function(G, weight)
    return _dijkstra_multisource(G, sources, weight, cutoff=cutoff)



def multi_source_dijkstra(G, sources, target=None, cutoff=None,
                          weight='weight'):

    if not sources:
        raise ValueError('sources must not be empty')
    if target in sources:
        return (0, [target])
    weight = _weight_function(G, weight)
    paths = {source: [source] for source in sources}  # dictionary of paths
    dist = _dijkstra_multisource(G, sources, weight, paths=paths,
                                 cutoff=cutoff, target=target)
    if target is None:
        return (dist, paths)
    try:
        return (dist[target], paths[target])
    except KeyError:
        raise nx.NetworkXNoPath("No path to {}.".format(target))



def _dijkstra(G, source, weight, pred=None, paths=None, cutoff=None,
              target=None):

    return _dijkstra_multisource(G, [source], weight, pred=pred, paths=paths,
                                 cutoff=cutoff, target=target)


def _dijkstra_multisource(G, sources, weight, pred=None, paths=None,
                          cutoff=None, target=None):

    G_succ = G._succ if G.is_directed() else G._adj

    push = heappush
    pop = heappop
    dist = {}
    seen = {}

    c = count()
    fringe = []
    for source in sources:
        if source not in G:
            raise nx.NodeNotFound("Source {} not in G".format(source))
        seen[source] = 0
        push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue
        dist[v] = d
        if v == target:
            break
        for u, e in G_succ[v].items():
            cost = weight(v, u, e)
            if cost is None:
                continue
            vu_dist = dist[v] + cost
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)

    return dist


def dijkstra_predecessor_and_distance(G, source, cutoff=None, weight='weight'):

    weight = _weight_function(G, weight)
    pred = {source: []}  # dictionary of predecessors
    return (pred, _dijkstra(G, source, weight, pred=pred, cutoff=cutoff))



def all_pairs_dijkstra(G, cutoff=None, weight='weight'):

    for n in G:
        dist, path = single_source_dijkstra(G, n, cutoff=cutoff, weight=weight)
        yield (n, (dist, path))



def all_pairs_dijkstra_path_length(G, cutoff=None, weight='weight'):

    length = single_source_dijkstra_path_length
    for n in G:
        yield (n, length(G, n, cutoff=cutoff, weight=weight))



def all_pairs_dijkstra_path(G, cutoff=None, weight='weight'):
    path = single_source_dijkstra_path
    for n in G:
        yield (n, path(G, n, cutoff=cutoff, weight=weight))
