"""Ship and projectile rendering functions for Space Blaster.

Enhanced with multi-layered detail, panel lines, animated effects.
"""

import math
import random

import pygame


# ---------- Player Ship ----------

def draw_player_ship(surface, x, y, w, h):
    """Draw a highly detailed player spaceship with layered panels and glow effects."""
    cx = x + w / 2

    # --- Shield glow (subtle aura) ---
    shield_s = pygame.Surface((w + 30, h + 30), pygame.SRCALPHA)
    pygame.draw.ellipse(shield_s, (40, 120, 255, 15), (0, 5, w + 30, h + 20))
    surface.blit(shield_s, (x - 15, y - 10))

    # --- Wing struts (behind body) ---
    # Left strut
    left_strut = [
        (cx - w * 0.1, y + h * 0.55),
        (x - w * 0.35, y + h * 0.9),
        (x - w * 0.25, y + h),
        (cx - w * 0.05, y + h * 0.7),
    ]
    pygame.draw.polygon(surface, (8, 55, 140), left_strut)
    # Right strut
    right_strut = [
        (cx + w * 0.1, y + h * 0.55),
        (x + w + w * 0.35, y + h * 0.9),
        (x + w + w * 0.25, y + h),
        (cx + w * 0.05, y + h * 0.7),
    ]
    pygame.draw.polygon(surface, (8, 55, 140), right_strut)

    # --- Wings ---
    # Left wing
    lw = [
        (x + w * 0.12, y + h * 0.5),
        (x - w * 0.38, y + h * 0.82),
        (x - w * 0.32, y + h),
        (x - w * 0.15, y + h),
        (x + w * 0.2, y + h * 0.85),
    ]
    pygame.draw.polygon(surface, (10, 65, 170), lw)
    # Wing panel line
    pygame.draw.line(surface, (20, 90, 210),
                     (int(x + w * 0.15), int(y + h * 0.55)),
                     (int(x - w * 0.25), int(y + h * 0.95)), 1)
    # Wingtip light
    pygame.draw.circle(surface, (100, 200, 255), (int(x - w * 0.35), int(y + h * 0.85)), 2)

    # Right wing
    rw = [
        (x + w * 0.88, y + h * 0.5),
        (x + w + w * 0.38, y + h * 0.82),
        (x + w + w * 0.32, y + h),
        (x + w + w * 0.15, y + h),
        (x + w * 0.8, y + h * 0.85),
    ]
    pygame.draw.polygon(surface, (10, 65, 170), rw)
    pygame.draw.line(surface, (20, 90, 210),
                     (int(x + w * 0.85), int(y + h * 0.55)),
                     (int(x + w + w * 0.25), int(y + h * 0.95)), 1)
    pygame.draw.circle(surface, (100, 200, 255), (int(x + w + w * 0.35), int(y + h * 0.85)), 2)

    # --- Main body ---
    body = [
        (cx, y),                            # nose
        (x + w * 0.82, y + h * 0.55),
        (x + w * 0.78, y + h * 0.85),
        (x + w * 0.65, y + h),
        (x + w * 0.35, y + h),
        (x + w * 0.22, y + h * 0.85),
        (x + w * 0.18, y + h * 0.55),
    ]
    pygame.draw.polygon(surface, (20, 95, 215), body)

    # Body center highlight
    hl = [
        (cx, y + 3),
        (cx + w * 0.12, y + h * 0.5),
        (cx + w * 0.08, y + h * 0.85),
        (cx - w * 0.08, y + h * 0.85),
        (cx - w * 0.12, y + h * 0.5),
    ]
    pygame.draw.polygon(surface, (50, 140, 255), hl)

    # Nose bright tip
    pygame.draw.polygon(surface, (120, 200, 255), [
        (cx, y), (cx + 4, y + h * 0.1), (cx - 4, y + h * 0.1)])

    # --- Panel lines (detail ridges) ---
    for frac in [0.35, 0.55, 0.75]:
        lx = int(x + w * 0.22 + (w * 0.56) * 0.15)
        rx = int(x + w * 0.22 + (w * 0.56) * 0.85)
        ly = int(y + h * frac)
        pygame.draw.line(surface, (15, 80, 190), (lx, ly), (rx, ly), 1)

    # --- Cockpit canopy ---
    cockpit = [
        (cx, y + h * 0.15),
        (cx + w * 0.11, y + h * 0.35),
        (cx + w * 0.08, y + h * 0.48),
        (cx - w * 0.08, y + h * 0.48),
        (cx - w * 0.11, y + h * 0.35),
    ]
    pygame.draw.polygon(surface, (60, 180, 255), cockpit)
    # Canopy frame
    pygame.draw.polygon(surface, (80, 200, 255), cockpit, width=1)
    # Canopy shine
    shine = [
        (cx - 2, y + h * 0.18),
        (cx + 3, y + h * 0.28),
        (cx, y + h * 0.32),
        (cx - 3, y + h * 0.26),
    ]
    pygame.draw.polygon(surface, (180, 240, 255), shine)

    # --- Antenna ---
    pygame.draw.line(surface, (150, 200, 255), (int(cx), int(y)), (int(cx), int(y - 6)), 1)
    pygame.draw.circle(surface, (200, 240, 255), (int(cx), int(y - 7)), 1)

    # --- Engine nozzles ---
    for nx in [cx - w * 0.12, cx + w * 0.12]:
        nozzle = [
            (nx - 4, y + h * 0.92), (nx + 4, y + h * 0.92),
            (nx + 5, y + h), (nx - 5, y + h),
        ]
        pygame.draw.polygon(surface, (60, 70, 90), nozzle)
        pygame.draw.polygon(surface, (100, 110, 130), nozzle, width=1)

    # --- Engine exhaust flames ---
    flame_flicker = random.uniform(0.8, 1.0)
    for nx in [cx - w * 0.12, cx + w * 0.12]:
        fh = int(14 * flame_flicker)
        # Outer flame
        pygame.draw.polygon(surface, (255, 100, 20), [
            (nx - 5, y + h), (nx, y + h + fh), (nx + 5, y + h)])
        # Inner flame
        fh2 = int(fh * 0.55)
        pygame.draw.polygon(surface, (255, 220, 100), [
            (nx - 2, y + h), (nx, y + h + fh2), (nx + 2, y + h)])
        # Core white
        pygame.draw.polygon(surface, (255, 255, 230), [
            (nx - 1, y + h), (nx, y + h + fh2 * 0.5), (nx + 1, y + h)])

    # Engine glow halo
    g_s = pygame.Surface((w, 14), pygame.SRCALPHA)
    pygame.draw.ellipse(g_s, (80, 160, 255, 40), (w // 4, 0, w // 2, 14))
    surface.blit(g_s, (x, y + h - 3))


# ---------- Enemy Ship ----------

def draw_enemy_ship(surface, x, y, w, h, body_color, wing_color):
    """Draw a highly detailed enemy ship with aggressive silhouette and glow."""
    bcr, bcg, bcb = body_color
    wcr, wcg, wcb = wing_color
    cx = x + w / 2

    # Threat glow underneath
    g_s = pygame.Surface((w + 20, h + 10), pygame.SRCALPHA)
    pygame.draw.ellipse(g_s, (bcr, bcg, bcb, 18), (0, 0, w + 20, h + 10))
    surface.blit(g_s, (x - 10, y))

    # --- Weapon pods on wings ---
    for px in [x - w * 0.25, x + w + w * 0.15]:
        pod = pygame.Rect(int(px), int(y + h * 0.2), 5, 12)
        pygame.draw.rect(surface, (max(0, wcr - 20), max(0, wcg - 20), max(0, wcb - 20)), pod)
        pygame.draw.rect(surface, wing_color, pod, width=1)
        # Muzzle flash dot
        pygame.draw.circle(surface, (255, 200, 60), (int(px + 2), int(y + h * 0.2 + 12)), 1)

    # --- Wings ---
    # Left wing (aggressive sweep)
    lw = [
        (x + w * 0.15, y + h * 0.08),
        (x - w * 0.38, y + h * 0.1),
        (x - w * 0.3, y + h * 0.45),
        (x + w * 0.05, y + h * 0.5),
    ]
    pygame.draw.polygon(surface, wing_color, lw)
    # Wing panel line
    pygame.draw.line(surface, (min(255, wcr + 30), min(255, wcg + 30), min(255, wcb + 30)),
                     (int(x + w * 0.1), int(y + h * 0.12)),
                     (int(x - w * 0.2), int(y + h * 0.38)), 1)

    # Right wing
    rw = [
        (x + w * 0.85, y + h * 0.08),
        (x + w + w * 0.38, y + h * 0.1),
        (x + w + w * 0.3, y + h * 0.45),
        (x + w * 0.95, y + h * 0.5),
    ]
    pygame.draw.polygon(surface, wing_color, rw)
    pygame.draw.line(surface, (min(255, wcr + 30), min(255, wcg + 30), min(255, wcb + 30)),
                     (int(x + w * 0.9), int(y + h * 0.12)),
                     (int(x + w + w * 0.2), int(y + h * 0.38)), 1)

    # --- Main body ---
    body = [
        (x + w * 0.25, y),
        (x + w * 0.75, y),
        (x + w * 0.9, y + h * 0.35),
        (x + w * 0.7, y + h * 0.7),
        (cx, y + h),
        (x + w * 0.3, y + h * 0.7),
        (x + w * 0.1, y + h * 0.35),
    ]
    pygame.draw.polygon(surface, body_color, body)

    # Body shading — darker bottom
    shade = [
        (x + w * 0.15, y + h * 0.45),
        (x + w * 0.85, y + h * 0.45),
        (x + w * 0.7, y + h * 0.7),
        (cx, y + h),
        (x + w * 0.3, y + h * 0.7),
    ]
    pygame.draw.polygon(surface, (max(0, bcr - 50), max(0, bcg - 50), max(0, bcb - 50)), shade)

    # Body highlight strip
    hl = [
        (cx - w * 0.08, y + h * 0.03),
        (cx + w * 0.08, y + h * 0.03),
        (cx + w * 0.05, y + h * 0.4),
        (cx - w * 0.05, y + h * 0.4),
    ]
    pygame.draw.polygon(surface, (min(255, bcr + 50), min(255, bcg + 50), min(255, bcb + 50)), hl)

    # Panel lines
    for frac in [0.2, 0.4, 0.58]:
        lx = int(x + w * 0.2)
        rx = int(x + w * 0.8)
        ly = int(y + h * frac)
        pygame.draw.line(surface, (max(0, bcr - 25), max(0, bcg - 25), max(0, bcb - 25)),
                         (lx, ly), (rx, ly), 1)

    # --- Vent slits (sides) ---
    for vx, sign in [(x + w * 0.15, -1), (x + w * 0.8, 1)]:
        for vi in range(3):
            vy = y + h * 0.55 + vi * 5
            pygame.draw.line(surface, (max(0, bcr - 40), max(0, bcg - 40), max(0, bcb - 40)),
                             (int(vx), int(vy)), (int(vx + sign * 6), int(vy)), 1)

    # --- Cockpit / menacing eye ---
    eye_cy = int(y + h * 0.28)

    # Eye glow halo
    eg = pygame.Surface((28, 28), pygame.SRCALPHA)
    pygame.draw.circle(eg, (255, 180, 40, 35), (14, 14), 14)
    surface.blit(eg, (int(cx - 14), eye_cy - 14))

    # Eye diamond
    cockpit = [
        (cx, y + h * 0.14),
        (cx + w * 0.14, y + h * 0.28),
        (cx, y + h * 0.42),
        (cx - w * 0.14, y + h * 0.28),
    ]
    pygame.draw.polygon(surface, (255, 160, 40), cockpit)
    # Inner bright ring
    pygame.draw.polygon(surface, (255, 200, 80), cockpit, width=1)
    # Pupil
    pygame.draw.circle(surface, (255, 255, 200), (int(cx), eye_cy), 4)
    pygame.draw.circle(surface, (255, 100, 20), (int(cx), eye_cy), 2)

    # --- Nose spike ---
    pygame.draw.polygon(surface, body_color, [
        (cx, y - 4), (cx - 3, y + h * 0.05), (cx + 3, y + h * 0.05)])
    pygame.draw.circle(surface, (255, 200, 60), (int(cx), int(y - 4)), 1)


# ---------- Lasers ----------

def draw_laser(surface, rect):
    """Draw a vibrant player laser with animated glow and particle trail."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx = x + w // 2

    # Wide outer glow
    for i in range(3):
        gw = w + 14 - i * 4
        gh = h + 12 - i * 3
        gs = pygame.Surface((gw, gh), pygame.SRCALPHA)
        alpha = 20 + i * 15
        pygame.draw.ellipse(gs, (60, 255, 100, alpha), (0, 0, gw, gh))
        surface.blit(gs, (cx - gw // 2, y - 6 + i * 2))

    # Core beam with gradient
    core_w = max(3, w)
    for i in range(core_w):
        frac = abs(i - core_w / 2) / (core_w / 2)
        r = int(120 + 135 * (1 - frac))
        g = 255
        b = int(150 + 105 * (1 - frac))
        pygame.draw.line(surface, (r, g, b),
                         (cx - core_w // 2 + i, y + 4),
                         (cx - core_w // 2 + i, y + h - 3))

    # Hot center line
    pygame.draw.line(surface, (255, 255, 255), (cx, y + 3), (cx, y + h - 2), 1)

    # Pointed tip with bright flash
    tip = [(cx, y - 5), (cx - w // 2 - 2, y + 5), (cx + w // 2 + 2, y + 5)]
    pygame.draw.polygon(surface, (180, 255, 200), tip)
    pygame.draw.circle(surface, (255, 255, 255), (cx, y - 3), 3)
    pygame.draw.circle(surface, (200, 255, 220), (cx, y - 3), 5)

    # Particle trail sparks
    for _ in range(2):
        sx = cx + random.randint(-3, 3)
        sy = y + h + random.randint(-2, 6)
        spark_s = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(spark_s, (100, 255, 130, random.randint(80, 200)), (2, 2), 2)
        surface.blit(spark_s, (sx - 2, sy - 2))

    # Fading tail
    tail_s = pygame.Surface((w + 8, 14), pygame.SRCALPHA)
    pygame.draw.polygon(tail_s, (60, 255, 100, 40),
                        [(0, 0), (w + 8, 0), ((w + 8) // 2, 14)])
    surface.blit(tail_s, (cx - (w + 8) // 2, y + h - 2))


def draw_enemy_laser(surface, rect):
    """Draw a menacing enemy laser with red-orange glow and sparks."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx = x + w // 2

    # Wide outer glow
    for i in range(3):
        gw = w + 14 - i * 4
        gh = h + 12 - i * 3
        gs = pygame.Surface((gw, gh), pygame.SRCALPHA)
        alpha = 20 + i * 15
        pygame.draw.ellipse(gs, (255, 50, 30, alpha), (0, 0, gw, gh))
        surface.blit(gs, (cx - gw // 2, y - 6 + i * 2))

    # Core beam with gradient
    core_w = max(3, w)
    for i in range(core_w):
        frac = abs(i - core_w / 2) / (core_w / 2)
        r = 255
        g = int(100 + 120 * (1 - frac))
        b = int(50 + 130 * (1 - frac))
        pygame.draw.line(surface, (r, g, b),
                         (cx - core_w // 2 + i, y + 4),
                         (cx - core_w // 2 + i, y + h - 3))

    # Hot center line
    pygame.draw.line(surface, (255, 255, 220), (cx, y + 3), (cx, y + h - 2), 1)

    # Pointed tip (bottom, downward)
    tip = [(cx, y + h + 5), (cx - w // 2 - 2, y + h - 5), (cx + w // 2 + 2, y + h - 5)]
    pygame.draw.polygon(surface, (255, 180, 100), tip)
    pygame.draw.circle(surface, (255, 255, 200), (cx, y + h + 3), 3)
    pygame.draw.circle(surface, (255, 200, 120), (cx, y + h + 3), 5)

    # Particle sparks trailing up
    for _ in range(2):
        sx = cx + random.randint(-3, 3)
        sy = y + random.randint(-6, 2)
        spark_s = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(spark_s, (255, 120, 50, random.randint(80, 200)), (2, 2), 2)
        surface.blit(spark_s, (sx - 2, sy - 2))

    # Fading tail (top)
    tail_s = pygame.Surface((w + 8, 14), pygame.SRCALPHA)
    pygame.draw.polygon(tail_s, (255, 60, 30, 40),
                        [((w + 8) // 2, 0), (0, 14), (w + 8, 14)])
    surface.blit(tail_s, (cx - (w + 8) // 2, y - 12))


# ---------- HUD Hearts ----------

def draw_hearts(surface, lives):
    """Draw pixel-art heart icons with shadow and highlights."""
    for i in range(lives):
        hx = 15 + i * 32
        hy = 12

        # Shadow
        sh = pygame.Surface((24, 22), pygame.SRCALPHA)
        pygame.draw.circle(sh, (0, 0, 0, 70), (7, 7), 7)
        pygame.draw.circle(sh, (0, 0, 0, 70), (17, 7), 7)
        pygame.draw.polygon(sh, (0, 0, 0, 70), [(0, 10), (24, 10), (12, 22)])
        surface.blit(sh, (hx + 2, hy + 2))

        # Heart body
        pygame.draw.circle(surface, (230, 35, 55), (hx + 6, hy + 6), 6)
        pygame.draw.circle(surface, (230, 35, 55), (hx + 16, hy + 6), 6)
        pygame.draw.polygon(surface, (230, 35, 55),
                            [(hx - 1, hy + 9), (hx + 23, hy + 9), (hx + 11, hy + 21)])

        # Darker bottom shade
        pygame.draw.polygon(surface, (180, 25, 40),
                            [(hx + 2, hy + 14), (hx + 20, hy + 14), (hx + 11, hy + 21)])

        # Highlight shine
        pygame.draw.circle(surface, (255, 140, 160), (hx + 4, hy + 4), 2)
        pygame.draw.circle(surface, (255, 200, 210), (hx + 4, hy + 3), 1)
