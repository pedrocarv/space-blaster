"""Ship and projectile rendering functions for Space Blaster."""

import math
import random

import pygame


def draw_player_ship(surface, x, y, w, h):
    """Draw a detailed, shaded player spaceship with engine flame animation."""
    # --- Shadow/ground glow underneath ---
    shadow_s = pygame.Surface((w + 20, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_s, (0, 100, 255, 20), (0, 0, w + 20, 10))
    surface.blit(shadow_s, (x - 10, y + h - 2))

    # --- Main body (pointed nose) ---
    body = [
        (x + w // 2, y),
        (x + w * 0.85, y + h * 0.6),
        (x + w * 0.75, y + h),
        (x + w * 0.25, y + h),
        (x + w * 0.15, y + h * 0.6),
    ]
    pygame.draw.polygon(surface, (20, 100, 220), body)

    # Body highlight (lighter center strip)
    highlight = [
        (x + w // 2, y + 2),
        (x + w * 0.62, y + h * 0.55),
        (x + w * 0.55, y + h * 0.9),
        (x + w * 0.45, y + h * 0.9),
        (x + w * 0.38, y + h * 0.55),
    ]
    pygame.draw.polygon(surface, (40, 140, 255), highlight)

    # Nose tip highlight
    nose_hl = [
        (x + w // 2, y),
        (x + w * 0.55, y + h * 0.15),
        (x + w * 0.45, y + h * 0.15),
    ]
    pygame.draw.polygon(surface, (100, 180, 255), nose_hl)

    # --- Wings ---
    # Left wing
    left_wing = [
        (x + w * 0.15, y + h * 0.5),
        (x - w * 0.3, y + h * 0.85),
        (x - w * 0.2, y + h),
        (x + w * 0.25, y + h),
    ]
    pygame.draw.polygon(surface, (10, 70, 180), left_wing)
    # Left wing edge highlight
    pygame.draw.line(surface, (60, 150, 255),
                     (int(x + w * 0.15), int(y + h * 0.5)),
                     (int(x - w * 0.3), int(y + h * 0.85)), 1)

    # Right wing
    right_wing = [
        (x + w * 0.85, y + h * 0.5),
        (x + w + w * 0.3, y + h * 0.85),
        (x + w + w * 0.2, y + h),
        (x + w * 0.75, y + h),
    ]
    pygame.draw.polygon(surface, (10, 70, 180), right_wing)
    pygame.draw.line(surface, (60, 150, 255),
                     (int(x + w * 0.85), int(y + h * 0.5)),
                     (int(x + w + w * 0.3), int(y + h * 0.85)), 1)

    # --- Cockpit canopy ---
    cockpit = [
        (x + w // 2, y + h * 0.2),
        (x + w * 0.6, y + h * 0.42),
        (x + w // 2, y + h * 0.55),
        (x + w * 0.4, y + h * 0.42),
    ]
    pygame.draw.polygon(surface, (80, 200, 255), cockpit)
    # Cockpit shine
    shine = [
        (x + w * 0.48, y + h * 0.24),
        (x + w * 0.55, y + h * 0.35),
        (x + w * 0.48, y + h * 0.38),
    ]
    pygame.draw.polygon(surface, (180, 240, 255), shine)

    # --- Engine exhaust (animated flame) ---
    flame_flicker = random.uniform(0.7, 1.0)
    flame_h = int(12 * flame_flicker)

    # Outer flame (orange-red)
    outer_flame = [
        (x + w * 0.32, y + h),
        (x + w // 2, y + h + flame_h),
        (x + w * 0.68, y + h),
    ]
    pygame.draw.polygon(surface, (255, 120, 30), outer_flame)

    # Inner flame (yellow-white)
    inner_flame = [
        (x + w * 0.40, y + h),
        (x + w // 2, y + h + flame_h * 0.6),
        (x + w * 0.60, y + h),
    ]
    pygame.draw.polygon(surface, (255, 240, 150), inner_flame)

    # Engine glow halo
    glow_s = pygame.Surface((30, 16), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_s, (100, 180, 255, 50), (0, 0, 30, 16))
    surface.blit(glow_s, (x + w // 2 - 15, y + h - 5))


def draw_enemy_ship(surface, x, y, w, h, body_color, wing_color):
    """Draw a detailed, menacing enemy ship with shading and eye glow."""
    bc_r, bc_g, bc_b = body_color
    wc_r, wc_g, wc_b = wing_color

    # --- Main body (inverted arrow) ---
    body = [
        (x + w * 0.2, y),
        (x + w * 0.8, y),
        (x + w, y + h * 0.4),
        (x + w // 2, y + h),
        (x, y + h * 0.4),
    ]
    pygame.draw.polygon(surface, body_color, body)

    # Body shading (darker lower half)
    shade = [
        (x + w * 0.1, y + h * 0.45),
        (x + w * 0.9, y + h * 0.45),
        (x + w // 2, y + h),
    ]
    dark_body = (max(0, bc_r - 40), max(0, bc_g - 40), max(0, bc_b - 40))
    pygame.draw.polygon(surface, dark_body, shade)

    # Body highlight strip
    hl = [
        (x + w * 0.4, y + h * 0.05),
        (x + w * 0.6, y + h * 0.05),
        (x + w * 0.55, y + h * 0.35),
        (x + w * 0.45, y + h * 0.35),
    ]
    light_body = (min(255, bc_r + 40), min(255, bc_g + 40), min(255, bc_b + 40))
    pygame.draw.polygon(surface, light_body, hl)

    # --- Wings ---
    # Left wing with detail
    left_wing = [
        (x, y + h * 0.4),
        (x - w * 0.35, y + h * 0.12),
        (x + w * 0.15, y),
    ]
    pygame.draw.polygon(surface, wing_color, left_wing)
    # Wing edge
    dark_wing = (max(0, wc_r - 30), max(0, wc_g - 30), max(0, wc_b - 30))
    pygame.draw.line(surface, dark_wing,
                     (int(x - w * 0.35), int(y + h * 0.12)),
                     (int(x), int(y + h * 0.4)), 1)

    # Right wing
    right_wing = [
        (x + w, y + h * 0.4),
        (x + w + w * 0.35, y + h * 0.12),
        (x + w * 0.85, y),
    ]
    pygame.draw.polygon(surface, wing_color, right_wing)
    pygame.draw.line(surface, dark_wing,
                     (int(x + w + w * 0.35), int(y + h * 0.12)),
                     (int(x + w), int(y + h * 0.4)), 1)

    # --- Cockpit / glowing eye ---
    eye_cx = int(x + w // 2)
    eye_cy = int(y + h * 0.32)

    # Eye glow
    glow_s = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(glow_s, (255, 200, 60, 40), (10, 10), 10)
    surface.blit(glow_s, (eye_cx - 10, eye_cy - 10))

    # Eye shape
    cockpit = [
        (x + w // 2, y + h * 0.18),
        (x + w * 0.62, y + h * 0.32),
        (x + w // 2, y + h * 0.46),
        (x + w * 0.38, y + h * 0.32),
    ]
    pygame.draw.polygon(surface, (255, 180, 60), cockpit)
    # Bright center pupil
    pygame.draw.circle(surface, (255, 255, 200), (eye_cx, eye_cy), 3)


def draw_laser(surface, rect):
    """Draw a glowing player laser bolt with a pointed tip and fading tail."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx = x + w // 2

    # Outer glow
    glow_w, glow_h = w + 12, h + 10
    glow_surf = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf, (60, 255, 100, 30), (0, 0, glow_w, glow_h))
    surface.blit(glow_surf, (cx - glow_w // 2, y - 5))

    # Mid glow
    mid_w, mid_h = w + 4, h + 2
    mid_surf = pygame.Surface((mid_w, mid_h), pygame.SRCALPHA)
    pygame.draw.ellipse(mid_surf, (120, 255, 140, 80), (0, 0, mid_w, mid_h))
    surface.blit(mid_surf, (cx - mid_w // 2, y - 1))

    # Bright core beam
    core_w = max(2, w - 2)
    pygame.draw.rect(surface, (160, 255, 180), (cx - core_w // 2, y + 4, core_w, h - 6))

    # Hot white center line
    pygame.draw.line(surface, (240, 255, 245), (cx, y + 5), (cx, y + h - 3), 1)

    # Pointed tip
    tip = [
        (cx, y - 4),
        (cx - w // 2 - 2, y + 5),
        (cx + w // 2 + 2, y + 5),
    ]
    pygame.draw.polygon(surface, (200, 255, 220), tip)
    pygame.draw.circle(surface, (255, 255, 255), (cx, y - 2), 2)

    # Fading tail
    tail_surf = pygame.Surface((w + 6, 10), pygame.SRCALPHA)
    tail = [(0, 0), (w + 6, 0), ((w + 6) // 2, 10)]
    pygame.draw.polygon(tail_surf, (80, 255, 110, 50), tail)
    surface.blit(tail_surf, (cx - (w + 6) // 2, y + h - 2))


def draw_enemy_laser(surface, rect):
    """Draw a red-orange enemy laser bolt (pointing downward)."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx = x + w // 2

    # Outer glow
    glow_w, glow_h = w + 12, h + 10
    glow_surf = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf, (255, 50, 30, 30), (0, 0, glow_w, glow_h))
    surface.blit(glow_surf, (cx - glow_w // 2, y - 5))

    # Mid glow
    mid_w, mid_h = w + 4, h + 2
    mid_surf = pygame.Surface((mid_w, mid_h), pygame.SRCALPHA)
    pygame.draw.ellipse(mid_surf, (255, 100, 50, 80), (0, 0, mid_w, mid_h))
    surface.blit(mid_surf, (cx - mid_w // 2, y - 1))

    # Core beam
    core_w = max(2, w - 2)
    pygame.draw.rect(surface, (255, 130, 70), (cx - core_w // 2, y + 4, core_w, h - 6))

    # Hot center line
    pygame.draw.line(surface, (255, 220, 180), (cx, y + 3), (cx, y + h - 3), 1)

    # Pointed tip (bottom)
    tip = [
        (cx, y + h + 4),
        (cx - w // 2 - 2, y + h - 5),
        (cx + w // 2 + 2, y + h - 5),
    ]
    pygame.draw.polygon(surface, (255, 180, 100), tip)
    pygame.draw.circle(surface, (255, 255, 200), (cx, y + h + 2), 2)

    # Fading tail (top)
    tail_surf = pygame.Surface((w + 6, 10), pygame.SRCALPHA)
    tail = [((w + 6) // 2, 0), (0, 10), (w + 6, 10)]
    pygame.draw.polygon(tail_surf, (255, 60, 40, 50), tail)
    surface.blit(tail_surf, (cx - (w + 6) // 2, y - 8))


def draw_hearts(surface, lives):
    """Draw pixel-art style heart icons for the HUD."""
    for i in range(lives):
        hx = 15 + i * 32
        hy = 12

        # Shadow
        shadow_s = pygame.Surface((24, 22), pygame.SRCALPHA)
        pygame.draw.circle(shadow_s, (0, 0, 0, 60), (7, 7), 7)
        pygame.draw.circle(shadow_s, (0, 0, 0, 60), (17, 7), 7)
        pygame.draw.polygon(shadow_s, (0, 0, 0, 60),
                            [(0, 10), (24, 10), (12, 22)])
        surface.blit(shadow_s, (hx + 1, hy + 1))

        # Main heart (bright red)
        pygame.draw.circle(surface, (240, 40, 60), (hx + 6, hy + 6), 6)
        pygame.draw.circle(surface, (240, 40, 60), (hx + 16, hy + 6), 6)
        pygame.draw.polygon(surface, (240, 40, 60),
                            [(hx - 1, hy + 9), (hx + 23, hy + 9), (hx + 11, hy + 21)])

        # Heart highlight (top-left shine)
        pygame.draw.circle(surface, (255, 120, 140), (hx + 4, hy + 4), 2)
