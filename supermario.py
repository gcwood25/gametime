import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 1000
GROUND = HEIGHT - 50
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create the game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Mario Game")

# Initialize font
score = 0
font = pygame.font.Font(None, 36)


# Load images (Assuming images are already resized to fit the screen)
player_img = pygame.image.load("mario.png")
player_img = pygame.transform.scale(player_img, (65, 80))
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
goomba_img = pygame.image.load("goombas.png")
goomba_img = pygame.transform.scale(goomba_img, (50, 50))
coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (30, 30))  # Adjust size as needed
title_img = pygame.image.load("supermario.png")  # Replace "super_mario_title.png" with your image file
title_img = pygame.transform.scale(title_img, (400, 200))  # Resize the image to fit the screen
brick_img = pygame.image.load("brick.png")

# Player attributes
player_rect = player_img.get_rect()
player_rect.bottom = GROUND
player_rect.left = WIDTH // 2
player_speed = 7
player_jump = -15
player_gravity = 0.9
player_y_speed = 0
is_jumping = False

# Level (Assuming platforms are adjusted for the new screen size and more spaced out)
platforms = [
    pygame.Rect(0, GROUND, WIDTH, 50),
    pygame.Rect(100, HEIGHT - 200, 250, 20),   # More spaced out platform
    pygame.Rect(500, HEIGHT - 350, 200, 20),
    pygame.Rect(50, HEIGHT - 500, 200, 20),   # More spaced out platform
    pygame.Rect(350, HEIGHT - 550, 180, 20),
    pygame.Rect(700, HEIGHT - 550, 220, 20),  # More spaced out platform
    pygame.Rect(200, HEIGHT - 700, 150, 20),  # More spaced out platform
    pygame.Rect(300, HEIGHT - 350, 100, 20),
    pygame.Rect(700, HEIGHT - 500, 120, 20),
    pygame.Rect(400, HEIGHT - 600, 180, 20),
]

# Coin positions (on the ground and platforms)
coin_positions = [
    (100, GROUND - 30),
    (150, GROUND - 30),
    (500, GROUND - 30),
    (50, HEIGHT - 500 - 30),
    (370, HEIGHT - 550 - 30),
    (700, HEIGHT - 550 - 30),
    (210, HEIGHT - 700 - 30),
    (350, HEIGHT - 350 - 30),
    (750, HEIGHT - 500 - 30),
    (450, HEIGHT - 600 - 30),
]

# Goombas (Enemies)
goombas = [
    {"rect": pygame.Rect(400, GROUND - 50, 60, 60), "speed": 1, "direction": "right", "timer": 0},
    {"rect": pygame.Rect(700, GROUND - 50, 60, 60), "speed": 1, "direction": "right", "timer": 0},
    {"rect": pygame.Rect(150, HEIGHT - 500 - 50, 60, 60), "speed": 1, "direction": "right", "timer": 0},  # Goomba on platform 3
    {"rect": pygame.Rect(700, HEIGHT - 550 - 50, 60, 60), "speed": 1, "direction": "right", "timer": 0},  # Goomba on platform 5
    {"rect": pygame.Rect(400, HEIGHT - 600 - 50, 60, 60), "speed": 1, "direction": "right", "timer": 0},  # Goomba on platform 10
]

# Initialize coin timers
coin_timer = [0] * len(coin_positions)
start_time = pygame.time.get_ticks()
# Game loop
clock = pygame.time.Clock()
running = True
timer_reset = False
score = 0

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for platform in platforms:
        win.blit(brick_img, platform)
    # Player movement
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    # Player jumping
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            player_y_speed = player_jump
    else:
        player_y_speed += player_gravity
        player_rect.y += player_y_speed
        if player_rect.bottom >= GROUND:
            player_rect.bottom = GROUND
            is_jumping = False

    # Collision detection with platforms
    for platform in platforms:
        if player_rect.colliderect(platform) and player_y_speed > 0:
            player_rect.bottom = platform.top
            player_y_speed = 0
            is_jumping = False

    for pos, timer in zip(coin_positions, coin_timer):
        if player_rect.colliderect(pygame.Rect(pos, (30, 30))):  # Check collision with coins
            score += 50  # Add 50 points for each collected coin
            coin_timer[coin_positions.index(pos)] = 7 * FPS  # Set timer for coin respawn after 7 seconds
            coin_positions.remove(pos)

    # Move Goombas and collision detection
    for goomba in goombas:
        if goomba["direction"] == "right":
            goomba["rect"].x += goomba["speed"]
        else:
            goomba["rect"].x -= goomba["speed"]

        goomba["timer"] += 1
        if goomba["timer"] == FPS * 3.5:  # Change direction after 3.5 seconds
            goomba["timer"] = 0
            if goomba["direction"] == "right":
                goomba["direction"] = "left"
            else:
                goomba["direction"] = "right"

        if player_rect.colliderect(goomba["rect"]):
            # Reset timer if player collides with goomba
            start_time = pygame.time.get_ticks()
            timer_reset = True
            for goomba in goombas:
                if player_rect.colliderect(goomba["rect"]):
                    score -= 20  # Deduct 20 points for colliding with a goomba
                    start_time = pygame.time.get_ticks()  # Reset timer if player collides with goomba
                    timer_reset = True
        # Draw everything
        win.blit(background_img, (0, 0))
        pygame.draw.rect(win, BLUE, (0, GROUND, WIDTH, HEIGHT - GROUND))
        for platform in platforms:
            pygame.draw.rect(win,BLUE,platform)
        for goomba in goombas:
            win.blit(goomba_img, goomba["rect"])
        for pos in coin_positions:
            win.blit(coin_img, pos)
        win.blit(player_img, player_rect)

        # Timer
        if not timer_reset:
            elapsed_time = pygame.time.get_ticks() - start_time
        else:
            elapsed_time = 0
            timer_reset = False

        win.blit(title_img, (WIDTH // 2 - title_img.get_width() // 2, 10))  # Position the image at the top middle
        timer_text = font.render("Time: " + str(round(elapsed_time / 1000, 2)), True, WHITE)
        win.blit(timer_text, (10, 10))
        score_text = font.render("Score: " + str(score), True, WHITE)
        win.blit(score_text, (WIDTH - 150, 10))  # Display score at top right corner
        pygame.display.flip()
        clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
