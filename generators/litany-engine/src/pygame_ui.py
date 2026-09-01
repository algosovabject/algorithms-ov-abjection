import pygame

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


def run_ui():

    pygame.init()

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

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

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
            "STATUS: IDLE",
            True,
            TEXT_COLOR
        )

        screen.blit(
            status_text,
            (55, 470)
        )

        # Command panel

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            COMMAND_RECT,
            2
        )

        command_text = text_font.render(
            "> _",
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