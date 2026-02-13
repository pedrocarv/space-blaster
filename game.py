"""Game class — holds all state and runs the main loop for Space Blaster."""

import sys
import random

import pygame

from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, DEFAULT_BG_COLOR,
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_LIVES, INVINCIBLE_DURATION,
    BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED,
    ENEMY_WIDTH, ENEMY_HEIGHT,
    ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT, ENEMY_BULLET_SPEED,
    STAGE_CONFIGS, STAGE_DURATION,
    SCORE_PER_KILL, SCORE_PENALTY_ESCAPE,
    ENEMY_EXPLOSION_COLORS, PLAYER_EXPLOSION_COLORS,
    GALAXY_MIN_DELAY, GALAXY_MAX_DELAY,
    CELESTIAL_COOLDOWN_MIN, CELESTIAL_COOLDOWN_MAX,
)
from sound import init_sounds
from score import load_high_scores, save_high_score
from particles import ParticleSystem
from background import (
    create_star_layers, update_and_draw_stars,
    spawn_galaxy, draw_galaxy,
    spawn_celestial, draw_celestial,
)
from renderer import (
    draw_player_ship, draw_enemy_ship,
    draw_laser, draw_enemy_laser,
)
from screens import (
    Fonts, BUTTON_RECT, GAME_OVER_BUTTON_RECT, PAUSE_CONTINUE_RECT, PAUSE_QUIT_RECT,
    draw_title_screen, draw_hud, draw_stage_effects,
    draw_pause_screen, draw_game_over_screen,
)


class Game:
    """Main game class holding all mutable state."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # Sound effects
        self.laser_sound, self.explosion_sound, self.hit_sound, self.sounds_available = init_sounds()

        # Fonts
        self.fonts = Fonts()

        # Particle system
        self.particles = ParticleSystem()

        # Background
        self.star_layers = create_star_layers()
        self.galaxy = None
        self.galaxy_cooldown = random.randint(GALAXY_MIN_DELAY, GALAXY_MAX_DELAY)

        # Celestial
        self.celestial_obj = None
        self.celestial_cooldown = random.randint(CELESTIAL_COOLDOWN_MIN, CELESTIAL_COOLDOWN_MAX)

        # High scores
        self.high_scores = load_high_scores()

        # Game state
        self.state = 'TITLE'
        self.title_frame = 0

        # Player
        self.player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.player_lives = PLAYER_LIVES
        self.player_invincible = 0

        # Score & stage
        self.score = 0
        self.stage = 1
        self.stage_start_time = 0
        self.stage_flash = 0
        self.stage_announce = 0

        # Entities
        self.bullets = []
        self.enemies = []
        self.enemy_bullets = []

        # Screen shake
        self.shake_intensity = 0

        # Dynamic settings (applied from stage config)
        self.enemy_speed = STAGE_CONFIGS[0]['enemy_speed']
        self.enemy_spawn_time = STAGE_CONFIGS[0]['spawn_time']
        self.enemy_fire_chance = STAGE_CONFIGS[0]['fire_chance']
        self.enemy_timer = 0

    # ---------- Helpers ----------

    def get_stage_config(self):
        """Return the config dict for the current stage."""
        return STAGE_CONFIGS[min(self.stage - 1, len(STAGE_CONFIGS) - 1)]

    def apply_stage_config(self):
        """Apply the current stage's difficulty settings."""
        cfg = self.get_stage_config()
        self.enemy_speed = cfg['enemy_speed']
        self.enemy_spawn_time = cfg['spawn_time']
        self.enemy_fire_chance = cfg['fire_chance']

    def reset(self):
        """Reset all game state for a new round."""
        self.player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
        self.player_lives = PLAYER_LIVES
        self.player_invincible = 0
        self.score = 0
        self.stage = 1
        self.stage_flash = 0
        self.stage_announce = 0
        self.shake_intensity = 0
        self.celestial_obj = None
        self.celestial_cooldown = random.randint(CELESTIAL_COOLDOWN_MIN, CELESTIAL_COOLDOWN_MAX)
        self.apply_stage_config()
        self.bullets.clear()
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.particles.clear()
        self.stage_start_time = pygame.time.get_ticks()
        self.enemy_timer = pygame.time.get_ticks()
        self.state = 'PLAYING'

    # ---------- Event handling ----------

    def handle_events(self):
        """Process all pygame events."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.state in ('PLAYING', 'PAUSED'):
                    save_high_score(self.score)
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.state == 'TITLE':
                    if BUTTON_RECT.collidepoint(mouse_pos):
                        self.reset()
                elif self.state == 'GAME_OVER':
                    if GAME_OVER_BUTTON_RECT.collidepoint(mouse_pos):
                        self.reset()
                elif self.state == 'PAUSED':
                    if PAUSE_CONTINUE_RECT.collidepoint(mouse_pos):
                        self.state = 'PLAYING'
                    elif PAUSE_QUIT_RECT.collidepoint(mouse_pos):
                        self.high_scores = save_high_score(self.score)
                        self.state = 'TITLE'
                        self.bullets.clear()
                        self.enemies.clear()
                        self.enemy_bullets.clear()
                        self.particles.clear()

            if event.type == pygame.KEYDOWN:
                if self.state == 'PLAYING':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'PAUSED'
                    elif event.key == pygame.K_SPACE:
                        bx = self.player_x + PLAYER_WIDTH // 2 - BULLET_WIDTH // 2
                        by = self.player_y
                        self.bullets.append(pygame.Rect(bx, by, BULLET_WIDTH, BULLET_HEIGHT))
                        if self.sounds_available:
                            self.laser_sound.play()
                elif self.state == 'PAUSED':
                    if event.key == pygame.K_ESCAPE:
                        self.state = 'PLAYING'
                elif self.state == 'GAME_OVER':
                    if event.key == pygame.K_r:
                        self.reset()

    # ---------- Update ----------

    def update(self):
        """Update game logic (only when PLAYING)."""
        if self.state != 'PLAYING':
            return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.player_x < SCREEN_WIDTH - PLAYER_WIDTH:
            self.player_x += PLAYER_SPEED

        # Player bullets
        for bullet in self.bullets:
            bullet.y -= BULLET_SPEED
        self.bullets = [b for b in self.bullets if b.y > 0]

        # Enemy spawning
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_timer > self.enemy_spawn_time:
            ex = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
            self.enemies.append(pygame.Rect(ex, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT))
            self.enemy_timer = current_time

        # Enemy movement
        for enemy in self.enemies:
            enemy.y += self.enemy_speed

        # Enemy firing
        for enemy in self.enemies:
            if 0 < enemy.y < SCREEN_HEIGHT - ENEMY_HEIGHT:
                if random.random() < self.enemy_fire_chance:
                    ebx = enemy.x + ENEMY_WIDTH // 2 - ENEMY_BULLET_WIDTH // 2
                    eby = enemy.y + ENEMY_HEIGHT
                    self.enemy_bullets.append(
                        pygame.Rect(ebx, eby, ENEMY_BULLET_WIDTH, ENEMY_BULLET_HEIGHT))

        # Enemy bullet movement
        for eb in self.enemy_bullets:
            eb.y += ENEMY_BULLET_SPEED
        self.enemy_bullets = [eb for eb in self.enemy_bullets if eb.y < SCREEN_HEIGHT]

        # Player bullets vs enemies
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if bullet.colliderect(enemy):
                    ecx = enemy.x + ENEMY_WIDTH // 2
                    ecy = enemy.y + ENEMY_HEIGHT // 2
                    self.particles.spawn(ecx, ecy, ENEMY_EXPLOSION_COLORS,
                                         count=30, speed_range=(1.5, 6), lifetime=32)
                    self.shake_intensity = 6
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += SCORE_PER_KILL
                    if self.sounds_available:
                        self.explosion_sound.play()
                    break

        # Enemy bullets vs player
        if self.player_invincible > 0:
            self.player_invincible -= 1
        else:
            player_rect = pygame.Rect(self.player_x, self.player_y,
                                      PLAYER_WIDTH, PLAYER_HEIGHT)
            for eb in self.enemy_bullets[:]:
                if eb.colliderect(player_rect):
                    self.enemy_bullets.remove(eb)
                    self.player_lives -= 1
                    self.player_invincible = INVINCIBLE_DURATION
                    if self.sounds_available:
                        self.hit_sound.play()
                    pcx = self.player_x + PLAYER_WIDTH // 2
                    pcy = self.player_y + PLAYER_HEIGHT // 2
                    self.particles.spawn(pcx, pcy, PLAYER_EXPLOSION_COLORS,
                                         count=18, speed_range=(1, 4), lifetime=22)
                    self.shake_intensity = 10
                    if self.player_lives <= 0:
                        self.particles.spawn(pcx, pcy, PLAYER_EXPLOSION_COLORS,
                                             count=55, speed_range=(2, 8), lifetime=45)
                        self.shake_intensity = 18
                        self.high_scores = save_high_score(self.score)
                        self.state = 'GAME_OVER'
                    break

        # Escaped enemies — penalty
        surviving = []
        for enemy in self.enemies:
            if enemy.y >= SCREEN_HEIGHT:
                self.score = max(0, self.score - SCORE_PENALTY_ESCAPE)
            else:
                surviving.append(enemy)
        self.enemies = surviving

        # Stage progression
        if (current_time - self.stage_start_time > STAGE_DURATION
                and self.stage < len(STAGE_CONFIGS)):
            self.stage += 1
            self.stage_start_time = current_time
            self.stage_flash = 12
            self.stage_announce = 150
            self.apply_stage_config()

        if self.stage_flash > 0:
            self.stage_flash -= 1
        if self.stage_announce > 0:
            self.stage_announce -= 1

    # ---------- Draw ----------

    def draw(self):
        """Render the current frame with optional screen shake."""
        mouse_pos = pygame.mouse.get_pos()

        # Compute shake offset
        shake_x, shake_y = 0, 0
        if self.shake_intensity > 0:
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity = max(0, self.shake_intensity - 1)

        # Background
        bg = self.get_stage_config()['bg'] if self.state in ('PLAYING', 'PAUSED') else DEFAULT_BG_COLOR
        self.screen.fill(bg)

        # Stars
        update_and_draw_stars(self.screen, self.star_layers)

        # Galaxy
        if self.galaxy is not None:
            self.galaxy['y'] += self.galaxy['speed']
            self.galaxy['angle'] += 0.002
            draw_galaxy(self.screen, self.galaxy)
            if self.galaxy['y'] > SCREEN_HEIGHT + self.galaxy['radius'] * 2:
                self.galaxy = None
                self.galaxy_cooldown = random.randint(GALAXY_MIN_DELAY, GALAXY_MAX_DELAY)
        else:
            self.galaxy_cooldown -= 1
            if self.galaxy_cooldown <= 0:
                self.galaxy = spawn_galaxy()

        # Celestial bodies (during gameplay)
        if self.state in ('PLAYING', 'PAUSED'):
            if self.celestial_obj is not None:
                if self.state == 'PLAYING':
                    self.celestial_obj['y'] += self.celestial_obj['speed']
                draw_celestial(self.screen, self.celestial_obj)
                if self.celestial_obj['y'] > SCREEN_HEIGHT + 150:
                    self.celestial_obj = None
                    self.celestial_cooldown = random.randint(
                        CELESTIAL_COOLDOWN_MIN, CELESTIAL_COOLDOWN_MAX)
            else:
                if self.state == 'PLAYING':
                    self.celestial_cooldown -= 1
                    if self.celestial_cooldown <= 0:
                        self.celestial_obj = spawn_celestial(
                            self.get_stage_config()['celestial'])

        # Advance title animation counter
        self.title_frame += 1

        # State-specific drawing — gameplay uses shake offset
        if self.state == 'TITLE':
            draw_title_screen(self.screen, self.fonts, self.high_scores,
                              mouse_pos, self.title_frame, PLAYER_WIDTH, PLAYER_HEIGHT)

        elif self.state == 'PLAYING':
            # Render gameplay to buffer for shake effect
            if shake_x != 0 or shake_y != 0:
                buf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                self._draw_gameplay_to(buf, mouse_pos)
                self.screen.blit(buf, (shake_x, shake_y))
            else:
                self._draw_gameplay_to(self.screen, mouse_pos)
            draw_hud(self.screen, self.fonts, self.score, self.stage, self.player_lives)
            draw_stage_effects(self.screen, self.fonts, self.stage,
                               self.stage_flash, self.stage_announce)

        elif self.state == 'PAUSED':
            self._draw_gameplay_to(self.screen, mouse_pos)
            draw_hud(self.screen, self.fonts, self.score, self.stage, self.player_lives)
            draw_pause_screen(self.screen, self.fonts, self.score, self.stage, mouse_pos)

        elif self.state == 'GAME_OVER':
            # Still apply shake to explosion aftermath
            if shake_x != 0 or shake_y != 0:
                buf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                self.particles.update_and_draw(buf)
                self.screen.blit(buf, (shake_x, shake_y))
            else:
                self.particles.update_and_draw(self.screen)
            draw_game_over_screen(self.screen, self.fonts, self.score, self.stage,
                                  self.high_scores, mouse_pos)

        pygame.display.flip()

    def _draw_gameplay_to(self, target, mouse_pos):
        """Draw player, enemies, bullets, and explosions to a target surface."""
        cfg = self.get_stage_config()

        # Player (blink when invincible)
        if self.player_invincible == 0 or (self.player_invincible // 4) % 2 == 0:
            draw_player_ship(target, self.player_x, self.player_y,
                             PLAYER_WIDTH, PLAYER_HEIGHT)

        # Player lasers
        for bullet in self.bullets:
            draw_laser(target, bullet)

        # Enemy lasers
        for eb in self.enemy_bullets:
            draw_enemy_laser(target, eb)

        # Enemies
        for enemy in self.enemies:
            draw_enemy_ship(target, enemy.x, enemy.y, ENEMY_WIDTH, ENEMY_HEIGHT,
                            cfg['enemy_body'], cfg['enemy_wing'])

        # Explosions
        self.particles.update_and_draw(target)

    # ---------- Main loop ----------

    def run(self):
        """Run the game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
