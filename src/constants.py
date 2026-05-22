import os
import pygame

# Display settings
WIDTH = 1000
HEIGHT = 600
FPS = 60
TITLE = "2026 북중미 월드컵 1대1 축구"

# Colors
GREEN = (34, 139, 34)
DARK_GREEN = (20, 80, 40)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GRAY = (180, 180, 180)
LIGHT_GRAY = (220, 220, 220)

# Game states
STATE_TITLE = "title"
STATE_SELECTION = "selection"
STATE_PLAYING = "playing"

# Menu teams (name, display name, jersey color)
TEAMS = [
    {"id": "korea", "name": "대한민국", "color": (200, 16, 46)},
    {"id": "brazil", "name": "브라질", "color": (255, 223, 0)},
    {"id": "france", "name": "프랑스", "color": (0, 35, 149)},
    {"id": "argentina", "name": "아르헨티나", "color": (117, 170, 219)},
    {"id": "germany", "name": "독일", "color": (255, 255, 255)},
    {"id": "japan", "name": "일본", "color": (188, 0, 45)},
    {"id": "spain", "name": "스페인", "color": (200, 16, 46)},
    {"id": "england", "name": "잉글랜드", "color": (255, 255, 255)},
]

# Gameplay constants
PLAYER_SIZE = (60, 90)
PLAYER_RADIUS = 30
PLAYER_SPEED = 7
PLAYER_DASH_SPEED = 18
PLAYER_DASH_DURATION = 10
PLAYER_DASH_COOLDOWN = 90
PLAYER_JUMP_VELOCITY = -15
PLAYER_GRAVITY = 0.8
BALL_RADIUS = 15
BALL_GRAVITY = 0.5
BALL_BOUNCE_Y = -0.7
BALL_BOUNCE_X = -0.8
BALL_AIR_FRICTION = 0.99
BALL_GROUND_FRICTION = 0.88
BALL_MAX_SPEED = 30
GROUND_Y = 550
GOAL_WIDTH = 50
GOAL_HEIGHT = 150
GOAL_Y = 400
SCORE_TEXT_POS = (WIDTH // 2 - 40, 20)

# Resource paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
PLAYER1_IMAGE_PATH = os.path.join(ASSETS_DIR, "player1.png")
PLAYER2_IMAGE_PATH = os.path.join(ASSETS_DIR, "player2.png")

# Key settings
P1_CONTROLS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_LSHIFT]
P2_CONTROLS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT]
