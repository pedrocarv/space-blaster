"""Ship and projectile rendering functions for Space Blaster."""

import pygame


def draw_player_ship(surface, x, y, w, h):
    """Draw a sleek upward-pointing spaceship for the player."""
    # Main body (pointed nose)
    body = [
        (x + w // 2, y),
        (x + w, y + h * 0.65),
        (x + w * 0.8, y + h),
        (x + w * 0.2, y + h),
        (x, y + h * 0.65),
    ]
    pygame.draw.polygon(surface, (0, 128, 255), body)

    # Wing – left
    left_wing = [
        (x, y + h * 0.65),
        (x - w * 0.25, y + h),
        (x + w * 0.2, y + h),
    ]
    pygame.draw.polygon(surface, (0, 90, 200), left_wing)

    # Wing – right
    right_wing = [
        (x + w, y + h * 0.65),
        (x + w + w * 0.25, y + h),
        (x + w * 0.8, y + h),
    ]
    pygame.draw.polygon(surface, (0, 90, 200), right_wing)

    # Cockpit window
    cockpit = [
        (x + w // 2, y + h * 0.18),
        (x + w * 0.62, y + h * 0.48),
        (x + w // 2, y + h * 0.58),
        (x + w * 0.38, y + h * 0.48),
    ]
    pygame.draw.polygon(surface, (130, 220, 255), cockpit)

    # Engine glow
    engine_glow = [
        (x + w * 0.35, y + h),
        (x + w // 2, y + h + 8),
        (x + w * 0.65, y + h),
    ]
    pygame.draw.polygon(surface, (255, 180, 50), engine_glow)


def draw_enemy_ship(surface, x, y, w, h, body_color, wing_color):
    """Draw a menacing downward-facing enemy ship."""
    # Main body (inverted, nose pointing down)
    body = [
        (x + w * 0.2, y),
        (x + w * 0.8, y),
        (x + w, y + h * 0.4),
        (x + w // 2, y + h),
        (x, y + h * 0.4),
    ]
    pygame.draw.polygon(surface, body_color, body)

    # Wing – left
    left_wing = [
        (x, y + h * 0.4),
        (x - w * 0.3, y + h * 0.15),
        (x + w * 0.15, y),
    ]
    pygame.draw.polygon(surface, wing_color, left_wing)

    # Wing – right
    right_wing = [
        (x + w, y + h * 0.4),
        (x + w + w * 0.3, y + h * 0.15),
        (x + w * 0.85, y),
    ]
    pygame.draw.polygon(surface, wing_color, right_wing)

    # Cockpit / eye
    cockpit = [
        (x + w // 2, y + h * 0.15),
        (x + w * 0.62, y + h * 0.35),
        (x + w // 2, y + h * 0.50),
        (x + w * 0.38, y + h * 0.35),
    ]
    pygame.draw.polygon(surface, (255, 160, 60), cockpit)


def draw_laser(surface, rect):
    """Draw a glowing player laser bolt with a pointed tip and fading tail."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx = x + w // 2

    # Outer glow
    glow_w, glow_h = w + 10, h + 8
    glow_surf = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf, (80, 255, 120, 35), (0, 0, glow_w, glow_h))
    surface.blit(glow_surf, (cx - glow_w // 2, y - 4))

    # Mid glow
    mid_w, mid_h = w + 4, h + 2
    mid_surf = pygame.Surface((mid_w, mid_h), pygame.SRCALPHA)
    pygame.draw.ellipse(mid_surf, (120, 255, 140, 80), (0, 0, mid_w, mid_h))
    surface.blit(mid_surf, (cx - mid_w // 2, y - 1))

    # Bright core beam
    core_w = max(2, w - 2)
    pygame.draw.rect(surface, (180, 255, 200), (cx - core_w // 2, y + 4, core_w, h - 6))

    # Hot white center line
    pygame.draw.line(surface, (240, 255, 245), (cx, y + 5), (cx, y + h - 3), 1)

    # Pointed tip
    tip = [
        (cx, y - 3),
        (cx - w // 2 - 1, y + 5),
        (cx + w // 2 + 1, y + 5),
    ]
    pygame.draw.polygon(surface, (200, 255, 220), tip)
    pygame.draw.circle(surface, (255, 255, 255), (cx, y - 1), 2)

    # Fading tail
    tail_surf = pygame.Surface((w + 4, 8), pygame.SRCALPHA)
    tail = [
        (0, 0),
        (w + 4, 0),
        ((w + 4) // 2, 8),
    ]
    pygame.draw.polygon(tail_surf, (100, 255, 130, 60), tail)
    surface.blit(tail_surf, (cx - (w + 4) // 2, y + h - 2))


def draw_enemy_laser(surface, rect):
    """Draw a red-orange enemy laser bolt (pointing downward)."""
    x, y, w, h = rect.x, rect.y, rect.w, rect.h
    cx = x + w // 2

    # Outer glow
    glow_w, glow_h = w + 10, h + 8
    glow_surf = pygame.Surface((glow_w, glow_h), pygame.SRCALPHA)
    pygame.draw.ellipse(glow_surf, (255, 60, 40, 35), (0, 0, glow_w, glow_h))
    surface.blit(glow_surf, (cx - glow_w // 2, y - 4))

    # Mid glow
    mid_w, mid_h = w + 4, h + 2
    mid_surf = pygame.Surface((mid_w, mid_h), pygame.SRCALPHA)
    pygame.draw.ellipse(mid_surf, (255, 100, 50, 80), (0, 0, mid_w, mid_h))
    surface.blit(mid_surf, (cx - mid_w // 2, y - 1))

    # Core beam
    core_w = max(2, w - 2)
    pygame.draw.rect(surface, (255, 140, 80), (cx - core_w // 2, y + 4, core_w, h - 6))

    # Hot center line
    pygame.draw.line(surface, (255, 220, 180), (cx, y + 3), (cx, y + h - 3), 1)

    # Pointed tip (bottom)
    tip = [
        (cx, y + h + 3),
        (cx - w // 2 - 1, y + h - 5),
        (cx + w // 2 + 1, y + h - 5),
    ]
    pygame.draw.polygon(surface, (255, 180, 100), tip)
    pygame.draw.circle(surface, (255, 255, 200), (cx, y + h + 1), 2)

    # Fading tail (top)
    tail_surf = pygame.Surface((w + 4, 8), pygame.SRCALPHA)
    tail = [
        ((w + 4) // 2, 0),
        (0, 8),
        (w + 4, 8),
    ]
    pygame.draw.polygon(tail_surf, (255, 80, 50, 60), tail)
    surface.blit(tail_surf, (cx - (w + 4) // 2, y - 6))


def draw_hearts(surface, lives):
    """Draw heart-shaped life indicators in the top-left corner."""
    for i in range(lives):
        hx = 15 + i * 30
        hy = 15
        pygame.draw.circle(surface, (255, 50, 70), (hx + 5, hy + 5), 6)
        pygame.draw.circle(surface, (255, 50, 70), (hx + 15, hy + 5), 6)
        pygame.draw.polygon(surface, (255, 50, 70),
                            [(hx - 1, hy + 8), (hx + 21, hy + 8), (hx + 10, hy + 20)])
