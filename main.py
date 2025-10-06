import pygame
from game.game_engine import GameEngine

# Initialize pygame and its mixer for sound
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Classic arcade-style colors
BACKGROUND_COLOR = (0, 0, 30)      # Dark navy blue for the background
PADDLE_COLOR = (255, 255, 0)       # Bright yellow paddles
BALL_COLOR = (255, 0, 0)           # Bright red ball
TEXT_COLOR = (255, 255, 255)       # White text
PAUSE_BUTTON_COLOR = (0, 200, 255) # Cyan pause button
PAUSE_BUTTON_HOVER = (0, 255, 255) # Lighter cyan on hover

# Clock
clock = pygame.time.Clock()
FPS = 60

# Try loading sounds safely
try:
    # Game engine instantiation will load sounds
    engine = GameEngine(WIDTH, HEIGHT)
except pygame.error as e:
    print(f"Error initializing sound system: {e}")
    engine = GameEngine(WIDTH, HEIGHT)
    # Disable sound playback if needed by modifying engine flags or methods

# Button properties
button_font = pygame.font.SysFont("Arial", 20)
pause_button_rect = pygame.Rect(WIDTH - 110, 10, 100, 40)  # top-right corner

def draw_pause_button(paused):
    """Draws the pause/resume button."""
    color = PAUSE_BUTTON_HOVER if paused else PAUSE_BUTTON_COLOR
    pygame.draw.rect(SCREEN, color, pause_button_rect, border_radius=8)
    text = "Resume" if paused else "Pause"
    text_surf = button_font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=pause_button_rect.center)
    SCREEN.blit(text_surf, text_rect)

def main():
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Keyboard quit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False

            # Click detection for pause button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    paused = not paused

            # Restart logic
            if engine.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    engine.player_score = 0
                    engine.ai_score = 0
                    engine.game_over = False
                    engine.winner = None
                    engine.ball.reset()
                elif event.key == pygame.K_q:
                    running = False

        # Update only if not paused
        if not paused:
            engine.handle_input()
            engine.update()

        # Render background and game elements
        SCREEN.fill(BACKGROUND_COLOR)
        engine.render(SCREEN)

        # Draw pause button
        draw_pause_button(paused)

        # Pause overlay
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)  # semi-transparent dark overlay
            overlay.fill((0, 0, 0))
            SCREEN.blit(overlay, (0, 0))
            font = pygame.font.SysFont("Arial", 40)
            pause_text = font.render("GAME PAUSED", True, TEXT_COLOR)
            rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            SCREEN.blit(pause_text, rect)
            draw_pause_button(paused)

        # Game-over instructions
        if engine.game_over:
            font = pygame.font.SysFont("Arial", 20)
            instruction_text = font.render("Press R to Restart or Q to Quit", True, TEXT_COLOR)
            rect = instruction_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            SCREEN.blit(instruction_text, rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
