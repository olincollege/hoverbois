import sys
import pygame

# Useful constants
COLORS = {"black": (0, 0, 0),
          "white": (255, 255, 255),
          "gray_mid": (127, 127, 127),
          "gray_dark": (60, 60, 60),
          "gray_light": (190, 190, 190),
          "blue": (0, 0, 255), }
BACKGROUND = COLORS["gray_mid"]

SIZE = WIDTH, HEIGHT = 640, 480


def print_controller_info(controller: pygame.joystick.Joystick):
    """
    Print state of controller axis and buttons.

    For debugging.

    Args:
        controller: A pygame joystick.Joystick type.
    """
    axis = [controller.get_axis(x)
            for x in range(controller.get_numaxes())]
    button = [controller.get_button(x)
              for x in range(controller.get_numbuttons())]
    print(axis, button)


def pick_controller(controllers: list[pygame.joystick.Joystick],
                    screen: pygame.Surface) -> int:
    """
    Prompt user to pick controller.

    Returns:
        An int representing joystick ID in SDL. -1 means keyboard instead of
        a joystick.
    """
    if len(controllers) == 0:
        print("No controllers found, using keyboard.")
        return -1

    pygame.display.set_caption("Pick Controller")

    font_large = pygame.font.SysFont("freesansbold", 50)
    font_small = pygame.font.SysFont("freesansbold", 30)

    instructions_str = ("Pick a controller using arrow keys.",
                        "Press Enter to select.",
                        "Press K to use keyboard.", )
    instructions_font = []
    instructions_rect = []
    for i in range(len(instructions_str)):
        instructions_font.append(font_small.render(instructions_str[i],
                                                   True, COLORS["white"]))
        instructions_rect.append(instructions_font[i].get_rect())
        instructions_rect[i].center = (WIDTH/2, 40+20*i)

    controller = 0
    # Perhaps these should be functions to call instead
    keybinds = {pygame.K_UP: "prev",
                pygame.K_DOWN: "next",
                pygame.K_LEFT: "prev",
                pygame.K_RIGHT: "next",
                pygame.K_k: "prev",  # Vim
                pygame.K_j: "next",  # Vim
                pygame.K_p: "prev",  # Emacs
                pygame.K_n: "next",  # Emacs
                pygame.K_k: "keyboard",
                pygame.K_RETURN: "select", }

    while True:
        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Goodbye")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                action = keybinds.get(event.key)
                # Cries in Python 3.9
                if action == "prev":
                    controller -= 1
                    if controller < 0:
                        controller = len(controllers) - 1
                elif action == "next":
                    controller += 1
                    if controller >= len(controllers):
                        controller = 0
                elif action == "keyboard":
                    return -1
                elif action == "select":
                    return controller

            selected = font_large.render(controllers[controller].get_name(),
                                         True,
                                         COLORS["white"])
            selected_rect = selected.get_rect()
            selected_rect.center = (WIDTH/2, HEIGHT/2)

        # Redraw Screen
        screen.fill(BACKGROUND)
        for i in range(len(instructions_font)):
            screen.blit(instructions_font[i], instructions_rect[i])
        screen.blit(selected, selected_rect)
        pygame.display.flip()


def main():
    pygame.init()

    # Setup controllers
    pygame.joystick.init()
    controllers = [pygame.joystick.Joystick(x)
                   for x in range(pygame.joystick.get_count())]

    # Setup text
    pygame.font.init()

    # Setup canvas
    screen = pygame.display.set_mode(SIZE)

    clock = pygame.time.Clock()

    pick_controller(controllers, screen)

    while True:
        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Redraw Screen
        screen.fill(BACKGROUND)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
