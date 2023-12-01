import pygame
import sys
import os
import random
from obstacles import Block

os.chdir(os.path.dirname(os.path.abspath(__file__)))

screen_width = 750  # Define screen_width globally
screen_height = 660  # Define screen_height globally

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, alien_group, screen):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5
        self.visible = True
        self.alien_group = alien_group
        self.screen = screen

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < screen_width - self.image.get_width():
            self.rect.x += self.speed

        if self.visible:
            # Check for collisions between player and aliens
            player_alien_collision = pygame.sprite.spritecollide(self, self.alien_group, True)
            if player_alien_collision:
                # Implement player death actions here (e.g., make the player invisible)
                self.visible = False
                self.rect.topleft = (-100, -100)  # Move the player off-screen

        # Only update if the player is visible
        if self.visible:
            self.screen.blit(self.image, self.rect.topleft)
                
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.image.load('rocket_kitty_alien.png')
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 10

    def update(self):
        global screen_width, screen_height  # Declare global variables
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed = -self.speed
            self.rect.y += 20

class AlienGroup(pygame.sprite.Group):
    def __init__(self, number_of_aliens, alien_size):
        super().__init__()
        self.create_aliens(number_of_aliens, alien_size)
        self.alien_size = alien_size

    def create_aliens(self, number_of_aliens, alien_size):
        for _ in range(number_of_aliens):
            x = random.randint(0, screen_width - alien_size)
            y = random.randint(50, 200)
            alien = Alien(x, y, alien_size)
            self.add(alien)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, obstacle_group, alien_group):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10
        self.obstacle_group = obstacle_group
        self.alien_group = alien_group

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

        # Check for collisions with obstacles
        obstacle_collision = pygame.sprite.spritecollide(self, self.obstacle_group, True)
        if obstacle_collision:
            self.kill()

        # Check for collisions with aliens
        alien_collision = pygame.sprite.spritecollide(self, self.alien_group, True)
        if alien_collision:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    shape = [
        "  xxxxxxx",
        " xxxxxxxxx",
        "xxxxxxxxxxx",
        "xxxxxxxxxxx",
        "xxxxxxxxxxx",
        "xxx     xxx",
        "xx       xx"
    ]
    
    def __init__(self, screen_width):
        super().__init__()
        self.shape = Obstacle.shape
        self.block_size = 7
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = screen_width / 15, y_start = 505)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Block(self.block_size, (6, 201, 145), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

def fade_in_intro(screen, intro_bg, fade_duration, fade_start_time):
    pygame.time.delay(15)
    elapsed_time = 0

    while elapsed_time < fade_duration:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - fade_start_time

        alpha = int((elapsed_time / fade_duration) * 255)
        intro_bg.set_alpha(alpha)

        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(intro_bg, (screen_width, screen_height)), (0, 0))
        pygame.display.flip()

def main():
    global screen_width, screen_height, alien_group  # Declare variables as global

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    intro_bg = pygame.image.load('intro_bg.png')
    background = pygame.image.load('rocket_kitty_bg.png')
    player_img = pygame.image.load('rocket_kitty_player.png')
    icon = pygame.image.load('rocket_kitty_icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Rocket Kitty Blast!")
    clock = pygame.time.Clock()
    fade_duration = 2000  # in milliseconds (2 seconds)
    fade_start_time = pygame.time.get_ticks()

    # fade in the logo
    fade_in_intro(screen, intro_bg, fade_duration, fade_start_time)

    # Move the initialization of alien_group before creating the Player instance
    alien_group = AlienGroup(number_of_aliens=15, alien_size=55)

    player = Player(screen_width // 2 - player_img.get_width() // 2, screen_height - player_img.get_height(), player_img, alien_group, screen)

    lasers = pygame.sprite.Group()
    obstacle = Obstacle(screen_width)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                laser = Laser(player.rect.x + player_img.get_width() // 2, player.rect.y, obstacle.blocks, alien_group)
                lasers.add(laser)

        player.update()

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - fade_start_time

        if elapsed_time < fade_duration:
            alpha = int((elapsed_time / fade_duration) * 255)
            intro_bg.set_alpha(alpha)
            screen.blit(pygame.transform.scale(intro_bg, (screen_width, screen_height)), (0, 0))
        else:
            screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
            screen.blit(player.image, player.rect.topleft)

        lasers.update()
        lasers.draw(screen)
        obstacle.blocks.update()
        obstacle.blocks.draw(screen)
        alien_group.update()
        alien_group.draw(screen)

        # Check for collisions between lasers and obstacles
        laser_obstacle_collision = pygame.sprite.groupcollide(lasers, obstacle.blocks, True, True)
        # Check for collisions between lasers and aliens
        laser_alien_collision = pygame.sprite.groupcollide(lasers, alien_group, True, True)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()