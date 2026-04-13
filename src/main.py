"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    # ── User Profiles ──────────────────────────────────────────────────────────
    #
    # Profile 1: Gym Warrior
    # Wants maximum aggression and energy — genre metal, mood angry, energy 0.95,
    # strongly anti-acoustic (produced, distorted sound). This is the hard ceiling
    # of the catalog's intensity axis. Should score Iron Curtain (#16) and
    # Overdrive Protocol (#15) near the top, and rank Morning Prelude (#13) or
    # Library Rain (#4) near zero — making it a useful stress test for the scorer.
    gym_warrior = {
        "genre": "metal",
        "mood": "angry",
        "energy": 0.95,
        "likes_acoustic": False,
    }

    # Profile 2: Late-Night Study Session
    # Low-energy lofi listener seeking calm, acoustic-textured focus music.
    # Polar opposite of gym_warrior: genre lofi, mood chill, energy 0.38, acoustic.
    # Should strongly favor Library Rain (#4), Midnight Coding (#2), Focus Flow (#9),
    # and Spacewalk Thoughts (#6). Any high-energy or metal track should bottom out.
    study_session = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.38,
        "likes_acoustic": True,
    }

    # Profile 3: Late-Night Driver
    # Mid-to-high energy synthwave listener in a moody headspace — not aggressive,
    # but definitely not relaxed. Genre synthwave, mood moody, energy 0.75,
    # non-acoustic (electronic texture preferred). Should favor Night Drive Loop (#8)
    # and Overdrive Protocol (#15), while scoring classical and folk near zero.
    # This profile tests whether the recommender distinguishes "moody + produced"
    # from both the intense and the chill extremes.
    late_night_driver = {
        "genre": "synthwave",
        "mood": "moody",
        "energy": 0.75,
        "likes_acoustic": False,
    }

    # Profile 4: Soul & Warmth Seeker
    # Mid-energy soul/r&b listener drawn to emotional, uplifting, acoustic-textured
    # music. Genre soul, mood uplifting, energy 0.62, acoustic. Sits in the middle
    # of the energy range but occupies a completely different genre/mood corner than
    # any other profile. Should favor Rise Together (#18), Velvet Nights (#12), and
    # Coffee Shop Stories (#7). Metal and EDM should score near zero. Demonstrates
    # that genre and mood weights matter more than energy alone.
    acoustic_soul = {
        "genre": "soul",
        "mood": "uplifting",
        "energy": 0.62,
        "likes_acoustic": True,
    }

    profiles = [
        ("Gym Warrior", gym_warrior),
        ("Late-Night Study Session", study_session),
        ("Late-Night Driver", late_night_driver),
        ("Soul & Warmth Seeker", acoustic_soul),
    ]

    for name, user_prefs in profiles:
        print(f"\n{'=' * 50}")
        print(f"Profile: {name}")
        print(f"{'=' * 50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rec in recommendations:
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
