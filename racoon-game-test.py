import os
import pygame

# Change the current working directory to the directory where your game files are located
#os.chdir("/home/gabriel-waters/Documents")

# Initialize Pygame
pygame.init()

# Load the background image
background_image = pygame.image.load("Background photo2.png")

# Get the size of the background image
background_width, background_height = background_image.get_size()

# Set up the game window to match the background image width and shrink the height by 100 pixels
screen_height = background_height - 100  # Shrink the window from the bottom up by 100 pixels
screen = pygame.display.set_mode((background_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Raccoon Game")

# Load the character image
character_image = pygame.image.load("raccoon.png")

# Resize the character image to make it bigger
character_image = pygame.transform.scale(character_image, (75, 75))  # Resize to 75x75 pixels

# Load the spaceship image
spaceship_image = pygame.image.load("spaceship.png")

# Scale the spaceship image up by 20 pixels in width and shrink the height by 15 pixels
spaceship_image = pygame.transform.scale(spaceship_image, (190, 100))  # Resize to 190x100 pixels

# Set the initial position of the character
initial_character_x = 50
initial_character_y = screen_height - 100  # Start above the ground line
initial_character_y_velocity = 0
gravity = 0.8  # Change gravity to 0.8
jump_strength = -15  # Change jump strength to -15

# Set the initial position of the spaceship
spaceship_x = background_width
spaceship_y = screen_height - 300  # Set the spaceship's y position

# Set the speed of the spaceship
spaceship_speed = 5

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()
fps = 30  # Set the frame rate to 30 FPS

# Set up the ground
ground_y = screen_height - 50

# Function to display the "Game Over" message
def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (background_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()

# Function to reset the game state
def reset_game():
    global character_x, character_y, character_y_velocity, gravity_enabled, flipped, game_over, touching_spaceship, hit_spaceship, spaceship_x
    character_x = initial_character_x
    character_y = initial_character_y
    character_y_velocity = initial_character_y_velocity
    gravity_enabled = True
    flipped = False
    game_over = False
    touching_spaceship = False
    hit_spaceship = False
    spaceship_x = background_width
    # Reset the character image to its original orientation
    global character_image
    character_image = pygame.image.load("raccoon.png")
    character_image = pygame.transform.scale(character_image, (75, 75))  # Resize to 75x75 pixels

# Initialize the game state
reset_game()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                if touching_spaceship:
                    touching_spaceship = False  # Allow the character to drop back down to the ground
                    character_y_velocity = 5  # Reset the velocity
                    character_y += 20  # Move the character further down to avoid immediate collision
                    if flipped:
                        character_image = pygame.transform.flip(character_image, False, True)  # Flip the character back to original orientation
                        flipped = False
                        print("Character flipped back to original orientation")
                    print("Character drops back down")
                elif gravity_enabled:
                    character_y_velocity = jump_strength  # Allow jump only if gravity is enabled
                    print("Character jumps with velocity:", character_y_velocity)
            if event.key == pygame.K_DOWN:
                if touching_spaceship:
                    touching_spaceship = False  # Allow the character to drop back down to the ground
                    character_y_velocity = 5  # Reset the velocity
                    character_y += 20  # Move the character further down to avoid immediate collision
                    if flipped:
                        character_image = pygame.transform.flip(character_image, False, True)  # Flip the character back to original orientation
                        flipped = False
                        print("Character flipped back to original orientation")
                    print("Character drops back down")
            if event.key == pygame.K_z:
                reset_game()
                print("Game reset")

    if not game_over:
        # Apply gravity
        if gravity_enabled:
            character_y_velocity += gravity
            character_y += character_y_velocity
            print("Applying gravity. Velocity:", character_y_velocity, "Position:", character_y)

            # Prevent the character from falling below the ground
            if character_y > ground_y - 75:
                character_y = ground_y - 75
                character_y_velocity = 0
                print("Character hit the ground")

        # Move the spaceship
        spaceship_x -= spaceship_speed

        # Reset the spaceship's position when it moves off the screen
        if spaceship_x < -190:
            spaceship_x = background_width

        # Create rectangles for collision points
        character_rect = pygame.Rect(character_x, character_y, 75, 75)
        spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, 190, 100)

        # Draw the collision boxes
        pygame.draw.rect(screen, (0, 255, 0), character_rect)  # Draw filled character collision box in green
        pygame.draw.rect(screen, (0, 255, 0), spaceship_rect)  # Draw filled spaceship collision box in green

    # Draw the background image on the screen
    screen.blit(background_image, (0, 0))

    # Draw the spaceship image on the screen
    screen.blit(spaceship_image, (spaceship_x, spaceship_y))  # Move the spaceship slightly above the line

    # Draw the character image on the screen
    screen.blit(character_image, (character_x, character_y))

    # Check for collision with the spaceship
    if character_rect.colliderect(spaceship_rect):
        character_y = spaceship_rect.bottom - 55  # Ensure the bottom of the character is lower at the bottom of the spaceship
        character_y_velocity = 0
        if not hit_spaceship:
            hit_spaceship = True
            print("Character hit the spaceship")
        touching_spaceship = True
        print("Character is touching the spaceship")
        if not flipped:
            character_image = pygame.transform.flip(character_image, False, True)  # Flip the character upside down
            flipped = True
            print("Character flipped upside down")
    else:
        if touching_spaceship:
            touching_spaceship = False
            hit_spaceship = False
            print("Character is no longer touching the spaceship")
            if flipped:
                character_image = pygame.transform.flip(character_image, False, True)  # Flip the character back to original orientation
                flipped = False
                print("Character flipped back to original orientation")

    if game_over:
        display_game_over()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()