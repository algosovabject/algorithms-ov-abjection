import yaml

def load_input_map(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def parse_input(user_input, input_map, G):

    user_input = user_input.lower()

    matches = []

    for node_id, data in G.nodes(data=True):

        keywords = data.get("keywords", [])

        for keyword in keywords:

            if keyword.lower() in user_input:
                matches.append(node_id)
                break

        return matches
