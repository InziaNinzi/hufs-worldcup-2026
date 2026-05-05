import os
import pygame

from src.constants import (
    GROUND_Y,
    HEIGHT,
    PLAYER_GRAVITY,
    PLAYER_JUMP_VELOCITY,
    PLAYER_SIZE,
    PLAYER_SPEED,
    WIDTH,
)


class Player:
    def __init__(self, x, y, controls, color, image_path=None):
        self.image = self._load_or_fallback_image(image_path, color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.controls = controls
        self.vel_y = 0
        self.is_jumping = False
        self.speed = PLAYER_SPEED
        self.gravity = PLAYER_GRAVITY

    def _load_or_fallback_image(self, image_path, color):
        if image_path and isinstance(image_path, (str, os.PathLike)) and os.path.exists(image_path):
            try:
                image = pygame.image.load(image_path).convert_alpha()
                return pygame.transform.scale(image, PLAYER_SIZE)
            except pygame.error:
                pass

        fallback = pygame.Surface(PLAYER_SIZE, pygame.SRCALPHA)
        fallback.fill(color)
        return fallback

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[self.controls[0]]:
            self.rect.x -= self.speed
        if keys[self.controls[1]]:
            self.rect.x += self.speed

        if keys[self.controls[2]] and not self.is_jumping:
            self.vel_y = PLAYER_JUMP_VELOCITY
            self.is_jumping = True

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom > GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False
            self.vel_y = 0

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)
