import networkx as nx

def find_ooze_path(G, start, end):
    try:
        path = nx.dijkstra_path(G, source=start, target=end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return []
