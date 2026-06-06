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
SKY_BLUE = (135, 206, 235)
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
STATE_BACKGROUND = "background"
STATE_SELECTION = "selection"
STATE_PLAYING = "playing"
STATE_RESULT = "result"

# Resource paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
BACKGROUND_DIR = os.path.join(ASSETS_DIR, "backgrounds")
FLAG_DIR = os.path.join(ASSETS_DIR, "flags")
PLAYER1_IMAGE_PATH = os.path.join(ASSETS_DIR, "player1.png")
PLAYER2_IMAGE_PATH = os.path.join(ASSETS_DIR, "player2.png")

# Menu teams (name, display name, jersey color)
TEAMS = [
    {
        "id": "korea",
        "name": "대한민국",
        "color": (200, 16, 46),
        "flag_path": os.path.join(FLAG_DIR, "korea.png"),
    },
    {
        "id": "brazil",
        "name": "브라질",
        "color": (255, 223, 0),
        "flag_path": os.path.join(FLAG_DIR, "brazil.png"),
    },
    {
        "id": "france",
        "name": "프랑스",
        "color": (0, 35, 149),
        "flag_path": os.path.join(FLAG_DIR, "france.png"),
    },
    {
        "id": "argentina",
        "name": "아르헨티나",
        "color": (117, 170, 219),
        "flag_path": os.path.join(FLAG_DIR, "argentina.png"),
    },
    {"id": "usa", "name": "미국", "color": (255, 255, 255)},
    {"id": "senegal", "name": "세네갈", "color": (0, 100, 0)},
    {"id": "portugal", "name": "포르투갈", "color": (139, 0, 0)},
    {"id": "england", "name": "잉글랜드", "color": (255, 255, 255)},
]
TOURNAMENT_TEAMS = TEAMS[:4]

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
BALL_AIR_FRICTION = 1.0
BALL_GROUND_FRICTION = 0.995
BALL_MAX_SPEED = 30
GROUND_Y = 550
GOAL_WIDTH = 70
GOAL_HEIGHT = 150
GOAL_Y = 400
GOAL_POST_THICKNESS = 6
SCORE_TEXT_POS = (WIDTH // 2 - 40, 20)
MATCH_WIN_SCORE = 3

STADIUM_BACKGROUNDS = [
    {
        "id": "usa",
        "name": "미국",
        "path": os.path.join(BACKGROUND_DIR, "usa_stadium.png"),
    },
    {
        "id": "canada",
        "name": "캐나다",
        "path": os.path.join(BACKGROUND_DIR, "canada_stadium.png"),
    },
    {
        "id": "mexico",
        "name": "멕시코",
        "path": os.path.join(BACKGROUND_DIR, "mexico_stadium.png"),
    },
]

# Key settings
P1_CONTROLS = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_LSHIFT]
P2_CONTROLS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_RSHIFT]

PLAYER_SPEED = 7
PLAYER_GRAVITY = 0.6
PLAYER_RADIUS = 30
