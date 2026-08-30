import yaml
import networkx as nx
import random
import math
import datetime

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def load_oracle_graph(nodes_path, edges_path):
    node_data = load_yaml(nodes_path)
    edge_data = load_yaml(edges_path)

    G = nx.DiGraph()

    for node in node_data['nodes']:
        G.add_node(
            node['id'],
            label=node.get('label', ''),
            meaning=node.get('meaning', ''),
            tags=node.get('tags', [])
        )

    for edge in edge_data['edges']:
        G.add_edge(
            edge['source'],
            edge['target'],
            weight=edge.get('weight', 1)
        )

    return G

def weighted_pseudopod_walk(G, start='life', steps=4, tag_bias=True):
    path = [start]
    current = start
    visited = set([start])

    for _ in range(steps):
        neighbors = list(G.successors(current))
        if not neighbors:
            break

        weights = []
        for n in neighbors:
            base_weight = G.edges[current, n].get('weight', 1.0)

            if tag_bias:
                shared_tags = set(G.nodes[current]['tags']) & set(G.nodes[n]['tags'])
                tag_bonus = 1 + len(shared_tags)
                final_weight = base_weight * tag_bonus
            else:
                final_weight = base_weight

            weights.append(final_weight)

        total_weight = sum(weights)
        probabilities = [w / total_weight for w in weights]
        next_node = random.choices(neighbors, weights=probabilities, k=1)[0]

        path.append(next_node)
        visited.add(next_node)
        current = next_node

    return path

def log_behavior(entry, path="data/ooze_behavior.log"):
    with open(path, "a") as f:
        timestamp = datetime.datetime.now().isoformat()
        f.write(f"{timestamp} - {entry}\n")
