"""UI screens: title, pause, and game-over for Space Blaster."""

import math
import os

import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_W, BUTTON_H, FONT_PATH
from renderer import draw_player_ship


# Precomputed button rectangles
BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                          SCREEN_HEIGHT // 2 + 60, BUTTON_W, BUTTON_H)
GAME_OVER_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                                     SCREEN_HEIGHT - 130, BUTTON_W, BUTTON_H)
PAUSE_CONTINUE_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                                  SCREEN_HEIGHT // 2 - 10, BUTTON_W, BUTTON_H)
PAUSE_QUIT_RECT = pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_W // 2,
                               SCREEN_HEIGHT // 2 + 60, BUTTON_W, BUTTON_H)


def _load_font(size):
    """Load the pixel font at the given size, falling back to system font."""
    if os.path.isfile(FONT_PATH):
        return pygame.font.Font(FONT_PATH, size)
    return pygame.font.SysFont('monospace', size)


class Fonts:
    """Pixel-art font collection using Press Start 2P."""

    def __init__(self):
        self.small = _load_font(10)
        self.medium = _load_font(14)
        self.large = _load_font(24)
        self.title = _load_font(32)
        self.button = _load_font(14)
        self.score = _load_font(12)


def _draw_retro_panel(surface, rect, bg_alpha=120, border_color=(100, 120, 180)):
    """Draw a retro-styled panel with border and translucent background."""
    panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    panel.fill((10, 10, 30, bg_alpha))
    surface.blit(panel, rect.topleft)
    pygame.draw.rect(surface, border_color, rect, width=2)
    # Corner highlights
    csize = 6
    for cx, cy in [rect.topleft, (rect.right - csize, rect.top),
                   (rect.left, rect.bottom - csize), (rect.right - csize, rect.bottom - csize)]:
        pygame.draw.rect(surface, (180, 200, 255), (cx, cy, csize, csize), width=1)


def _draw_button(surface, rect, label, font, mouse_pos, color_normal, color_hover,
                 border_normal, border_hover):
    """Draw a pixel-styled button with hover effect."""
    hover = rect.collidepoint(mouse_pos)
    btn_color = color_hover if hover else color_normal
    brd_color = border_hover if hover else border_normal

    # Shadow
    shadow_rect = rect.move(3, 3)
    pygame.draw.rect(surface, (0, 0, 0, 80), shadow_rect)

    # Button body
    pygame.draw.rect(surface, btn_color, rect)
    # Inner highlight (top edge)
    r, g, b = btn_color
    highlight = (min(255, r + 60), min(255, g + 60), min(255, b + 60))
    pygame.draw.line(surface, highlight, rect.topleft, rect.topright, 2)
    # Border
    pygame.draw.rect(surface, brd_color, rect, width=2)

    text = font.render(label, True, (255, 255, 255))
    surface.blit(text, (rect.centerx - text.get_width() // 2,
                        rect.centery - text.get_height() // 2))


def _draw_text_with_shadow(surface, text_surf, x, y, shadow_offset=2):
    """Blit text with a dark drop shadow for readability."""
    shadow = text_surf.copy()
    shadow.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_MIN)
    shadow.set_alpha(120)
    surface.blit(shadow, (x + shadow_offset, y + shadow_offset))
    surface.blit(text_surf, (x, y))


def draw_title_screen(surface, fonts, high_scores, mouse_pos, title_frame, player_w, player_h):
    """Draw the title screen."""
    # Title text with glow pulse
    pulse = 0.8 + 0.2 * math.sin(title_frame * 0.04)
    title_color = (int(80 * pulse), int(180 * pulse), int(255 * pulse))

    # Title glow effect
    glow_text = fonts.title.render('SPACE BLASTER', True, (40, 100, 200))
    glow_surf = pygame.Surface((glow_text.get_width() + 8, glow_text.get_height() + 8),
                               pygame.SRCALPHA)
    glow_surf.blit(glow_text, (4, 4))
    glow_surf.set_alpha(int(60 * pulse))
    tx = SCREEN_WIDTH // 2 - glow_surf.get_width() // 2
    ty = SCREEN_HEIGHT // 5 - 10
    surface.blit(glow_surf, (tx - 2, ty - 2))
    surface.blit(glow_surf, (tx + 2, ty + 2))

    # Title text
    title_text = fonts.title.render('SPACE BLASTER', True, title_color)
    _draw_text_with_shadow(surface,
                           title_text,
                           SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                           SCREEN_HEIGHT // 5 - 10, shadow_offset=3)

    # Subtitle
    sub_text = fonts.small.render('Defend the galaxy!', True, (160, 180, 200))
    _draw_text_with_shadow(surface,
                           sub_text,
                           SCREEN_WIDTH // 2 - sub_text.get_width() // 2,
                           SCREEN_HEIGHT // 5 + 40)

    # Decorative player ship (bobbing)
    bob = math.sin(title_frame * 0.05) * 8
    draw_player_ship(surface, SCREEN_WIDTH // 2 - player_w // 2,
                     SCREEN_HEIGHT // 2 - 50 + bob, player_w, player_h)

    # START button
    _draw_button(surface, BUTTON_RECT, 'START', fonts.button, mouse_pos,
                 (20, 80, 180), (40, 120, 220), (60, 140, 230), (100, 200, 255))

    # High scores in a retro panel
    if high_scores:
        panel_w, panel_h = 280, 30 + len(high_scores) * 24
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - panel_w // 2,
                                 BUTTON_RECT.bottom + 20, panel_w, panel_h)
        _draw_retro_panel(surface, panel_rect, bg_alpha=140)

        hs_title = fonts.small.render('HIGH SCORES', True, (180, 200, 255))
        _draw_text_with_shadow(surface, hs_title,
                               SCREEN_WIDTH // 2 - hs_title.get_width() // 2,
                               panel_rect.top + 8)
        for idx, hs in enumerate(high_scores):
            color = (255, 215, 0) if idx == 0 else (200, 200, 220)
            num_text = fonts.score.render(f'{idx + 1}.', True, (120, 140, 160))
            score_text = fonts.score.render(f'{hs:,}', True, color)
            row_y = panel_rect.top + 30 + idx * 24
            surface.blit(num_text, (panel_rect.left + 20, row_y))
            surface.blit(score_text, (panel_rect.right - 20 - score_text.get_width(), row_y))


def draw_hud(surface, fonts, score, stage, lives, is_boosted=False):
    """Draw the in-game HUD: hearts, score, stage, and boost indicator."""
    from renderer import draw_hearts
    draw_hearts(surface, lives)

    score_text = fonts.score.render(f'SCORE {score:,}', True, (220, 230, 255))
    _draw_text_with_shadow(surface, score_text,
                           SCREEN_WIDTH - score_text.get_width() - 15, 12)

    stage_hud = fonts.score.render(f'STAGE {stage}', True, (180, 200, 255))
    _draw_text_with_shadow(surface, stage_hud,
                           SCREEN_WIDTH // 2 - stage_hud.get_width() // 2, 12)

    if is_boosted:
        boost_text = fonts.small.render('SPEED UP!', True, (50, 255, 50))
        # Blink effect
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            _draw_text_with_shadow(surface, boost_text,
                                   SCREEN_WIDTH // 2 - boost_text.get_width() // 2, 35)


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
        _draw_text_with_shadow(surface, ann_s,
                               SCREEN_WIDTH // 2 - ann_text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - ann_text.get_height() // 2)


def draw_pause_screen(surface, fonts, score, stage, mouse_pos):
    """Draw the pause overlay with continue/quit buttons."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    # PAUSED title
    pause_text = fonts.large.render('PAUSED', True, (220, 220, 255))
    _draw_text_with_shadow(surface, pause_text,
                           SCREEN_WIDTH // 2 - pause_text.get_width() // 2,
                           SCREEN_HEIGHT // 2 - 90)

    # Continue button
    _draw_button(surface, PAUSE_CONTINUE_RECT, 'CONTINUE', fonts.button, mouse_pos,
                 (20, 110, 70), (40, 160, 100), (40, 160, 100), (80, 220, 140))

    # Quit button
    _draw_button(surface, PAUSE_QUIT_RECT, 'QUIT', fonts.button, mouse_pos,
                 (110, 30, 30), (160, 50, 50), (160, 50, 50), (220, 80, 80))

    # Hint
    esc_hint = fonts.small.render('Press ESC to resume', True, (140, 140, 160))
    surface.blit(esc_hint, (SCREEN_WIDTH // 2 - esc_hint.get_width() // 2,
                            PAUSE_QUIT_RECT.bottom + 20))


def draw_game_over_screen(surface, fonts, score, stage, high_scores, mouse_pos):
    """Draw the game-over overlay with score, high scores, and play again button."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    # GAME OVER title
    go_text = fonts.large.render('GAME OVER', True, (255, 60, 60))
    _draw_text_with_shadow(surface, go_text,
                           SCREEN_WIDTH // 2 - go_text.get_width() // 2,
                           SCREEN_HEIGHT // 5 - 10, shadow_offset=3)

    # Stage reached
    stage_go = fonts.small.render(f'Stage {stage} reached', True, (120, 180, 255))
    _draw_text_with_shadow(surface, stage_go,
                           SCREEN_WIDTH // 2 - stage_go.get_width() // 2,
                           SCREEN_HEIGHT // 5 + 28)

    # Final score
    final_text = fonts.medium.render(f'Your Score: {score:,}', True, (255, 220, 100))
    _draw_text_with_shadow(surface, final_text,
                           SCREEN_WIDTH // 2 - final_text.get_width() // 2,
                           SCREEN_HEIGHT // 5 + 55)

    # High scores in a retro panel
    if high_scores:
        panel_w, panel_h = 320, 38 + len(high_scores) * 26
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - panel_w // 2,
                                 SCREEN_HEIGHT // 5 + 90, panel_w, panel_h)
        _draw_retro_panel(surface, panel_rect, bg_alpha=160, border_color=(120, 140, 200))

        hs_title = fonts.small.render('HIGH SCORES', True, (180, 200, 255))
        _draw_text_with_shadow(surface, hs_title,
                               SCREEN_WIDTH // 2 - hs_title.get_width() // 2,
                               panel_rect.top + 10)

        for idx, hs in enumerate(high_scores):
            is_current = (hs == score and idx == next(
                (i for i, s in enumerate(high_scores) if s == score), -1))
            if is_current:
                color = (100, 255, 100)
            elif idx == 0:
                color = (255, 215, 0)
            else:
                color = (200, 200, 220)

            num_text = fonts.score.render(f'{idx + 1}.', True, (120, 140, 160))
            score_text = fonts.score.render(f'{hs:,}', True, color)
            row_y = panel_rect.top + 34 + idx * 26

            # Highlight bar for current score
            if is_current:
                hl_rect = pygame.Rect(panel_rect.left + 4, row_y - 3,
                                      panel_rect.w - 8, 22)
                hl_surf = pygame.Surface((hl_rect.w, hl_rect.h), pygame.SRCALPHA)
                hl_surf.fill((100, 255, 100, 30))
                surface.blit(hl_surf, hl_rect.topleft)
                pygame.draw.rect(surface, (100, 255, 100), hl_rect, width=1)

            surface.blit(num_text, (panel_rect.left + 24, row_y))
            surface.blit(score_text, (panel_rect.right - 24 - score_text.get_width(), row_y))

    # Play Again button
    _draw_button(surface, GAME_OVER_BUTTON_RECT, 'PLAY AGAIN', fonts.button, mouse_pos,
                 (140, 30, 30), (200, 50, 50), (180, 50, 50), (255, 100, 80))

    hint_text = fonts.small.render('or press R', True, (160, 160, 160))
    surface.blit(hint_text, (SCREEN_WIDTH // 2 - hint_text.get_width() // 2,
                             GAME_OVER_BUTTON_RECT.bottom + 12))
