import pygame
import sys
from network import Network
from fighter import Fighter

# Test git comment by Jack 
# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game")

# Networking
clientNumber = 0

# Game variables
FPS = 60
clock = pygame.time.Clock()
speed = 5  # Movement speed
ANIMATION_TIME = 6  # Speed of the animation

# Load background image
# Replace 'background.jpg' with the correct path to your background image file
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def redrawWindow(screen, fighter, fighter2):
    # Draw background
    screen.blit(background, (0, 0)) # maybe fill?
    fighter.draw(screen)
    fighter2.draw(screen)
    # Update display
    pygame.display.update()
 

projectiles = []

def main():
    # Networking
    n = Network()
    p = n.getP()
    # Game loop
    running = True
    while running:
        p2 = n.send(p)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Update the fighter's vertical position
        p.update_vertical_movement()
    # Drawing the projectiles
        for projectile in projectiles[:]:
            projectile.move()
            if projectile.rect.x < 0 or projectile.rect.x > WIDTH:
                projectiles.remove(projectile)

        if p.punching and p.current_frame in p.punch_frame_at_hit_point:
            p.check_punch_collision(p, p2)

        
        # Update the fighters
        p.update()
        p2.update()

        # Draw fighter
        p.draw(screen)
        p2.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)

        p.animate()
        p2.animate()
        
        p.move()
        redrawWindow(screen, p, p2)
        # redrawWindow(screen, fighter2)
        # Tick the clock
        clock.tick(FPS)

main()
# Quit Pygame
pygame.quit()
sys.exit()
