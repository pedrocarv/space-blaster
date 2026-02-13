"""Constants and configuration for Space Blaster."""

import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(_BASE_DIR, 'assets', 'PressStart2P-Regular.ttf')

# ---------- Display ----------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = 'Space Blaster'

# ---------- Player ----------
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
PLAYER_LIVES = 3
INVINCIBLE_DURATION = 90  # frames (~1.5 s at 60 fps)

# ---------- Bullets ----------
BULLET_WIDTH = 6
BULLET_HEIGHT = 18
BULLET_SPEED = 9

ENEMY_BULLET_WIDTH = 5
ENEMY_BULLET_HEIGHT = 14
ENEMY_BULLET_SPEED = 5

# ---------- Enemies ----------
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 60
ENEMY_SPEED_DEFAULT = 2
ENEMY_SPAWN_TIME_DEFAULT = 2000  # ms
ENEMY_FIRE_CHANCE_DEFAULT = 0.004

# ---------- Scoring ----------
SCORE_PER_KILL = 100
SCORE_PENALTY_ESCAPE = 50
MAX_HIGH_SCORES = 5

# ---------- Stage / Difficulty ----------
STAGE_DURATION = 30_000  # ms per stage

STAGE_CONFIGS = [
    {  # Stage 1
        'bg': (4, 4, 18),
        'enemy_body': (220, 40, 40), 'enemy_wing': (180, 30, 30),
        'enemy_speed': 2, 'spawn_time': 2000, 'fire_chance': 0.004,
        'celestial': 'moon',
    },
    {  # Stage 2
        'bg': (10, 4, 24),
        'enemy_body': (40, 180, 220), 'enemy_wing': (30, 130, 180),
        'enemy_speed': 2.5, 'spawn_time': 1700, 'fire_chance': 0.006,
        'celestial': 'gas_planet',
    },
    {  # Stage 3
        'bg': (18, 8, 8),
        'enemy_body': (50, 220, 50), 'enemy_wing': (30, 160, 30),
        'enemy_speed': 3, 'spawn_time': 1400, 'fire_chance': 0.008,
        'celestial': 'rocky_planet',
    },
    {  # Stage 4
        'bg': (4, 14, 14),
        'enemy_body': (220, 160, 40), 'enemy_wing': (180, 120, 30),
        'enemy_speed': 3.5, 'spawn_time': 1100, 'fire_chance': 0.010,
        'celestial': 'ringed_planet',
    },
    {  # Stage 5
        'bg': (14, 4, 18),
        'enemy_body': (200, 50, 200), 'enemy_wing': (160, 30, 160),
        'enemy_speed': 4, 'spawn_time': 900, 'fire_chance': 0.013,
        'celestial': 'dark_planet',
    },
]

# ---------- Explosion colors ----------
ENEMY_EXPLOSION_COLORS = [
    (255, 200, 50), (255, 140, 30), (255, 80, 20),
    (255, 255, 100), (255, 60, 10),
]
PLAYER_EXPLOSION_COLORS = [
    (100, 180, 255), (180, 220, 255), (255, 255, 255),
    (50, 140, 255), (200, 240, 255),
]

# ---------- Background ----------
DEFAULT_BG_COLOR = (4, 4, 18)

STAR_LAYER_CONFIGS = [
    {'speed': 0.3, 'count': 80, 'bright_range': (60, 160), 'size': 1},
    {'speed': 0.7, 'count': 50, 'bright_range': (120, 255), 'size': 1},
    {'speed': 1.5, 'count': 25, 'bright_range': (120, 255), 'size_choices': [1, 2]},
]

GALAXY_MIN_DELAY = 600   # frames
GALAXY_MAX_DELAY = 1200

CELESTIAL_COOLDOWN_MIN = 600
CELESTIAL_COOLDOWN_MAX = 1200

# ---------- UI ----------
BUTTON_W = 200
BUTTON_H = 55
