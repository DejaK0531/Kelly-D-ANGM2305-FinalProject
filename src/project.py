import pygame
import sys


def main():
    pygame.init()
    screen_width = 750
    screen_height = 660
    screen = pygame.display.set_mode((screen_width, screen_height))
    intro_bg = pygame.image.load('intro_bg.png')
    background = pygame.image.load('rocket_kitty_bg.png')
    icon = pygame.image.load('rocket_kitty_icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Rocket Kitty Blast!")
    clock = pygame.time.Clock()

    
    # fade in the logo
    fade_duration = 2000  # in milliseconds (2 seconds)
    fade_start_time = pygame.time.get_ticks()
    pygame.time.delay(15)  # Add a small delay for a smoother fade-in

    running = True
    while running:
        # Checking for events
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - fade_start_time

        if elapsed_time < fade_duration:
            alpha = int((elapsed_time / fade_duration) * 255)
            intro_bg.set_alpha(alpha)
            screen.blit(pygame.transform.scale(intro_bg, (750, 660)), (0, 0))

        else:
            # Image stays on screen for a few seconds before fading out
            screen.blit(pygame.transform.scale(background, (750, 660)), (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()
    pygame.display.update()

if __name__ == "__main__":
    main()