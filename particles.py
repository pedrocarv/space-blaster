"""Enhanced explosion particle system for Space Blaster.

Features multiple particle types: circular particles, spark trails,
debris chunks, smoke puffs, and expanding shockwave rings.
"""

import math
import random

import pygame


class ParticleSystem:
    """Manages explosions with multiple visual effect types."""

    def __init__(self):
        self._particles = []
        self._shockwaves = []
        self._sparks = []
        self._debris = []
        self._smoke = []

    def spawn(self, cx, cy, color_palette, count=20, speed_range=(1, 5), lifetime=30):
        """Create a dramatic explosion burst with multiple effect layers."""
        # Core circular particles
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(*speed_range)
            color = random.choice(color_palette)
            self._particles.append({
                'x': float(cx), 'y': float(cy),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': lifetime,
                'max_life': lifetime,
                'color': color,
                'size': random.randint(2, 5),
            })

        # Spark trails (fast, thin lines)
        spark_count = count // 2
        for _ in range(spark_count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(speed_range[1] * 0.8, speed_range[1] * 2.0)
            color = random.choice(color_palette)
            # Brighten sparks
            bright = tuple(min(255, c + 80) for c in color)
            self._sparks.append({
                'x': float(cx), 'y': float(cy),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'prev_x': float(cx), 'prev_y': float(cy),
                'life': int(lifetime * 0.6),
                'max_life': int(lifetime * 0.6),
                'color': bright,
            })

        # Debris chunks (slower, tumbling squares)
        debris_count = max(3, count // 4)
        for _ in range(debris_count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(speed_range[0] * 0.5, speed_range[1] * 0.7)
            color = random.choice(color_palette)
            dark = tuple(max(0, c - 60) for c in color)
            self._debris.append({
                'x': float(cx), 'y': float(cy),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': int(lifetime * 1.2),
                'max_life': int(lifetime * 1.2),
                'color': dark,
                'size': random.randint(3, 6),
                'rot': random.uniform(0, math.pi * 2),
                'rot_speed': random.uniform(-0.2, 0.2),
            })

        # Smoke puffs (slow, expanding circles)
        smoke_count = max(2, count // 5)
        for _ in range(smoke_count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.2, 0.8)
            self._smoke.append({
                'x': float(cx) + random.uniform(-5, 5),
                'y': float(cy) + random.uniform(-5, 5),
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed - 0.3,
                'life': int(lifetime * 1.5),
                'max_life': int(lifetime * 1.5),
                'size': random.randint(6, 14),
            })

        # Shockwave ring
        self._shockwaves.append({
            'x': float(cx), 'y': float(cy),
            'radius': 4.0,
            'max_radius': 30.0 + count * 0.8,
            'life': 18,
            'max_life': 18,
            'color': random.choice(color_palette),
        })

    def update_and_draw(self, surface):
        """Update and draw all particle types."""
        self._update_smoke(surface)
        self._update_shockwaves(surface)
        self._update_particles(surface)
        self._update_debris(surface)
        self._update_sparks(surface)

    def _update_particles(self, surface):
        alive = []
        for p in self._particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.06  # gravity
            p['vx'] *= 0.98  # drag
            p['life'] -= 1
            if p['life'] <= 0:
                continue
            frac = p['life'] / p['max_life']
            alpha = int(255 * frac)
            sz = max(1, int(p['size'] * frac))
            r, g, b = p['color']
            ps = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (r, g, b, alpha), (sz, sz), sz)
            # Bright core
            if sz > 1:
                pygame.draw.circle(ps, (min(255, r + 100), min(255, g + 100),
                                        min(255, b + 100), alpha // 2),
                                   (sz, sz), max(1, sz // 2))
            surface.blit(ps, (int(p['x']) - sz, int(p['y']) - sz))
            alive.append(p)
        self._particles = alive

    def _update_sparks(self, surface):
        alive = []
        for s in self._sparks:
            s['prev_x'] = s['x']
            s['prev_y'] = s['y']
            s['x'] += s['vx']
            s['y'] += s['vy']
            s['vy'] += 0.08
            s['vx'] *= 0.96
            s['life'] -= 1
            if s['life'] <= 0:
                continue
            frac = s['life'] / s['max_life']
            alpha = int(255 * frac)
            r, g, b = s['color']
            # Draw a short line from previous to current position
            pygame.draw.line(surface, (r, g, b, 200),
                             (int(s['prev_x']), int(s['prev_y'])),
                             (int(s['x']), int(s['y'])), max(1, int(2 * frac)))
            # Bright tip
            ts = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(ts, (255, 255, 255, alpha), (2, 2), max(1, int(2 * frac)))
            surface.blit(ts, (int(s['x']) - 2, int(s['y']) - 2))
            alive.append(s)
        self._sparks = alive

    def _update_debris(self, surface):
        alive = []
        for d in self._debris:
            d['x'] += d['vx']
            d['y'] += d['vy']
            d['vy'] += 0.1  # heavier gravity
            d['rot'] += d['rot_speed']
            d['life'] -= 1
            if d['life'] <= 0:
                continue
            frac = d['life'] / d['max_life']
            alpha = int(200 * frac)
            sz = max(2, int(d['size'] * (0.5 + 0.5 * frac)))
            r, g, b = d['color']

            # Rotating square
            ds = pygame.Surface((sz * 3, sz * 3), pygame.SRCALPHA)
            cx_d, cy_d = sz * 3 // 2, sz * 3 // 2
            cos_a = math.cos(d['rot'])
            sin_a = math.sin(d['rot'])
            corners = []
            for dx, dy in [(-sz, -sz), (sz, -sz), (sz, sz), (-sz, sz)]:
                rx = cx_d + dx * cos_a - dy * sin_a
                ry = cy_d + dx * sin_a + dy * cos_a
                corners.append((rx, ry))
            pygame.draw.polygon(ds, (r, g, b, alpha), corners)
            # Edge highlight
            pygame.draw.polygon(ds, (min(255, r + 40), min(255, g + 40),
                                     min(255, b + 40), alpha // 2), corners, width=1)
            surface.blit(ds, (int(d['x']) - sz * 3 // 2, int(d['y']) - sz * 3 // 2))
            alive.append(d)
        self._debris = alive

    def _update_smoke(self, surface):
        alive = []
        for s in self._smoke:
            s['x'] += s['vx']
            s['y'] += s['vy']
            s['vy'] -= 0.01  # float upward
            s['size'] += 0.3  # expand
            s['life'] -= 1
            if s['life'] <= 0:
                continue
            frac = s['life'] / s['max_life']
            alpha = int(60 * frac)
            sz = int(s['size'])
            ss = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(ss, (80, 80, 80, alpha), (sz, sz), sz)
            surface.blit(ss, (int(s['x']) - sz, int(s['y']) - sz))
            alive.append(s)
        self._smoke = alive

    def _update_shockwaves(self, surface):
        alive = []
        for w in self._shockwaves:
            w['life'] -= 1
            if w['life'] <= 0:
                continue
            frac = w['life'] / w['max_life']
            w['radius'] += (w['max_radius'] - w['radius']) * 0.2

            r, g, b = w['color']
            alpha = int(120 * frac)
            rad = int(w['radius'])
            if rad > 2:
                ws = pygame.Surface((rad * 2 + 4, rad * 2 + 4), pygame.SRCALPHA)
                center = rad + 2
                # Outer ring
                pygame.draw.circle(ws, (r, g, b, alpha), (center, center), rad, width=2)
                # Inner bright ring
                if rad > 5:
                    pygame.draw.circle(ws, (min(255, r + 80), min(255, g + 80),
                                            min(255, b + 80), alpha // 2),
                                       (center, center), max(1, rad - 3), width=1)
                surface.blit(ws, (int(w['x']) - center, int(w['y']) - center))
            alive.append(w)
        self._shockwaves = alive

    def clear(self):
        """Remove all effects."""
        self._particles.clear()
        self._shockwaves.clear()
        self._sparks.clear()
        self._debris.clear()
        self._smoke.clear()
