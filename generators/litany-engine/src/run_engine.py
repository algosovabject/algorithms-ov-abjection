from litany import load_litany_graph
from input_parser import parse_input
from memory import log_query

NODES_PATH = "data/nodes.yml"
EDGES_PATH = "data/edges.yml"

def main():

    G = load_litany_graph(
        NODES_PATH,
        EDGES_PATH
    )

    session = {
        "inputs": [],
        "path": [],
        "active_nodes": [],
        "status": "idle"
    }

    print("LITANY ENGINE")
    print("READY.")

    while True:

        command = input(
            "\nCOMMAND [FEED / MUTATE / INTERRUPT / KILL]:"
        ).strip().upper()

        if command == "KILL":
            print("THROATS SLASHED.")
            break

        elif command == "FEED":

            if session["status"] != "idle":
                print("LITANY ALREADY ACTIVE.")
                continue

            query = input("FEED >")

            session["inputs"].append(query)
            session["status"] = "active"

            matches = parse_input(
                query,
                G
            )

            session["active_nodes"] = matches

            print("SIGNAL RECEIVED.")
            print(f"ACTIVE STATES: {matches}")

        elif command == "MUTATE":

            if session["status"] != "active":
                print("NO ACTIVE LITANY.")
                continue

            mutation = input("MUTATE > ")

            session["inputs"].append(mutation)

            full_input = "\n".join(session["inputs"])

            matches = parse_input(
                full_input,
                G
            )

            session["active_nodes"] = matches
        
            print("INPUT MUTATED.")
            print(f"ACTIVE STATES: {matches}")

        elif command == "INTERRUPT":

            session["status"] = "interrupted"

            print("SIGNAL INTERRUPTED.")

        else:
            print("UNKNOWN COMMAND.")

if __name__ == "__main__":
    main()
