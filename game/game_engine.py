import pygame
import os
from .paddle import Paddle
from .ball import Ball


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (153, 51, 255)
LIGHT_PURPLE = (204, 153, 255)
YELLOW = (255, 255, 102)
RED = (255, 51, 51)
GRAY = (50, 50, 50)

WINNING_SCORE = 5


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 15, 15, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 40)
        self.game_over = False
        self.winner = None

        # Load sounds robustly
        sound_dir = os.path.join(os.path.dirname(__file__), 'sounds')
        try:
            self.paddle_sound = pygame.mixer.Sound(os.path.join(sound_dir, "paddle_hit.wav"))
            self.wall_sound = pygame.mixer.Sound(os.path.join(sound_dir, "wall_bounce.wav"))
            self.score_sound = pygame.mixer.Sound(os.path.join(sound_dir, "score_point.wav"))
        except Exception as e:
            print("Sound file missing or could not be loaded: ", e)
            self.paddle_sound = None
            self.wall_sound = None
            self.score_sound = None

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.game_over:
            if keys[pygame.K_w]:
                self.player.move(-15, self.height)
            if keys[pygame.K_s]:
                self.player.move(15, self.height)

    def update(self):
        if not self.game_over:
            old_velocity_x = self.ball.velocity_x
            old_velocity_y = self.ball.velocity_y

            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            # Play sounds
            if (old_velocity_x != self.ball.velocity_x) and self.paddle_sound:
                self.paddle_sound.play()
            if (old_velocity_y != self.ball.velocity_y) and self.wall_sound:
                self.wall_sound.play()

            scored = False
            if self.ball.x <= 0:
                self.ai_score += 1
                scored = True
                self.ball.reset()
            elif self.ball.x + self.ball.width >= self.width:
                self.player_score += 1
                scored = True
                self.ball.reset()

            if scored and self.score_sound:
                self.score_sound.play()

            if self.player_score >= WINNING_SCORE:
                self.game_over = True
                self.winner = "Player"
            elif self.ai_score >= WINNING_SCORE:
                self.game_over = True
                self.winner = "AI"

            self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Background
        screen.fill(PURPLE)

        # Center dashed line
        dash_height = 15
        gap = 10
        y = 0
        while y < self.height:
            pygame.draw.rect(screen, LIGHT_PURPLE, (self.width // 2 - self.paddle_width // 2, y, self.paddle_width, dash_height))
            y += dash_height + gap

        # Draw paddles with shadow
        shadow_offset = 4
        pygame.draw.rect(screen, GRAY, (self.player.x + shadow_offset, self.player.y + shadow_offset, self.player.width, self.player.height))
        pygame.draw.rect(screen, GRAY, (self.ai.x + shadow_offset, self.ai.y + shadow_offset, self.ai.width, self.ai.height))
        pygame.draw.rect(screen, YELLOW, self.player.rect())
        pygame.draw.rect(screen, YELLOW, self.ai.rect())

        # Draw ball with glow effect
        glow_color = (255, 255, 150)
        glow_radius = self.ball.width + 8
        glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*glow_color, 128), (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (self.ball.x - glow_radius + self.ball.width//2, self.ball.y - glow_radius + self.ball.height//2))
        pygame.draw.ellipse(screen, RED, self.ball.rect())

        # Draw scores with shadow
        shadow_text_offset = 2
        player_score_shadow = self.font.render(str(self.player_score), True, GRAY)
        ai_score_shadow = self.font.render(str(self.ai_score), True, GRAY)
        screen.blit(player_score_shadow, (self.width // 4 + shadow_text_offset, 20 + shadow_text_offset))
        screen.blit(ai_score_shadow, (self.width * 3 // 4 + shadow_text_offset, 20 + shadow_text_offset))
        player_score_text = self.font.render(str(self.player_score), True, WHITE)
        ai_score_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_score_text, (self.width // 4, 20))
        screen.blit(ai_score_text, (self.width * 3 // 4, 20))

        # Draw game over screen with overlay
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # semi-transparent black
            screen.blit(overlay, (0, 0))
            text = self.font.render(f"{self.winner} Wins!", True, YELLOW)
            rect = text.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text, rect)
