import pygame
import sys

# Test git comment by Jack 
# Initialize Pygame
pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game")

# Game variables
FPS = 60
clock = pygame.time.Clock()
speed = 5  # Movement speed
ANIMATION_TIME = 6  # Speed of the animation

# Load background image
# Replace 'background.jpg' with the correct path to your background image file
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load character frames
idle_frames_r = [pygame.image.load(f'0{i}.gif') for i in range(1, 5)]
idle_frames_l = [pygame.transform.flip(frame, True, False) for frame in idle_frames_r]  # Flip frames for idle left
walk_frames_r = [pygame.image.load(f'walk/0{i}.gif') for i in range(1, 9)]
walk_frames_l = [pygame.transform.flip(frame, True, False) for frame in walk_frames_r]  # Flip frames for walking left
punch_frames_r = [pygame.image.load(f'punch/0{i}.gif') for i in range(1, 9)]
punch_frames_l = [pygame.transform.flip(frame, True, False) for frame in punch_frames_r]  # Flip frames for punching left
block_frames_r = [pygame.image.load(f'block/0{i}.gif') for i in range(1, 4)]
block_frames_l = [pygame.transform.flip(frame, True, False) for frame in block_frames_r]  # Flip frames for blocking left
duck_frames_r = [pygame.image.load(f'duck/d0{i}.gif') for i in range(1, 4)]
duck_frames_l = [pygame.transform.flip(frame, True, False) for frame in duck_frames_r]
special_frames_r = [pygame.image.load(f'special/f0{i}.gif') for i in range(1, 4)]
special_frames_l = [pygame.transform.flip(frame, True, False) for frame in special_frames_r]
# Load jump frames
jump_frames_r = [pygame.image.load(f'jump/f0{i}.gif') for i in range(1, 9)]
jump_frames_l = [pygame.transform.flip(frame, True, False) for frame in jump_frames_r]
hit_reaction_frames_r = [pygame.image.load(f'hitdetect/h0{i}.gif') for i in range(1, 4)]
hit_reaction_frames_l = [pygame.transform.flip(frame, True, False) for frame in hit_reaction_frames_r]  # Flip frames for hit reaction left

# Load character frames for ducking
class Projectile:
    def __init__(self, x, y, facing_left):
        self.image = pygame.image.load('special/f10.PNG')  # Load your projectile image here
        self.rect = self.image.get_rect(center=(x, y))
        self.facing_left = facing_left
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed = 10 if not facing_left else -10

    def move(self):
        self.rect.x += self.speed
        print("Projectile moved to", self.rect.x)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Character class
class Fighter:
    def __init__(self, x, y, idle_frames_r, idle_frames_l, walk_frames_r, walk_frames_l, punch_frames_r, punch_frames_l, block_frames_r, block_frames_l, duck_frames_r, duck_frames_l, special_frames_r, special_frames_l, jump_frames_r, jump_frames_l, hit_reaction_frames_r, hit_reaction_frames_l):
        self.x = x
        self.y = y
        self.idle_frames_r = idle_frames_r
        self.idle_frames_l = idle_frames_l
        self.walk_frames_r = walk_frames_r
        self.walk_frames_l = walk_frames_l
        self.punch_frames_r = punch_frames_r
        self.punch_frames_l = punch_frames_l
        self.block_frames_r = block_frames_r
        self.block_frames_l = block_frames_l
        self.duck_frames_r = duck_frames_r
        self.duck_frames_l = duck_frames_l
        self.special_frames_r = special_frames_r
        self.special_frames_l = special_frames_l
        self.current_frame = 0
        self.image = idle_frames_r[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_count = 0
        self.facing_left = False
        self.moving = False
        self.punching = False
        self.blocking = False
        self.ducking = False
        self.special = False
        self.jump_frames_r = jump_frames_r
        self.jump_frames_l = jump_frames_l
        self.jumping = False
        self.jump_frame_index = 0
        self.jump_speed = -17  # The initial upward speed for a jump
        self.gravity = 0.5  # The force pulling the fighter down
        self.vertical_velocity = 0  # The current vertical speed
        self.grounded = True  # Indicates if the fighter is on the ground
        self.hitbox = self.rect.inflate(-1, -5)  # Adjust the values as needed
        self.hit_reacting = False
        self.hit_reaction_frames_r = hit_reaction_frames_r
        self.hit_reaction_frames_l = hit_reaction_frames_l
        self.punch_frame_at_hit_point = [2,3,6,8,9]

    def animate(self):
        self.animation_count += 1
        frames = self.idle_frames_l if self.facing_left else self.idle_frames_r
        if self.jumping:
            frames = self.jump_frames_l if self.facing_left else self.jump_frames_r
        elif self.special: 
            frames = self.special_frames_l if self.facing_left else special_frames_r
        elif self.blocking:
            frames = self.block_frames_l if self.facing_left else self.block_frames_r
        elif self.punching:
            frames = self.punch_frames_l if self.facing_left else self.punch_frames_r
        elif self.moving:
            frames = self.walk_frames_l if self.facing_left else self.walk_frames_r
        elif self.ducking:
            frames = self.duck_frames_l if self.facing_left else self.duck_frames_r
        
        if self.animation_count >= ANIMATION_TIME:
            self.animation_count = 0
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]
            if self.special and self.current_frame == 0:
                self.special = False
            if self.punching and self.current_frame == 0:
                self.punching = False  # Reset punching state after the animation
            if self.blocking and self.current_frame == 0:
                self.blocking = False  # Reset blocking state after the animation
            if self.jumping and self.current_frame == 0:
                self.jumping = False
    def update_hitbox(self):
        # Update the hitbox position to follow the character
        self.hitbox.x = self.rect.x + 10  # Offset if necessary
        self.hitbox.y = self.rect.y + 10  # Offset if necessary

    def get_hit(self):
        if not self.hit_reacting:
            self.hit_reacting = True
            self.current_frame = 0

    def update_hit_reaction(self):
        if self.hit_reacting:
            frames = self.hit_reaction_frames_l if self.facing_left else self.hit_reaction_frames_r
            if self.current_frame < len(frames):
                self.image = frames[self.current_frame]
                self.current_frame += 1
            else:
                self.hit_reacting = False
                self.current_frame = 0  # Reset to idle or other post-hit state

    def start_jump(self):
        if self.grounded:  # The fighter can only jump if they are on the ground
            self.jumping = True
            self.grounded = False
            self.vertical_velocity = self.jump_speed

    def update_vertical_movement(self):
        if not self.grounded:
            self.vertical_velocity += self.gravity
            self.y += self.vertical_velocity
            self.rect.y = self.y

            # Check if the fighter is on the ground
            if self.y >= HEIGHT - 200:  # 200 is where the ground level is, adjust as needed
                self.y = HEIGHT - 200
                self.rect.y = self.y
                self.vertical_velocity = 0
                self.grounded = True
                self.jumping = False

    def update_jump_animation(self):
        if self.jumping:
            self.jump_frame_index += 1
            if self.jump_frame_index >= len(self.jump_frames_r):
                self.jump_frame_index = 0  # Optionally reset to loop the animation or stop at the last frame
            self.image = (self.jump_frames_l[self.jump_frame_index] if self.facing_left 
                          else self.jump_frames_r[self.jump_frame_index])

    def punch(self):
        if not self.punching and not self.moving:
            self.punching = True
            self.current_frame = 0  # Reset frame to start punch animation
    def special_move(self):
        if not self.special and not self.moving:
            self.special = True
            new_projectile = Projectile(self.rect.centerx, self.rect.centery, self.facing_left)
            projectiles.append(new_projectile)
            print("Projectile created:", new_projectile)  # Debug print

    

    def block(self):
        self.blocking = True
        self.current_frame = 0  # Reset frame to start block animation

    def duck(self):
        self.ducking = True
        self.current_frame = 0  # Reset frame to start block animation

    def move(self, dx=0):
        if not self.blocking and not self.ducking:
            self.x += dx
            self.rect.x = self.x
            self.moving = True
            self.facing_left = dx < 0

    def update(self):
        self.update_hitbox()
        if self.hit_reacting:
            self.update_hit_reaction()
        else:
            if not self.moving and not self.punching and not self.blocking and not self.ducking and not self.special and not self.hit_reacting:
                # Character is idle
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_l)

    def draw(self):
        
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        screen.blit(self.image, self.rect.topleft)
    
    def check_punch_collision(self, puncher, receiver):
        
        if puncher.punching and puncher.current_frame in self.punch_frame_at_hit_point:  # punch_frame_at_hit_point needs to be defined based on your animation
            if puncher.hitbox.colliderect(receiver.hitbox):
                receiver.get_hit()
projectiles = []
# Create fighter
fighter = Fighter(100, HEIGHT - 200, idle_frames_r, idle_frames_l, walk_frames_r, walk_frames_l, punch_frames_r, punch_frames_l, block_frames_r, block_frames_l, duck_frames_r, duck_frames_l, special_frames_r, special_frames_l, jump_frames_r, jump_frames_l, hit_reaction_frames_r, hit_reaction_frames_l)
fighter2 = Fighter(100, HEIGHT - 200, idle_frames_r, idle_frames_l, walk_frames_r, walk_frames_l, punch_frames_r, punch_frames_l, block_frames_r, block_frames_l, duck_frames_r, duck_frames_l, special_frames_r, special_frames_l, jump_frames_r, jump_frames_l, hit_reaction_frames_r, hit_reaction_frames_l)
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()
    fighter.moving = False
    # Movement and animation for fighter
    if keys[pygame.K_LEFT]:
        fighter.move(-speed)
    elif keys[pygame.K_RIGHT]:
        fighter.move(speed)
    else:
        # If no keys are pressed, the character is not moving
        fighter.update()  # Update idle animation
    if keys[pygame.K_s]:
        fighter.special_move()
        
    # Check for punching
    if keys[pygame.K_SPACE]:  # Assuming space bar is used for punching
        fighter.punch()

    # Check for blocking
    if keys[pygame.K_b]:  # Assuming 'b' is used for blocking
        fighter.block()
    else:
        fighter.blocking = False  # Stop blocking when 'b' is released
    if keys[pygame.K_DOWN]:  # Assuming 'b' is used for blocking
        fighter.duck()
    else:
        fighter.ducking = False  # Stop blocking when 'b' is released
    if keys[pygame.K_UP] and not fighter.jumping:
        fighter.start_jump()

# Update the fighter's vertical position
    fighter.update_vertical_movement()
# Drawing the projectiles
    for projectile in projectiles[:]:
        projectile.move()
        if projectile.rect.x < 0 or projectile.rect.x > WIDTH:
            projectiles.remove(projectile)
    # Reset movement status


    # Animate the fighter
   
    if fighter.punching and fighter.current_frame in fighter.punch_frame_at_hit_point:
        fighter.check_punch_collision(fighter, fighter2)

    
    # Update the fighters
    fighter.update()
    fighter2.update()
    # Draw background
    screen.blit(background, (0, 0))

    # Draw fighter
    fighter.draw()
    fighter2.draw()
    for projectile in projectiles:
        projectile.draw(screen)

    fighter.animate()
    fighter2.animate()
    # Update display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
