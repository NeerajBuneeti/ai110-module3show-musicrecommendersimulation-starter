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
    reasons = []

    # --- Genre (weight 3.0) ---
    GENRE_CLOSE_COUSINS = [
        {"rock", "metal"},
        {"pop", "indie pop"},
        {"synthwave", "electronic"},
        {"r&b", "soul"},
        {"folk", "country"},
        {"jazz", "blues"},
    ]
    GENRE_EXTENDED_FAMILIES = [
        {"soul", "jazz", "blues", "r&b"},
        {"lofi", "ambient", "jazz"},
    ]

    user_genre = user_prefs.get("genre", "").lower()
    song_genre = song.get("genre", "").lower()

    if user_genre == song_genre:
        genre_score = 1.0
    elif any(user_genre in pair and song_genre in pair for pair in GENRE_CLOSE_COUSINS):
        genre_score = 0.6
    elif any(user_genre in group and song_genre in group for group in GENRE_EXTENDED_FAMILIES):
        genre_score = 0.3
    else:
        genre_score = 0.0

    genre_weighted = genre_score * 3.0
    reasons.append(f"genre match: {user_genre} -> {song_genre} (+{genre_weighted:.2f})")

    # --- Mood (weight 2.5) ---
    MOOD_ADJACENT = [
        {"happy", "uplifting"},
        {"chill", "relaxed", "peaceful"},
        {"intense", "angry", "energetic"},
        {"focused", "chill"},
        {"moody", "melancholic", "sad"},
    ]
    MOOD_DISTANT = [
        {"happy", "focused"},
        {"chill", "moody"},
    ]

    user_mood = user_prefs.get("mood", "").lower()
    song_mood = song.get("mood", "").lower()

    if user_mood == song_mood:
        mood_score = 1.0
    elif any(user_mood in group and song_mood in group for group in MOOD_ADJACENT):
        mood_score = 0.5
    elif any(user_mood in pair and song_mood in pair for pair in MOOD_DISTANT):
        mood_score = 0.2
    else:
        mood_score = 0.0

    mood_weighted = mood_score * 2.5
    reasons.append(f"mood match: {user_mood} -> {song_mood} (+{mood_weighted:.2f})")

    # --- Energy (weight 2.0) ---
    user_energy = user_prefs["energy"]
    song_energy = song["energy"]
    energy_diff = abs(user_energy - song_energy)
    energy_score = 1.0 - energy_diff
    energy_weighted = energy_score * 2.0
    reasons.append(f"energy proximity: |{user_energy} - {song_energy}| = {energy_diff:.2f} (+{energy_weighted:.2f})")

    # --- Valence (weight 1.5) ---
    user_valence = user_prefs.get("target_valence", 0.5)
    song_valence = song["valence"]
    valence_diff = abs(user_valence - song_valence)
    valence_score = 1.0 - valence_diff
    valence_weighted = valence_score * 1.5
    reasons.append(f"valence proximity: |{user_valence} - {song_valence}| = {valence_diff:.2f} (+{valence_weighted:.2f})")

    # --- Acousticness (weight 1.0) ---
    song_acousticness = song["acousticness"]
    if user_prefs["likes_acoustic"]:
        acousticness_score = song_acousticness
        acoustic_label = "likes acoustic"
    else:
        acousticness_score = 1.0 - song_acousticness
        acoustic_label = "dislikes acoustic"
    acousticness_weighted = acousticness_score * 1.0
    reasons.append(f"acousticness: {acoustic_label}, song={song_acousticness:.2f} (+{acousticness_weighted:.2f})")

    # --- Final score (normalize by total weight 10.0) ---
    raw = genre_weighted + mood_weighted + energy_weighted + valence_weighted + acousticness_weighted
    score = raw / 10.0

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
