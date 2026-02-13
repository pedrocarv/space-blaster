"""Background rendering: starfield, galaxies, and celestial bodies."""

import math
import random

import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    STAR_LAYER_CONFIGS,
    GALAXY_MIN_DELAY, GALAXY_MAX_DELAY,
)


# ---------- Starfield ----------

def create_star_layers():
    """Create three parallax star layers.

    Returns:
        list of (speed, star_list) tuples.
    """
    layers = []
    for cfg in STAR_LAYER_CONFIGS:
        stars = []
        for _ in range(cfg['count']):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            lo, hi = cfg['bright_range']
            brightness = random.randint(lo, hi)
            size = random.choice(cfg.get('size_choices', [cfg.get('size', 1)]))
            stars.append([sx, sy, brightness, size])
        layers.append((cfg['speed'], stars))
    return layers


def update_and_draw_stars(surface, layers):
    """Scroll stars downward and draw them."""
    for speed, stars in layers:
        for s in stars:
            s[1] += speed
            if s[1] > SCREEN_HEIGHT:
                s[0] = random.randint(0, SCREEN_WIDTH)
                s[1] = random.randint(-20, 0)
                s[2] = random.randint(100, 255)
            c = s[2]
            pygame.draw.circle(surface, (c, c, c), (int(s[0]), int(s[1])), s[3])


# ---------- Galaxy ----------

def spawn_galaxy():
    """Create a new galaxy dict positioned just above the screen."""
    gx = random.randint(80, SCREEN_WIDTH - 80)
    radius = random.randint(40, 70)
    tint = random.choice([
        (90, 60, 160),
        (60, 80, 170),
        (160, 80, 100),
        (70, 140, 160),
    ])
    angle = random.uniform(0, math.pi * 2)
    return {
        'x': gx, 'y': -radius * 2,
        'radius': radius,
        'tint': tint,
        'angle': angle,
        'speed': random.uniform(0.25, 0.6),
    }


def draw_galaxy(surface, g):
    """Draw a soft, glowing galaxy with spiral-arm hints."""
    gx, gy, r = int(g['x']), int(g['y']), g['radius']
    tr, tg_c, tb = g['tint']

    # Outer glow rings
    for i in range(6, 0, -1):
        frac = i / 6.0
        ring_r = int(r * frac * 1.3)
        alpha = int(18 * frac)
        color = (tr, tg_c, tb)
        glow_surf = pygame.Surface((ring_r * 2, ring_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, alpha), (ring_r, ring_r), ring_r)
        surface.blit(glow_surf, (gx - ring_r, gy - ring_r))

    # Spiral arm dots
    arm_count = 2
    for arm in range(arm_count):
        base_angle = g['angle'] + arm * math.pi
        for j in range(18):
            t = j / 18.0
            dist = r * 0.2 + r * 0.9 * t
            a = base_angle + t * 2.8
            dx = int(gx + math.cos(a) * dist)
            dy = int(gy + math.sin(a) * dist * 0.55)
            dot_alpha = int(100 * (1 - t * 0.7))
            dot_r = max(1, int(2 * (1 - t)))
            dot_surf = pygame.Surface((dot_r * 2, dot_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(dot_surf, (tr + 40, tg_c + 40, min(255, tb + 60), dot_alpha),
                               (dot_r, dot_r), dot_r)
            surface.blit(dot_surf, (dx - dot_r, dy - dot_r))

    # Bright core
    core_surf = pygame.Surface((12, 12), pygame.SRCALPHA)
    pygame.draw.circle(core_surf, (255, 255, 240, 90), (6, 6), 6)
    pygame.draw.circle(core_surf, (255, 255, 255, 160), (6, 6), 3)
    surface.blit(core_surf, (gx - 6, gy - 6))


# ---------- Celestial Bodies ----------

def spawn_celestial(cel_type):
    """Create a celestial body dict based on type."""
    x = random.randint(80, SCREEN_WIDTH - 80)
    obj = {'x': float(x), 'y': -120.0, 'speed': random.uniform(0.15, 0.35), 'type': cel_type}

    if cel_type == 'moon':
        obj['radius'] = random.randint(20, 35)
        obj['color'] = (160, 160, 150)
        obj['shadow'] = (100, 100, 95)
    elif cel_type == 'gas_planet':
        obj['radius'] = random.randint(50, 70)
        obj['color'] = (80, 60, 160)
        obj['bands'] = [(100, 80, 180), (60, 40, 140), (90, 70, 170)]
    elif cel_type == 'rocky_planet':
        obj['radius'] = random.randint(35, 50)
        obj['color'] = (160, 70, 40)
        obj['shadow'] = (100, 40, 25)
        obj['moon_offset'] = (random.randint(40, 60), random.randint(-20, 20))
        obj['moon_radius'] = random.randint(6, 10)
    elif cel_type == 'ringed_planet':
        obj['radius'] = random.randint(40, 55)
        obj['color'] = (60, 160, 150)
        obj['ring_color'] = (180, 160, 80)
    elif cel_type == 'dark_planet':
        obj['radius'] = random.randint(55, 75)
        obj['color'] = (30, 10, 35)
        obj['glow'] = (200, 50, 200)

    return obj


def draw_celestial(surface, obj):
    """Draw a celestial body on the surface."""
    cx, cy, r = int(obj['x']), int(obj['y']), obj['radius']
    t = obj['type']

    if t == 'moon':
        pygame.draw.circle(surface, obj['color'], (cx, cy), r)
        pygame.draw.circle(surface, obj['shadow'], (cx + r // 4, cy - r // 6), r - 2)
        for offset in [(r // 3, -r // 4), (-r // 4, r // 3), (0, 0)]:
            cr = max(2, r // 8)
            pygame.draw.circle(surface, obj['shadow'], (cx + offset[0], cy + offset[1]), cr)

    elif t == 'gas_planet':
        glow_s = pygame.Surface((r * 3, r * 3), pygame.SRCALPHA)
        pygame.draw.circle(glow_s, (*obj['color'], 25), (r * 3 // 2, r * 3 // 2), r * 3 // 2)
        surface.blit(glow_s, (cx - r * 3 // 2, cy - r * 3 // 2))
        pygame.draw.circle(surface, obj['color'], (cx, cy), r)
        for i, band_color in enumerate(obj['bands']):
            band_y = cy - r // 2 + i * (r // 2)
            band_s = pygame.Surface((r * 2, r // 4), pygame.SRCALPHA)
            pygame.draw.ellipse(band_s, (*band_color, 80), (0, 0, r * 2, r // 4))
            surface.blit(band_s, (cx - r, band_y))

    elif t == 'rocky_planet':
        pygame.draw.circle(surface, obj['color'], (cx, cy), r)
        pygame.draw.circle(surface, obj['shadow'], (cx + r // 3, cy - r // 5), r - 3)
        for dx, dy, cr in [(-r//3, r//4, r//6), (r//4, -r//3, r//7), (0, r//5, r//5)]:
            pygame.draw.circle(surface, (140, 55, 30), (cx + dx, cy + dy), max(2, cr))
        mx = cx + obj['moon_offset'][0]
        my = cy + obj['moon_offset'][1]
        pygame.draw.circle(surface, (140, 140, 130), (mx, my), obj['moon_radius'])
        pygame.draw.circle(surface, (100, 100, 95), (mx + 2, my - 1), obj['moon_radius'] - 1)

    elif t == 'ringed_planet':
        ring_s = pygame.Surface((r * 4, r * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(ring_s, (*obj['ring_color'], 60), (0, r // 2, r * 4, r))
        pygame.draw.ellipse(ring_s, (0, 0, 0, 0), (r // 2, r // 2 + r // 4, r * 3, r // 2))
        surface.blit(ring_s, (cx - r * 2, cy - r))
        pygame.draw.circle(surface, obj['color'], (cx, cy), r)
        hl_s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(hl_s, (255, 255, 255, 20), (r, r), r)
        pygame.draw.circle(hl_s, (255, 255, 255, 40), (r - r // 4, r - r // 4), r // 2)
        surface.blit(hl_s, (cx - r, cy - r))

    elif t == 'dark_planet':
        for i in range(5):
            gr = r + 8 - i * 2
            g_s = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
            pygame.draw.circle(g_s, (*obj['glow'], 15 + i * 8), (gr, gr), gr)
            surface.blit(g_s, (cx - gr, cy - gr))
        pygame.draw.circle(surface, obj['color'], (cx, cy), r)
        for _ in range(4):
            tx = cx + random.randint(-r // 2, r // 2)
            ty = cy + random.randint(-r // 2, r // 2)
            pygame.draw.circle(surface, (40, 15, 45), (tx, ty), random.randint(3, 8))
