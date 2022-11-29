import sys, pygame
pygame.init()
pygame.joystick.init()

size = width, height = 640, 480

colors = {"black" : (0, 0, 0),
          "white" : (255, 255, 255),
          "gray"  : (127, 127, 127), }
background = colors["gray"]

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:
    # Process Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # Update state

    # Redraw Screen
    screen.fill(background)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick(60)
