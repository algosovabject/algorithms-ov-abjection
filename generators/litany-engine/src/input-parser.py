import yaml
import re

def load_input_map(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def parse_input(user_input, input_map):
    user_input = user_input.lower()
    for category, data in input_map.items():
        for keyword in data['keywords']:
            if re.search(r'\b' + re.escape(keyword) + r'\b', user_input):
                return data['node']
    return None  # or a default node like 'life'
