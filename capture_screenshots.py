#!/usr/bin/env python3
"""Capture screenshots of each game screen for the README."""

import os
import sys
import random

# Render offscreen (no window needed)
os.environ['SDL_VIDEODRIVER'] = 'dummy'

import pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, STAGE_CONFIGS
from screens import Fonts, BUTTON_RECT, draw_title_screen, draw_hud, draw_game_over_screen
from renderer import draw_player_ship, draw_enemy_ship, draw_laser, draw_enemy_laser
from background import create_star_layers, update_and_draw_stars, spawn_galaxy, draw_galaxy
from particles import ParticleSystem

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fonts = Fonts()
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
os.makedirs(out_dir, exist_ok=True)

# Seed for reproducibility
random.seed(42)

# Create starfield
star_layers = create_star_layers()


def draw_bg(surface):
    surface.fill((4, 4, 18))
    update_and_draw_stars(surface, star_layers)


# --- 1. Title screen ---
draw_bg(screen)
galaxy = spawn_galaxy()
galaxy['y'] = SCREEN_HEIGHT * 0.6
draw_galaxy(screen, galaxy)
draw_title_screen(screen, fonts, [5200, 4100, 3800, 2500, 1200],
                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80), 60,
                  PLAYER_WIDTH, PLAYER_HEIGHT)
pygame.image.save(screen, os.path.join(out_dir, 'title_screen.png'))
print('Saved title_screen.png')


# --- 2. Gameplay ---
random.seed(99)
draw_bg(screen)

# Draw a few enemies
cfg = STAGE_CONFIGS[0]
enemy_positions = [(120, 60), (350, 30), (550, 90), (680, 50), (250, 140)]
for ex, ey in enemy_positions:
    draw_enemy_ship(screen, ex, ey, ENEMY_WIDTH, ENEMY_HEIGHT,
                    cfg['enemy_body'], cfg['enemy_wing'])

# Draw enemy lasers
for ebx, eby in [(145, 120), (575, 150), (370, 90)]:
    eb_rect = pygame.Rect(ebx, eby, 5, 14)
    draw_enemy_laser(screen, eb_rect)

# Draw player
draw_player_ship(screen, SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2,
                 SCREEN_HEIGHT - PLAYER_HEIGHT - 20,
                 PLAYER_WIDTH, PLAYER_HEIGHT)

# Draw player lasers
for lx in [SCREEN_WIDTH // 2 - 3, SCREEN_WIDTH // 2 + 30]:
    bullet = pygame.Rect(lx, 300, 6, 18)
    draw_laser(screen, bullet)

# Explosion
particles = ParticleSystem()
particles.spawn(400, 200, [(255, 200, 50), (255, 140, 30), (255, 80, 20)],
                count=25, speed_range=(1.5, 5), lifetime=20)
# Advance a few frames for the particles to spread
for _ in range(5):
    buf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    particles.update_and_draw(buf)
# Draw final state
particles.update_and_draw(screen)

# HUD
draw_hud(screen, fonts, 2400, 1, 3)

pygame.image.save(screen, os.path.join(out_dir, 'gameplay.png'))
print('Saved gameplay.png')


# --- 3. Game Over ---
random.seed(77)
draw_bg(screen)

# Lingering particles
particles2 = ParticleSystem()
particles2.spawn(400, 300, [(100, 180, 255), (180, 220, 255)],
                 count=35, speed_range=(2, 6), lifetime=30)
for _ in range(10):
    buf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    particles2.update_and_draw(buf)
particles2.update_and_draw(screen)

draw_game_over_screen(screen, fonts, 4200, 3,
                      [5200, 4200, 4100, 3800, 2500],
                      (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
pygame.image.save(screen, os.path.join(out_dir, 'game_over.png'))
print('Saved game_over.png')

pygame.quit()
print('All screenshots saved to screenshots/')
