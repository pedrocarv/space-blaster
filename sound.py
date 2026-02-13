"""Procedural sound effect generation for Space Blaster."""

import pygame


def init_sounds():
    """Generate all game sounds using numpy.

    Returns:
        tuple: (laser_sound, explosion_sound, hit_sound, sounds_available)
    """
    try:
        import numpy as np

        SAMPLE_RATE = 44100

        def _make_sound(samples_array):
            """Convert a float64 numpy array (-1..1) into a pygame Sound."""
            samples_array = np.clip(samples_array, -1.0, 1.0)
            pcm = (samples_array * 32767).astype(np.int16)
            stereo = np.column_stack((pcm, pcm))
            return pygame.sndarray.make_sound(stereo)

        # Laser zap: short descending sine sweep with harmonics
        dur_laser = 0.15
        t_l = np.linspace(0, dur_laser, int(SAMPLE_RATE * dur_laser), endpoint=False)
        freq_start, freq_end = 1800, 400
        freq_sweep = freq_start + (freq_end - freq_start) * (t_l / dur_laser)
        phase = 2 * np.pi * np.cumsum(freq_sweep) / SAMPLE_RATE
        laser_wave = 0.45 * np.sin(phase) + 0.15 * np.sin(phase * 2)
        env = np.exp(-t_l * 18)
        laser_wave *= env
        laser_sound = _make_sound(laser_wave)
        laser_sound.set_volume(0.35)

        # Explosion: burst of shaped noise with a low thump
        dur_exp = 0.35
        t_e = np.linspace(0, dur_exp, int(SAMPLE_RATE * dur_exp), endpoint=False)
        noise = np.random.uniform(-1, 1, len(t_e))
        thump = 0.6 * np.sin(2 * np.pi * 60 * t_e) * np.exp(-t_e * 12)
        noise_env = np.exp(-t_e * 8)
        explosion_wave = 0.5 * noise * noise_env + thump
        explosion_sound = _make_sound(explosion_wave)
        explosion_sound.set_volume(0.4)

        # Player hit: short harsh buzz
        dur_hit = 0.25
        t_h = np.linspace(0, dur_hit, int(SAMPLE_RATE * dur_hit), endpoint=False)
        hit_wave = 0.5 * np.sign(np.sin(2 * np.pi * 150 * t_h))
        hit_wave *= np.exp(-t_h * 10)
        hit_sound = _make_sound(hit_wave)
        hit_sound.set_volume(0.3)

        return laser_sound, explosion_sound, hit_sound, True

    except ImportError:
        print("Note: numpy not found — running without sound effects.")
        return None, None, None, False
