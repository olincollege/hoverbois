import sys
import pygame

# Constants to tweak when testing physical robot
MAX_HOVER = 40
MAX_THROTTLE = 40

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
    # Cries in Python < 3.10
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
                    controller: pygame.joystick.Joystick) -> int:
    """
    Configure which axis to use for controller.

    Args:
        controllers: A list of pygame joystick.Joystick devices.
        screen: A pygame surface to draw on.

    Returns:
        Int representing axis to use for analog control. If no axis, return -1.
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


def axis_deadzone(screen: pygame.surface.Surface,
                  controller: pygame.joystick.Joystick,
                  axis: int) -> float:
    """
    Configure axis deadzone and center.

    Args:
        controllers: A list of pygame joystick.Joystick devices.
        screen: A pygame surface to draw on.
        axis: An int representing the axis number to use.

    Returns:
        Tuple of two floats. First float is an offset to center joystick.
        Second float is the deadzone threshold.
    """
    num_axes = controller.get_numaxes()
    if num_axes == 0:
        print("Controller has no analog.")
        return -1

    x_center = screen.get_size()[0]/2
    y_center = screen.get_size()[1]/2
    pygame.display.set_caption("Set axis deadzone")

    instructions = ("Recenter axis and set deadzone.",
                    "Press space to center axis.",
                    "Use arrow keys to adjust deadzone.",
                    "Press Enter to select.")

    offset = 0
    deadzone = 0

    while True:
        # Process Inputs
        reading = controller.get_axis(axis)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Goodbye")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                action = get_select_input(event.key,
                                          special={pygame.K_SPACE: "center"})
                # Cries in Python < 3.10
                if action == "select":
                    return offset, deadzone
                if action == "center":
                    offset = reading
                if action == "prev":
                    deadzone -= 0.005
                if action == "next":
                    deadzone += 0.005
                deadzone = max(0, deadzone)

        adjusted = reading - offset
        # Redraw Screen
        screen.fill(BACKGROUND)
        draw_instructions(screen, instructions)
        pygame.draw.line(screen, COLORS["white"],
                         (x_center, y_center), (x_center+adjusted*300, y_center),
                         width=40)
        for i in (-1, 1):
            pygame.draw.line(screen, COLORS["black"],
                             (x_center+i*(deadzone*300), y_center-30),
                             (x_center+i*(deadzone*300), y_center+30),
                             width=2)
        pygame.display.flip()


def pick_button(screen: pygame.surface.Surface,
                controller: pygame.joystick.Joystick,
                name: str) -> int:
    """
    Pick a button.

    Args:
        controllers: A list of pygame joystick.Joystick devices.
        screen: A pygame surface to draw on.
        name: The name of the action to display in instructions.

    Returns:
        An int representing the controller button pressed.
    """
    num_axes = controller.get_numaxes()
    pygame.display.set_caption(f"Pick button for {name}")

    button = 0

    while True:
        # Process Inputs
        for i in range(controller.get_numbuttons()):
            if controller.get_button(i) == True:
                button = i

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Goodbye")
                sys.exit()

            if event.type == pygame.KEYDOWN:
                action = get_select_input(event.key)
                if action == "select":
                    return button

        # Redraw Screen
        screen.fill(BACKGROUND)
        instructions = (f"Press button to use for {name}.",
                        "Press Enter to confirm.",
                        f"Current button: {button}")
        draw_instructions(screen, instructions)
        pygame.display.flip()


def read_buttons(controller: pygame.joystick.Joystick) -> list[bool]:
    """
    Read all buttons from a controller.

    Args:
        controller: A pygame joystick.Joystick object.

    Returns:
        A list of bools.
    """
    return [controller.get_button(i)
            for i in range(controller.get_numbuttons())]


def calculate_button_state(prev: list[bool], curr: list[bool]) -> list[str]:
    """
    Calculate whether every button is unpressed, pressed, held, or released.

    Lists MUST be of equal length.

    Because an A press actually has three parts to it. It's the pressing that
    we want.

    Args:
        prev: A list of bools representing binary state of buttons last read.
        curr: A list of bools representing binary state of buttons this read.

    Returns:
        A list of strings, where the strings are "unpressed", "pressed", "held",
        or "released".
    """
    def find_state(prev, curr):
        # Cries in Python < 3.10
        if prev == False and curr == True:
            return "pressed"
        if prev == True and curr == False:
            return "released"
        if curr == True:
            return "held"
        return "unpressed"
    return [find_state(prev[x], curr[x]) for x in range(len(prev))]


def main():
    robot_state = {"hover"       : 0,
                   "throttle"    : 0,
                   "angular_vel" : 0, }

    def estop(): # TODO: make this send a special thing instead
        for key in robot_state.keys():
            robot_state[key] = 0
        # TODO: send_to_radio(message)
        print("ESTOP")


    def hover_plus():
        # TODO: send_to_radio(message)
        robot_state["hover"] = min(MAX_HOVER, robot_state["hover"]+5)

    def hover_minus():
        # TODO: send_to_radio(message)
        robot_state["hover"] = max(0, robot_state["hover"]-5)

    def throttle_plus():
        # TODO: send_to_radio(message)
        robot_state["throttle"] = min(MAX_THROTTLE, robot_state["throttle"]+5)

    def throttle_minus():
        # TODO: send_to_radio(message)
        robot_state["throttle"] = max(0, robot_state["throttle"]-5)

    # Setup pygame
    pygame.init()
    pygame.font.init()

    # Setup controllers
    pygame.joystick.init()
    controllers = [pygame.joystick.Joystick(x)
                   for x in range(pygame.joystick.get_count())]

    # Setup canvas
    screen = pygame.display.set_mode(SIZE)
    # Commented out because limiting framerate doesn't matter for us.
    # clock = pygame.time.Clock()

    # Setup controller
    controller_num = pick_controller(controllers, screen)
    controller = controllers[controller_num]
    axis = controller_axis(screen, controller)
    offset, deadzone = axis_deadzone(screen, controller, axis)

    angular_vel_scalar = 100 # TODO: This should probably be configurable during runtime

    button_map = {
        # button num : ("state", action_func)
        pick_button(screen, controller, "ESTOP")             : ("pressed", estop),
        pick_button(screen, controller, "Increase Hover")    : ("pressed", hover_plus),
        pick_button(screen, controller, "Decrease Hover")    : ("pressed", hover_minus),
        pick_button(screen, controller, "Increase Throttle") : ("pressed", throttle_plus),
        pick_button(screen, controller, "Decrease Throttle") : ("pressed", throttle_minus),
    }

    # Initialize these to ensure they are same size and exist
    pygame.display.set_caption("Drive Robot")
    buttons_prev = read_buttons(controller)
    buttons_curr = read_buttons(controller)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Read Inputs
        buttons_prev  = buttons_curr
        buttons_curr  = read_buttons(controller)
        buttons_state = calculate_button_state(buttons_prev, buttons_curr)
        axis_raw  = controller.get_axis(axis)

        axis_processed = axis_raw - offset
        if abs(axis_processed) < deadzone:
            axis_processed = 0

        # Process Inputs
        for button_num, action in button_map.items(): # Button map
            if buttons_state[button_num] == action[0]:
                action[1]()

        robot_state["angular_vel"] = int(angular_vel_scalar * axis_processed)
        # TODO: send_to_radio(message)

        hud_text = []
        for x,y in robot_state.items():
            hud_text.append(f"{x}")
            hud_text.append(f"{y}")
            hud_text.append("")

        # Redraw Screen
        screen.fill(BACKGROUND)
        draw_instructions(screen, hud_text)
        pygame.display.flip()


if __name__ == "__main__":
    main()
