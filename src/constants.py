import os
import pygame

# Display settings
WIDTH = 1000
HEIGHT = 600
FPS = 60
TITLE = "2026 북중미 월드컵 1대1 축구"

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Gameplay constants
PLAYER_SIZE = (60, 90)
PLAYER_SPEED = 7
PLAYER_JUMP_VELOCITY = -15
PLAYER_GRAVITY = 0.8
BALL_RADIUS = 15
BALL_GRAVITY = 0.5
BALL_BOUNCE_Y = -0.7
BALL_BOUNCE_X = -0.8
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
P1_CONTROLS = [pygame.K_a, pygame.K_d, pygame.K_w]
P2_CONTROLS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP]
