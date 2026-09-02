import yaml
import networkx as nx
import random

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_litany_graph(nodes_path, edges_path):
    node_data = load_yaml(nodes_path)
    edge_data = load_yaml(edges_path)

    G = nx.DiGraph()

    for node in node_data["nodes"]:
        G.add_node(
            node["id"],
            label=node.get("label", ""),
            meaning=node.get("meaning", ""),
            tags=node.get("tags", []),
            keywords=node.get("keywords", []),
            audio=node.get("audio"),
            visual=node.get("visual")
        )

    for edge in edge_data["edges"]:
        G.add_edge(
            edge["source"],
            edge["target"],
            weight=edge.get("weight", 1)
        )

    return G

def invoke_litany (G, start='life', steps=4, tag_bias=True):
    path = [start]
    current = start

    for _ in range(steps):
        neighbors = list(G.successors(current))
        if not neighbors:
            break

        weights = []

        for node in neighbors:
            base_weight = G.edges[current, node].get(
                "weight",
                1.0
            )

            if tag_bias:
                shared_tags = (
                    set(G.nodes[current]["tags"])
                    &
                    set(G.nodes[n]["tags"])
                )
                tag_bonus = 1 + len(shared_tags)
                final_weight = (
                    base_weight * tag_bonus
                )

            else:
                final_weight = base_weight

            weights.append(final_weight)

        next_node = random.choices(
            neighbors,
            weights=weights,
            k=1
        )[0]

        path.append(next_node)
        current = next_node

    return path
