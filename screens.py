"""UI screens: title, pause, and game-over for Space Blaster."""

import math

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_W, BUTTON_H
from renderer import draw_player_ship


# Precomputed button rectangles
BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                          SCREEN_HEIGHT // 2 + 60, BUTTON_W, BUTTON_H)
PAUSE_CONTINUE_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                                  SCREEN_HEIGHT // 2 - 10, BUTTON_W, BUTTON_H)
PAUSE_QUIT_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                               SCREEN_HEIGHT // 2 + 60, BUTTON_W, BUTTON_H)


class Fonts:
    """Lazy-loaded font collection."""

    def __init__(self):
        self.small = pygame.font.SysFont(None, 32)
        self.medium = pygame.font.SysFont(None, 40)
        self.large = pygame.font.SysFont(None, 72)
        self.title = pygame.font.SysFont(None, 96)
        self.button = pygame.font.SysFont(None, 48)
        self.score = pygame.font.SysFont(None, 36)


def _draw_button(surface, rect, label, font, mouse_pos, color_normal, color_hover,
                 border_normal, border_hover):
    """Draw a rounded button with hover effect."""
    hover = rect.collidepoint(mouse_pos)
    btn_color = color_hover if hover else color_normal
    brd_color = border_hover if hover else border_normal
    pygame.draw.rect(surface, btn_color, rect, border_radius=10)
    pygame.draw.rect(surface, brd_color, rect, width=2, border_radius=10)
    text = font.render(label, True, (255, 255, 255))
    surface.blit(text, (rect.centerx - text.get_width() // 2,
                        rect.centery - text.get_height() // 2))


def draw_title_screen(surface, fonts, high_scores, mouse_pos, title_frame, player_w, player_h):
    """Draw the title screen."""
    # Title text with subtle glow pulse
    pulse = 0.8 + 0.2 * math.sin(title_frame * 0.04)
    title_color = (int(60 * pulse), int(180 * pulse), int(255 * pulse))
    title_text = fonts.title.render('SPACE BLASTER', True, title_color)
    surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                              SCREEN_HEIGHT // 4 - 30))

    # Subtitle
    sub_text = fonts.small.render('Defend the galaxy!', True, (160, 180, 200))
    surface.blit(sub_text, (SCREEN_WIDTH // 2 - sub_text.get_width() // 2,
                            SCREEN_HEIGHT // 4 + 50))

    # Decorative player ship (slowly bobbing)
    bob = math.sin(title_frame * 0.05) * 8
    draw_player_ship(surface, SCREEN_WIDTH // 2 - player_w // 2,
                     SCREEN_HEIGHT // 2 - 40 + bob, player_w, player_h)

    # START button
    _draw_button(surface, BUTTON_RECT, 'START', fonts.button, mouse_pos,
                 (20, 100, 200), (40, 160, 255), (50, 140, 230), (100, 200, 255))

    # High scores
    if high_scores:
        hs_title = fonts.small.render('HIGH SCORES', True, (180, 200, 255))
        surface.blit(hs_title, (SCREEN_WIDTH // 2 - hs_title.get_width() // 2,
                                BUTTON_RECT.bottom + 30))
        for idx, hs in enumerate(high_scores):
            color = (255, 215, 0) if idx == 0 else (200, 200, 220)
            entry = fonts.score.render(f'{idx + 1}. {hs:,}', True, color)
            surface.blit(entry, (SCREEN_WIDTH // 2 - entry.get_width() // 2,
                                 BUTTON_RECT.bottom + 58 + idx * 28))


def draw_hud(surface, fonts, score, stage, lives):
    """Draw the in-game HUD: hearts, score, and stage indicator."""
    from renderer import draw_hearts
    draw_hearts(surface, lives)

    score_text = fonts.score.render(f'SCORE  {score:,}', True, (220, 230, 255))
    surface.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 15, 12))

    stage_hud = fonts.score.render(f'STAGE {stage}', True, (180, 200, 255))
    surface.blit(stage_hud, (SCREEN_WIDTH // 2 - stage_hud.get_width() // 2, 12))


def draw_stage_effects(surface, fonts, stage, stage_flash, stage_announce):
    """Draw stage transition flash and announcement."""
    if stage_flash > 0:
        flash_s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        flash_s.fill((255, 255, 255, int(180 * (stage_flash / 12))))
        surface.blit(flash_s, (0, 0))

    if stage_announce > 0:
        ann_alpha = min(255, stage_announce * 4)
        ann_text = fonts.large.render(f'STAGE {stage}', True, (255, 255, 100))
        ann_s = pygame.Surface(ann_text.get_size(), pygame.SRCALPHA)
        ann_s.blit(ann_text, (0, 0))
        ann_s.set_alpha(ann_alpha)
        surface.blit(ann_s, (SCREEN_WIDTH // 2 - ann_text.get_width() // 2,
                             SCREEN_HEIGHT // 2 - ann_text.get_height() // 2))


def draw_pause_screen(surface, fonts, score, stage, mouse_pos):
    """Draw the pause overlay with continue/quit buttons."""
    # Dark overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    # PAUSED title
    pause_text = fonts.large.render('PAUSED', True, (220, 220, 255))
    surface.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                              SCREEN_HEIGHT // 2 - 90))

    # Continue button
    _draw_button(surface, PAUSE_CONTINUE_RECT, 'CONTINUE', fonts.button, mouse_pos,
                 (20, 110, 70), (40, 160, 100), (40, 160, 100), (80, 220, 140))

    # Quit button
    _draw_button(surface, PAUSE_QUIT_RECT, 'QUIT', fonts.button, mouse_pos,
                 (110, 30, 30), (160, 50, 50), (160, 50, 50), (220, 80, 80))

    # Hint
    esc_hint = fonts.small.render('Press ESC to resume', True, (140, 140, 160))
    surface.blit(esc_hint, (SCREEN_WIDTH // 2 - esc_hint.get_width() // 2,
                            PAUSE_QUIT_RECT.bottom + 15))


def draw_game_over_screen(surface, fonts, score, stage, high_scores, mouse_pos):
    """Draw the game-over overlay with score, high scores, and play again button."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    go_text = fonts.large.render('GAME OVER', True, (255, 60, 60))
    surface.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2,
                           SCREEN_HEIGHT // 4 - 20))

    # Stage reached
    stage_go = fonts.small.render(f'Stage {stage} reached', True, (180, 200, 255))
    surface.blit(stage_go, (SCREEN_WIDTH // 2 - stage_go.get_width() // 2,
                            SCREEN_HEIGHT // 4 + 25))

    # Final score
    final_score_text = fonts.medium.render(f'Your Score: {score:,}', True, (255, 220, 100))
    surface.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2,
                                    SCREEN_HEIGHT // 4 + 50))

    # High scores table
    if high_scores:
        hs_title = fonts.small.render('HIGH SCORES', True, (180, 200, 255))
        surface.blit(hs_title, (SCREEN_WIDTH // 2 - hs_title.get_width() // 2,
                                SCREEN_HEIGHT // 4 + 90))
        for idx, hs in enumerate(high_scores):
            is_current = (hs == score and idx == next(
                (i for i, s in enumerate(high_scores) if s == score), -1))
            if is_current:
                color = (100, 255, 100)
            elif idx == 0:
                color = (255, 215, 0)
            else:
                color = (200, 200, 220)
            entry = fonts.score.render(f'{idx + 1}. {hs:,}', True, color)
            surface.blit(entry, (SCREEN_WIDTH // 2 - entry.get_width() // 2,
                                 SCREEN_HEIGHT // 4 + 118 + idx * 28))

    # Play Again button
    _draw_button(surface, BUTTON_RECT, 'PLAY AGAIN', fonts.button, mouse_pos,
                 (140, 30, 30), (200, 50, 50), (180, 50, 50), (255, 100, 80))

    hint_text = fonts.small.render('or press R', True, (160, 160, 160))
    surface.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2,
                             BUTTON_RECT.bottom + 12))
