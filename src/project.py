import pygame
import sys



def main():
    pygame.init()
    screen_width = 750
    screen_height = 660
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rocket Kitty Blast")
    icon = pygame.image.load('rocket_kitty.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    #background = (0, 0, 0)
    #intro_bg = pygame.image.load('bg.png')
    background = pygame.image.load('rocket_kitty_bg.png')

    running = True
    while running:
        # Checking for events
        screen.blit(pygame.transform.scale(background, (750, 660)), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()