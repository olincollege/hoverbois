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


def draw_instructions(screen: pygame.Surface, instructions: tuple[str]):
    """
    Draw instructions for controller setup wizard.

    Args:
        instructions: A tuple of strings.
    """
    x_center = screen.get_size()[0]/2

    font = pygame.font.SysFont("freesansbold", 40)

    for i in range(len(instructions)):
        instruction = instructions[i]
        text = font.render(instruction, True, COLORS["white"])
        rect = text.get_rect()
        rect.center = (x_center, 40+24*i)
        screen.blit(text, rect)


def get_select_input(key, special=None):
    """
    Figure out action to take for select menu.

    Args:
        key: A Pygame event for the keypress.
        special: An optional dict containing special keybind action pairs.

    Returns:
        A string representing prev, next, select, or a special option. Returns
        none if match is not found.
    """
    if special is None:
        special = {}

    default = {pygame.K_UP: "prev",
               pygame.K_DOWN: "next",
               pygame.K_LEFT: "prev",
               pygame.K_RIGHT: "next",
               pygame.K_k: "prev",  # Vim
               pygame.K_j: "next",  # Vim
               pygame.K_p: "prev",  # Emacs
               pygame.K_n: "next",  # Emacs
               pygame.K_RETURN: "select", }
    keybinds = default | special  # Yay for Python 3.9!
    return keybinds.get(key)


def next_selection(value, num, action):
    """
    Function to make it easier to loop list circularly.

    Args:
        value: Current value of selection.
        num: Number of total selections.
        action: A string representing action to take, ("next", "prev").
    """
    # Cries in Python 3.9
    next = value
    if action == "prev":
        next = value - 1
        if next < 0:
            return num - 1
    elif action == "next":
        next = value + 1
        if next >= num:
            return 0
    return next


def pick_controller(controllers: list[pygame.joystick.Joystick],
                    screen: pygame.Surface) -> int:
    """
    Prompt user to pick controller.

    Args:
        controllers: A list of pygame joystick.Joystick devices.
        screen: A pygame surface to draw on.

    Returns:
        An int representing joystick ID in SDL. -1 means keyboard instead of
        a joystick.
    """
    if len(controllers) == 0:
        print("No controllers found, using keyboard.")
        return -1

    pygame.display.set_caption("Pick Controller")

    instructions = ("Pick a controller using arrow keys.",
                    "Press Enter to select.",
                    "Press K to use keyboard.", )

    controller = 0
    font = pygame.font.SysFont("freesansbold", 30)

    while True:
        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Goodbye")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                action = get_select_input(event.key, {pygame.K_k: "keyboard"})
                controller = next_selection(controller,
                                            len(controllers),
                                            action)
                if action == "keyboard":
                    return -1
                if action == "select":
                    return controller

            selected = font.render(controllers[controller].get_name(),
                                   True,
                                   COLORS["white"])
            selected_rect = selected.get_rect()
            selected_rect.center = (WIDTH/2, HEIGHT/2)

        # Redraw Screen
        screen.fill(BACKGROUND)
        draw_instructions(screen, instructions)
        screen.blit(selected, selected_rect)
        pygame.display.flip()


def controller_axis(screen: pygame.surface.Surface,
                    controller: pygame.joystick.Joystick):
    """
    Configure which axis to use for controller.

    Args:
        controllers: A list of pygame joystick.Joystick devices.
        screen: A pygame surface to draw on.

    Returns:
        Number representing axis to use for analog control. If no axis, return
        -1.
    """
    axis = 0
    num_axes = controller.get_numaxes()
    if num_axes == 0:
        print("Controller has no analog.")
        return -1

    x_center = screen.get_size()[0]/2
    pygame.display.set_caption("Select Controller Axis")

    instructions = ("Play with your controller's joysticks.",
                    "Pick an axis to use for steering.",
                    "Use arrow keys.",
                    "Press Enter to select.")

    while True:
        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Goodbye")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                action = get_select_input(event.key)
                axis = next_selection(axis,
                                      num_axes,
                                      action)
                if action == "select":
                    return axis

        # Redraw Screen
        screen.fill(BACKGROUND)
        draw_instructions(screen, instructions)
        for i in range(num_axes):
            y = 150 + 30*i
            reading = controller.get_axis(i) * 100
            color = COLORS["white"]
            if i == axis:
                color = COLORS["blue"]
            pygame.draw.line(screen, color,
                             (x_center, y+12), (x_center+reading, y+12),
                             width=15)
            pygame.draw.line(screen, COLORS["black"],
                             (x_center, y), (x_center, y+24),
                             width=2)
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

    controller_num = pick_controller(controllers, screen)
    controller = controllers[controller_num]
    controller_axis(screen, controller)

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
