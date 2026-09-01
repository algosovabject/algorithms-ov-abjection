def parse_input(user_input, G):

    user_input = user_input.lower()

    matches = []

    for node_id, data in G.nodes(data=True):

        keywords = data.get("keywords", [])

        for keyword in keywords:

            if keyword.lower() in user_input:
                matches.append(node_id)
                break

    return matches
