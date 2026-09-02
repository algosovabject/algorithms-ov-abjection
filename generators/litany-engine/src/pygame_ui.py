from pathlib import Path

import pygame

from src.litany import load_litany_graph
from src.input_parser import parse_input

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

BACKGROUND = (20, 20, 20)
TEXT_COLOR = (220, 220, 220)
BORDER_COLOR = (120, 120, 120)

VIEWPORT_RECT = pygame.Rect(
    40,
    80,
    820,
    350
)

STATUS_RECT = pygame.Rect(
    40,
    450,
    820,
    90
)

COMMAND_RECT = pygame.Rect(
    40,
    560,
    820,
    100
)

ENGINE_DIR = Path(__file__).resolve().parent.parent
NODES_PATH = ENGINE_DIR / "data" / "nodes.yml"
EDGES_PATH = ENGINE_DIR / "data" / "edges.yml"

def run_ui():

    pygame.init()

    G = load_litany_graph(
    NODES_PATH,
    EDGES_PATH
    )

    screen = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    pygame.display.set_caption(
        "LITANY ENGINE"
    )

    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont(
        "monospace",
        32
    )

    text_font = pygame.font.SysFont(
        "monospace",
        20
    )

    user_input = ""
    active_states = []
    status = "IDLE"
    active_state = None
    active_visual = None

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                elif event.key == pygame.K_RETURN:
                    # Handle command execution here
                    if user_input.strip():

                        active_states = parse_input(
                            user_input,
                            G
                        )

                        if active_states:
                            status = "ACTIVE"

                            active_state = active_states[0]
                            visual_path = G.nodes[active_state].get("visual")

                            if visual_path:
                                active_visual = pygame.image.load(
                                    visual_path
                                ).convert()

                                active_visual = pygame.transform.scale(
                                    active_visual,
                                    (VIEWPORT_RECT.width, VIEWPORT_RECT.height)
                                )
                            else:
                                active_visual = None

                        else:
                            status = "NO SIGNAL"
                            active_state = None
                            active_visual = None

                        print("SIGNAL RECEIVED.")
                        print(f"ACTIVE STATES: {active_states}")

                        user_input = ""

                else:
                    user_input += event.unicode

        screen.fill(BACKGROUND)

        # Title

        title = title_font.render(
            "LITANY ENGINE",
            True,
            TEXT_COLOR
        )

        screen.blit(
            title,
            (40, 25)
        )

        # Viewport
        if active_visual:
            screen.blit(
                active_visual,
                VIEWPORT_RECT.topleft
            )
            
        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            VIEWPORT_RECT,
            2
        )

        # Status panel

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            STATUS_RECT,
            2
        )

        status_text = text_font.render(
            f"STATUS: {status}",
            True,
            TEXT_COLOR
        )

        screen.blit(
            status_text,
            (55, 470)
        )

        if active_states:

            states_text = text_font.render(
                "ACTIVE STATES: " + " / ".join(
                    state.upper()
                    for state in active_states
                ),
                True,
                TEXT_COLOR
            )

            screen.blit(
                states_text,
                (55, 500)
            )

        # Command panel

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            COMMAND_RECT,
            2
        )

        command_text = text_font.render(
            f"> {user_input}",
            True,
            TEXT_COLOR
        )

        screen.blit(
            command_text,
            (55, 600)
        )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()