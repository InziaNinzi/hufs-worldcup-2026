import pygame

from src.constants import (
    BALL_BOUNCE_X,
    BALL_BOUNCE_Y,
    BALL_GRAVITY,
    BALL_RADIUS,
    GROUND_Y,
    HEIGHT,
    WIDTH,
    YELLOW,
)


class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.reset()

    def reset(self):
        self.pos = [WIDTH // 2, HEIGHT // 2]
        self.vel = [0, 0]

    def update(self):
        self.vel[1] += BALL_GRAVITY
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        ground_contact_y = GROUND_Y - self.radius
        if self.pos[1] > ground_contact_y:
            self.pos[1] = ground_contact_y
            self.vel[1] *= BALL_BOUNCE_Y

        if self.pos[0] < self.radius or self.pos[0] > WIDTH - self.radius:
            self.vel[0] *= BALL_BOUNCE_X
            self.pos[0] = max(self.radius, min(WIDTH - self.radius, self.pos[0]))

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.pos[0]), int(self.pos[1])), self.radius)
