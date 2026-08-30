from oracle import load_oracle_graph, weighted_pseudopod_walk
from input_parser import load_input_map, parse_input
from memory import log_query
from responses import get_flavor_line
from mood_engine import get_oracle_mood
from responses import get_flavor_line, get_season_flavor
import random

mood = get_oracle_mood()
print(f"[Mood: {mood['vibe']}]")
print(get_flavor_line(mood["usage"]))
print(get_season_flavor(mood["season"]))

# Pick a random mood aspect to flavor the oracle's behavior
mood_choice = random.choice(['time', 'moon', 'usage', 'season'])
mood_key = mood.get(mood_choice, "")

# Get a flavor line for the chosen mood
flavor_line = get_flavor_line(mood_key)
print(flavor_line)

if __name__ == "__main__":
    mood = get_oracle_mood()
    print(f"[Mood: {mood['vibe']}]")

    if mood["usage"] == "repetitive":
        print("*blorp* The ooze makes a rude noise. You've asked this too many times.")
    elif mood["usage"] == "varied":
        print("The ooze wiggles excitedly. It likes your curiosity.")

    user_input = input("Ask the Ooze Oracle your question (or type 'mood'): ")

    if user_input.lower().strip() == "mood":
        print(f"The ooze is currently feeling: {mood['vibe']}")
        exit()

    G = load_oracle_graph("data/oracle_nodes.yaml", "data/oracle_edges.yaml")
    input_map = load_input_map("data/input_map.yaml")
    user_input = input("Ask the Ooze Oracle your question: ")
    start_node = parse_input(user_input, input_map)

    if start_node is None:
        responses = [
        "The ooze gurgles uncertainly... it does not understand.",
        "The slime sloshes side to side, uncomprehending.",
        "A ripple passes through the slime... but it says nothing.",
        "The ooze bubbles then deflates. You are ignored."
        ]
        print(random.choice(responses))
    else:
        path = weighted_pseudopod_walk(G, start=start_node)
        matched_tags = G.nodes[start_node]['tags']
        log_query(question, path, matched_tags)
        print("The oracle blorps quietly... it remembers this.")
        
        print("Your path through the Oracle of Ooze:")
        for node in path:
            print(f"> {G.nodes[node]['label']}: {G.nodes[node]['meaning']}")

def get_flavor_line(mood_phrase):
    return random.choice(MOOD_RESPONSES.get(mood_phrase, ["The ooze oozes in silence."]))