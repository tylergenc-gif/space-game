import pygame

# Window settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "My Awesome Game"
FPS = 60


# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

new_size = (200, 150)
# Images
SHIP_IMG = "assets/images/playerShip.png"
LASER_IMG = "assets/images/laserBlue.png"
ASTEROID_IMG = "assets/images/enemyRed.png"
BOMBER_IMG = "assets/images/enemyBlack.png"
ENEMY_LASER_IMG = "assets/images/laserRed.png"
EMPTY_HEART_IMG = "assets/images/emptyHeart.png"
FULL_HEART_IMG = "assets/images/fullHeart.png"
STAR_IMG = "assets/images/littleStar.png"
SPREADSHOT_IMG = "assets/images/spreadShot.png"


# Game
NUM_OF_LEVELS = 100
STAR_SPEED = 15
SCROLL_SPEED = 0
NUMBER_OF_STARS = 100

# Ship
SHIP_SPEED = 20
ACCELERATION = 1
FRICTION = 0.94
PLAYER_SHIELD = 5
MAX_PLAYER_SHIELD = PLAYER_SHIELD

# Lasers
LASER_SPEED = 30

# Enemy
ENEMY_SHIELD = 1
ASTEROID_SPEED = 30
MIN_SIZE = 100
MAX_SIZE = 300
RATE_OF_ASTEROIDS = 900
NUM_OF_ENEMIES = 1

# Enemy Lasers
ENEMY_SHOT_RATE = 1

# Controls
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
SHOOT = pygame.K_SPACE
UP = pygame.K_UP

# Power Ups
POWERUP_SPEED = 5
