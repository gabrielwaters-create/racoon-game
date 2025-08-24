# Racoon attaches to line but does not flip when drops back down
# Import the Pygame library
import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 400))

# Set the title of the window
pygame.display.set_caption("Raccoon Game")

# Load the character image
character_image = pygame.image.load("raccoon.png")

# Resize the character image
character_image = pygame.transform.scale(character_image, (50, 50))  # Resize to 50x50 pixels

# Set the initial position of the character
initial_character_x = 50
initial_character_y = 300
initial_character_y_velocity = 0
gravity = 0.5  # Gravity
jump_strength = -10  # Jump strength

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()
fps = 30  # Set the frame rate to 30 FPS

# Set up the lines
line_y = 150
line_thickness = 5
ground_y = 300

# Function to display the "Game Over" message
def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (250, 150))
    pygame.display.flip()

# Function to reset the game state
def reset_game():
    global character_x, character_y, character_y_velocity, gravity_enabled, flipped, game_over, touching_line
    character_x = initial_character_x
    character_y = initial_character_y
    character_y_velocity = initial_character_y_velocity
    gravity_enabled = True
    flipped = False
    game_over = False
    touching_line = False
    # Reset the character image to its original orientation
    global character_image
    character_image = pygame.image.load("raccoon.png")
    character_image = pygame.transform.scale(character_image, (50, 50))  # Resize to 50x50 pixels

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
                if touching_line:
                    touching_line = False  # Allow the character to drop back down to the ground
                    character_y_velocity = 5  # Reset the velocity
                    print("Character drops back down")
                elif gravity_enabled:
                    character_y_velocity = jump_strength  # Allow jump only if gravity is enabled
                    print("Character jumps with velocity:", character_y_velocity)
            if event.key == pygame.K_DOWN:
                if touching_line:
                    touching_line = False  # Allow the character to drop back down to the ground
                    character_y_velocity = 5  # Reset the velocity
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
            if character_y > ground_y:
                character_y = ground_y
                character_y_velocity = 0
                print("Character hit the ground")

        # Create rectangles for collision points
        character_rect = pygame.Rect(character_x, character_y, 50, 50)
        top_right_rect = pygame.Rect(character_x + 50, character_y, 1, 1)
        bottom_right_rect = pygame.Rect(character_x + 50, character_y + 50, 1, 1)
        bottom_left_rect = pygame.Rect(character_x, character_y + 50, 1, 1)

        # Check for collision with the line
        if (character_rect.colliderect(pygame.Rect(0, line_y, 800, line_thickness)) or
            top_right_rect.colliderect(pygame.Rect(0, line_y, 800, line_thickness)) or
            bottom_right_rect.colliderect(pygame.Rect(0, line_y, 800, line_thickness)) or
            bottom_left_rect.colliderect(pygame.Rect(0, line_y, 800, line_thickness))):
            character_y = line_y  # Ensure the top of the character is exactly at the top of the line
            character_y_velocity = 0
            if not touching_line:
                touching_line = True
                print("Character is touching the line")
            if not flipped:
                character_image = pygame.transform.flip(character_image, False, True)  # Flip the character upside down
                flipped = True
                print("Character flipped upside down")
            print("Character hit the line")
        else:
            if touching_line:
                touching_line = False
                if flipped:
                    character_image = pygame.transform.flip(character_image, False, True)  # Flip the character back to original orientation
                    flipped = False
                    print("Character flipped back to original orientation")

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Draw the character image on the screen
    screen.blit(character_image, (character_x, character_y))

    # Draw the line on the screen
    pygame.draw.line(screen, (0, 0, 0), (0, line_y), (800, line_y), line_thickness)

    # Draw the ground line on the screen
    pygame.draw.line(screen, (0, 0, 0), (0, ground_y + 50), (800, ground_y + 50), line_thickness)

    if game_over:
        display_game_over()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(fps)

# Quit Pygame
pygame.quit()