# 🚀 Space Blaster

A retro-style space shooter built with **Pygame**, featuring procedural sound effects, parallax starfield backgrounds, and a 5-stage difficulty progression system.

## Features

- **Polygon-based spaceship sprites** — player and enemies rendered as detailed vector ships
- **Procedural audio** — laser zaps, explosions, and hit sounds generated with numpy
- **5-stage difficulty progression** — background colors, enemy types, speeds, and celestial bodies change every 30 seconds
- **Parallax starfield** — three-layer scrolling stars with drifting galaxies
- **Celestial bodies** — moons, gas planets, rocky planets, ringed planets, and dark planets drift through the scene
- **Explosion particle system** — colorful particle bursts on enemy destruction and player death
- **Score system** — live counter, high-score persistence, and penalty for escaped enemies
- **Game states** — title screen, pause menu, and game-over screen with scoreboards

## Controls

| Key | Action |
|-----|--------|
| ← → | Move ship left / right |
| Space | Fire laser |
| Escape | Pause / Resume |
| R | Restart (on Game Over screen) |

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

> **Note:** `numpy` is optional — the game runs without sound effects if numpy is not installed.

## Project Structure

```
space_blaster/
├── main.py          # Entry point
├── game.py          # Game class — state, loop, update, draw
├── config.py        # Constants, stage configs, colors
├── sound.py         # Procedural sound effect generation
├── score.py         # High-score persistence (JSON)
├── particles.py     # Explosion particle system
├── background.py    # Starfield, galaxy, celestial bodies
├── renderer.py      # Ship & laser drawing functions
└── screens.py       # Title, pause, game-over UI screens
```
