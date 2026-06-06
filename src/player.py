import os

import pygame

from src.constants import (
    GROUND_Y,
    HEIGHT,
    PLAYER_DASH_COOLDOWN,
    PLAYER_DASH_DURATION,
    PLAYER_DASH_SPEED,
    PLAYER_GRAVITY,
    PLAYER_JUMP_VELOCITY,
    PLAYER_RADIUS,
    PLAYER_SIZE,
    PLAYER_SPEED,
    WIDTH,
)


class Player:
    def __init__(self, x, y, controls, color, image_path=None, char_type="NORMAL"):
        self.controls = controls
        self.color = color
        self.radius = PLAYER_RADIUS

        self.char_type = char_type
        if char_type == "SPEEDY":
            self.speed = 10
            self.power = 1.2
            self.jump_velocity = -14
        elif char_type == "HEAVY":
            self.speed = 5
            self.power = 2.0
            self.jump_velocity = -11
        else:
            self.speed = 7
            self.power = 1.5
            self.jump_velocity = -13

        self.image = self._load_or_fallback_image(image_path, color)
        self.rect = pygame.Rect(x, y, *PLAYER_SIZE)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = PLAYER_GRAVITY
        self.is_jumping = False

        self.last_dir = 1
        self.is_dashing = False
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self._dash_key_prev = False

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
        prev_x = self.rect.x

        if keys[self.controls[0]]:
            self.last_dir = -1
        elif keys[self.controls[1]]:
            self.last_dir = 1

        dash_key_now = keys[self.controls[3]]
        if dash_key_now and not self._dash_key_prev and not self.is_dashing and self.dash_cooldown_timer <= 0:
            self.is_dashing = True
            self.dash_timer = PLAYER_DASH_DURATION
        self._dash_key_prev = dash_key_now

        if self.is_dashing:
            self.rect.x += PLAYER_DASH_SPEED * self.last_dir
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown_timer = PLAYER_DASH_COOLDOWN
        else:
            if keys[self.controls[0]]:
                self.rect.x -= self.speed
            if keys[self.controls[1]]:
                self.rect.x += self.speed

        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1

        if keys[self.controls[2]] and not self.is_jumping:
            self.vel_y = self.jump_velocity
            self.is_jumping = True

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.is_jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.vel_x = self.rect.x - prev_x

    @property
    def circle_x(self):
        return self.rect.centerx

    @property
    def circle_y(self):
        return self.rect.centery

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.circle(surface, self.color, (self.circle_x, self.circle_y), self.radius)
