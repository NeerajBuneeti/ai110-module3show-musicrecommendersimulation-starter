import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# =============================================================================
# ALGORITHM RECIPE
# =============================================================================
#
# OVERVIEW
# --------
# Score every song in the catalog against a user preference dict, rank by
# score descending, and return the top-k results with explanations.
# The final score is always in the range [0.0, 1.0].
#
# -----------------------------------------------------------------------------
# WEIGHTS
# -----------------------------------------------------------------------------
#
#   Feature        Weight   Rationale
#   -------------- -------- --------------------------------------------------
#   genre          3.0      Defines the entire sonic world; strongest signal
#   mood           2.5      Sets emotional intent; nearly as important as genre
#   energy         2.0      Physical feel of the track; continuous signal
#   valence        1.5      Fine-tunes emotional tone beyond mood label
#   acousticness   1.0      Texture preference; tie-breaker at similar scores
#   -------------- -------- --------------------------------------------------
#   TOTAL          10.0     Used as the normalizer for the final score
#
# -----------------------------------------------------------------------------
# SCORING RULES
# -----------------------------------------------------------------------------
#
# 1. GENRE  (weight 3.0)
#    Not binary — uses partial-credit tiers so near-miss genres still
#    contribute rather than scoring zero.
#
#    Tier            Score   Pairs
#    --------------- ------- --------------------------------------------------
#    Exact match     1.0     any genre matched exactly
#    Close cousin    0.6     rock  ↔ metal
#                            pop   ↔ indie pop
#                            synthwave ↔ electronic
#                            r&b   ↔ soul
#                            folk  ↔ country
#                            jazz  ↔ blues
#    Extended family 0.3     soul ↔ jazz ↔ blues ↔ r&b  (any pair in group)
#                            lofi ↔ ambient ↔ jazz       (any pair in group)
#    Unrelated       0.0     everything else
#
# 2. MOOD  (weight 2.5)
#    Same partial-credit tier structure as genre.
#
#    Tier     Score   Groupings
#    -------- ------- --------------------------------------------------------
#    Exact    1.0     any mood matched exactly
#    Adjacent 0.5     happy      ↔ uplifting
#                     chill      ↔ relaxed ↔ peaceful   (any pair in group)
#                     intense    ↔ angry   ↔ energetic  (any pair in group)
#                     focused    ↔ chill
#                     moody      ↔ melancholic ↔ sad    (any pair in group)
#    Distant  0.2     happy ↔ focused
#                     chill ↔ moody
#    Unrelated 0.0    everything else
#
# 3. ENERGY  (weight 2.0)
#    Continuous proximity formula — rewards closeness to the user's target.
#
#      energy_score = 1.0 - abs(user_prefs["energy"] - song["energy"])
#
#    Range: [0.0, 1.0]. A perfect energy match → 1.0; opposite end → 0.02.
#
# 4. VALENCE  (weight 1.5)
#    Same proximity formula as energy.
#
#      valence_score = 1.0 - abs(user_prefs["valence"] - song["valence"])
#
#    Note: user_prefs may omit "valence"; default to 0.5 (neutral) if absent.
#
# 5. ACOUSTICNESS  (weight 1.0)
#    Directional preference — the user either wants acoustic texture or not.
#
#      if user_prefs["likes_acoustic"] is True:
#          acousticness_score = song["acousticness"]        # higher = better
#      else:
#          acousticness_score = 1.0 - song["acousticness"]  # lower = better
#
# -----------------------------------------------------------------------------
# FINAL SCORE
# -----------------------------------------------------------------------------
#
#   raw = (genre_score      * 3.0
#        + mood_score       * 2.5
#        + energy_score     * 2.0
#        + valence_score    * 1.5
#        + acousticness_score * 1.0)
#
#   final_score = raw / 10.0    # normalized to [0.0, 1.0]
#
# Songs are sorted by final_score descending; the top-k are returned as
# (song_dict, final_score, explanation_string) tuples.
#
# =============================================================================


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song = {}
            for key, value in row.items():
                if key == "id":
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
