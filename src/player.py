import os
import pygame

from src.constants import (
    CHARACTER_STATS, 
    GROUND_Y,
    HEIGHT,
    PLAYER_DASH_DURATION,
    PLAYER_GRAVITY,
    PLAYER_RADIUS,
    PLAYER_SIZE,
    WIDTH,
)


class Player:
    def __init__(self, x, y, controls, color, image_path=None, char_type="korea"):
        self.controls = controls
        self.color = color
        self.radius = PLAYER_RADIUS

        self.char_type = char_type
        
        
        stats = CHARACTER_STATS.get(char_type, CHARACTER_STATS["korea"])
        
        
        self.speed = stats["speed"]
        self.power = stats["power"]
        self.jump_velocity = stats["jump_velocity"]
        self.dash_cooldown_max = stats["dash_cooldown"]
        self.dash_speed = stats["dash_speed"]

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
            self.rect.x += self.dash_speed * self.last_dir  # 국가별 고유 대시 속도 적용
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.dash_cooldown_timer = self.dash_cooldown_max  # 국가별 고유 대시 쿨타임 적용
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