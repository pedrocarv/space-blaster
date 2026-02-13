"""High-score persistence for Space Blaster."""

import json
import os

from config import MAX_HIGH_SCORES

# Score file lives next to this module
SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'highscores.json')


def load_high_scores():
    """Load high scores from JSON file. Returns a sorted list of ints."""
    try:
        with open(SCORE_FILE, 'r') as f:
            scores = json.load(f)
        return sorted(scores, reverse=True)[:MAX_HIGH_SCORES]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_high_score(new_score):
    """Add a new score to the high-scores list and persist to disk.

    Returns:
        list: Updated sorted high-score list.
    """
    scores = load_high_scores()
    scores.append(new_score)
    scores = sorted(scores, reverse=True)[:MAX_HIGH_SCORES]
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores, f)
    return scores
