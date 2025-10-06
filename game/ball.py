import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        # Move the ball with incremental steps to avoid skipping collisions
        steps = max(abs(self.velocity_x), abs(self.velocity_y))
        step_x = self.velocity_x / steps
        step_y = self.velocity_y / steps

        for _ in range(int(steps)):
            self.x += step_x
            self.y += step_y

            # Check collision with top and bottom walls
            if self.y <= 0 or self.y + self.height >= self.screen_height:
                self.velocity_y *= -1
                self.y = max(0, min(self.y, self.screen_height - self.height))

    def check_collision(self, player, ai):
        # Check collision with player paddle
        if self.rect().colliderect(player.rect()):
            if self.velocity_x < 0:  # Ball moving left toward player paddle
                self.velocity_x *= -1
                self.x = player.x + player.width  # Keep ball outside paddle after collision

        # Check collision with AI paddle
        elif self.rect().colliderect(ai.rect()):
            if self.velocity_x > 0:  # Ball moving right toward AI paddle
                self.velocity_x *= -1
                self.x = ai.x - self.width  # Keep ball outside paddle after collision

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
