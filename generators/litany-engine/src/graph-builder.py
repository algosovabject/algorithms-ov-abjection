import yaml
import networkx as nx

def load_graph(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    G = nx.DiGraph()

    for node in data['nodes']:
        G.add_node(node['id'], label=node['label'], meaning=node['meaning'])

    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

    return G
