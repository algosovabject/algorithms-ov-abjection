import yaml
import random

def interpret_path(path_nodes):
    labels = [node.get('label', '???') for node in path_nodes if isinstance(node, dict)]
    return " → ".join(labels) if labels else "The voices of the choir fade into silence."