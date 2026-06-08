import os
import random
import pygame

from src.constants import (
    FPS,
    GOLD,
    GRAY,
    GROUND_Y,
    HEIGHT,
    WHITE,
    WIDTH,
)

_MINI_W, _MINI_H = 40, 60
_BALL_R = 15
_GRAVITY = 0.55
_CONFETTI_COLORS = [
    (255, 70, 70), (70, 170, 255), (255, 215, 0),
    (90, 230, 90), (255, 140, 40), (210, 70, 210),
]


class _Mini:
    def __init__(self, x, image):
        self.x = float(x)
        self.y = float(GROUND_Y - _MINI_H)
        self.vel_y = -random.uniform(8, 15)
        self.img = image
        self.flipped = random.choice([True, False])
        self._timer = random.randint(0, 55)

    def update(self):
        self._timer -= 1
        ground = GROUND_Y - _MINI_H
        if self._timer <= 0 and self.y >= ground - 1:
            self.vel_y = -random.uniform(10, 17)
            self._timer = random.randint(20, 65)
        self.vel_y += _GRAVITY
        self.y += self.vel_y
        if self.y > ground:
            self.y = ground
            self.vel_y = 0

    def draw(self, surface):
        img = pygame.transform.flip(self.img, True, False) if self.flipped else self.img
        surface.blit(img, (int(self.x - _MINI_W // 2), int(self.y)))


class _Ball:
    def __init__(self, image):
        self.img = image
        self.x = float(WIDTH // 2)
        self.y = float(GROUND_Y - _BALL_R * 3)
        self.vx = random.choice([-1, 1]) * random.uniform(4, 6)
        self.vy = -9.0

    def update(self):
        self.vy += 0.38
        self.x += self.vx
        self.y += self.vy
        if self.x < _BALL_R:
            self.x = _BALL_R
            self.vx = abs(self.vx) * 0.85
        if self.x > WIDTH - _BALL_R:
            self.x = WIDTH - _BALL_R
            self.vx = -abs(self.vx) * 0.85
        ground = GROUND_Y - _BALL_R
        if self.y > ground:
            self.y = ground
            self.vy *= -0.65
            self.vx *= 0.98

    def draw(self, surface):
        ix, iy = int(self.x), int(self.y)
        if self.img:
            surface.blit(self.img, (ix - _BALL_R, iy - _BALL_R))
        else:
            pygame.draw.circle(surface, (255, 220, 0), (ix, iy), _BALL_R)


class _Confetti:
    def __init__(self, spread=False):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(-HEIGHT, 0) if spread else -random.uniform(10, 80)
        self._randomize()

    def _randomize(self):
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(2.5, 5.5)
        self.color = random.choice(_CONFETTI_COLORS)
        self.w = random.randint(6, 13)
        self.h = random.randint(3, 7)
        self.angle = random.uniform(0, 360)
        self.spin = random.uniform(-5, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.spin
        if self.y > HEIGHT + 20:
            self.x = random.uniform(0, WIDTH)
            self.y = -random.uniform(10, 80)
            self._randomize()

    def draw(self, surface):
        surf = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        surf.fill((*self.color, 210))
        rotated = pygame.transform.rotate(surf, self.angle)
        surface.blit(rotated, (int(self.x), int(self.y)))


def _load_mini_image(char_type, color):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(root, "assets", "sprites", char_type, "idle.png")
    if os.path.exists(img_path):
        try:
            sheet = pygame.image.load(img_path).convert_alpha()
            w = sheet.get_width() // 4
            frame = sheet.subsurface(pygame.Rect(0, 0, w, sheet.get_height()))
            return pygame.transform.scale(frame, (_MINI_W, _MINI_H))
        except pygame.error:
            pass
    fallback = pygame.Surface((_MINI_W, _MINI_H), pygame.SRCALPHA)
    fallback.fill(color)
    return fallback


def _load_ball_image():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(root, "assets", "ball.png")
    if os.path.exists(img_path):
        try:
            img = pygame.image.load(img_path).convert_alpha()
            d = _BALL_R * 2
            return pygame.transform.scale(img, (d, d))
        except pygame.error:
            pass
    return None


def run_victory_screen(screen, clock, winner_team):
    title_font = pygame.font.SysFont("malgungothic", 54, bold=True)
    team_font = pygame.font.SysFont("malgungothic", 32, bold=True)
    hint_font = pygame.font.SysFont("malgungothic", 20)

    mini_img = _load_mini_image(winner_team["id"], winner_team["color"])
    xs = [int(WIDTH * (i + 1) / 12) for i in range(11)]
    players = [_Mini(x, mini_img) for x in xs]

    ball = _Ball(_load_ball_image())
    confetti = [_Confetti(spread=True) for _ in range(90)]

    tick = 0

    while True:
        clock.tick(FPS)
        tick += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    return "done"

        screen.fill((8, 28, 8))
        pygame.draw.rect(screen, (22, 90, 40), (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
        pygame.draw.line(screen, WHITE, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

        for c in confetti:
            c.update()
            c.draw(screen)

        ball.update()
        ball.draw(screen)

        for p in players:
            p.update()
            p.draw(screen)

        pulse = abs((tick % 60) - 30) / 30
        title_color = (255, int(200 + 55 * pulse), 0)
        title_surf = title_font.render("CHAMPION!", True, title_color)
        screen.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, 108)))

        team_surf = team_font.render(winner_team["name"], True, WHITE)
        screen.blit(team_surf, team_surf.get_rect(center=(WIDTH // 2, 178)))

        hint = hint_font.render("ENTER / SPACE 계속", True, GRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 18)))

        pygame.display.flip()
