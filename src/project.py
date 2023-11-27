import pygame
import sys



def main():
    pygame.init()
    screen_width = 750
    screen_height = 660
    screen = pygame.display.set_mode((screen_width, screen_height))
    intro_bg = pygame.image.load('intro_bg.png')
    background = pygame.image.load('rocket_kitty_bg.png')
    icon = pygame.image.load('rocket_kitty.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Rocket Kitty Blast")
    clock = pygame.time.Clock()

    
    # fade in the logo
    for i in range(255):
        screen.fill((0,0,0))
        intro_bg.set_alpha(i)
        screen.blit(pygame.transform.scale(intro_bg, (750, 660)), (0,0))
        pygame.display.flip()

    running = True
    while running:
        # Checking for events
        screen.blit(pygame.transform.scale(background, (750, 660)), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(20)

if __name__ == "__main__":
    main()