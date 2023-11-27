import pygame
import sys



def main():
    pygame.init()
    screen_width = 750
    screen_height = 700
    gray = (29, 29, 27)
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rockett Kitty Blast")
    #clock = pygame.time.Clock()
    while True:
        # Checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(gray)
        #pygame.display.update()
        #clock.tick(60)

if __name__ == "__main__":
    main()