"""Explosion particle system for Space Blaster."""

import math
import random

import pygame


class ParticleSystem:
    """Manages a collection of explosion particles."""

    def __init__(self):
        self._particles = []

    def spawn(self, cx, cy, color_palette, count=20, speed_range=(1, 5), lifetime=30):
        """Create a burst of particles at (cx, cy)."""
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
                'size': random.randint(2, 4),
            })

    def update_and_draw(self, surface):
        """Update particle positions and draw them; remove dead particles."""
        for p in self._particles[:]:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.05  # slight gravity
            p['life'] -= 1
            if p['life'] <= 0:
                self._particles.remove(p)
                continue
            frac = p['life'] / p['max_life']
            alpha = int(255 * frac)
            sz = max(1, int(p['size'] * frac))
            r, g, b = p['color']
            ps = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(ps, (r, g, b, alpha), (sz, sz), sz)
            surface.blit(ps, (int(p['x']) - sz, int(p['y']) - sz))

    def clear(self):
        """Remove all particles."""
        self._particles.clear()
