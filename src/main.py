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
    print(f"Loaded {len(songs)} songs.")

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

    # ── Adversarial Profiles ───────────────────────────────────────────────────
    #
    # Adversarial 1: Catalog Cliff
    # Both "hip-hop" and "confident" are isolated nodes — no close cousins, no
    # extended family, and each appears in exactly one song (Block Party Anthem).
    # After the one exact match the scorer has zero genre or mood signal for the
    # remaining 19 songs, so ranks #2-5 are decided purely by energy/valence/
    # acousticness proximity. The results look plausible but have no musical basis.
    catalog_cliff = {
        "genre": "hip-hop",
        "mood": "confident",
        "energy": 0.85,
        "likes_acoustic": False,
    }

    # Adversarial 2: Mood Override
    # Reggae appears in exactly one catalog song — Island Time (#19, mood: relaxed).
    # "relaxed" and "energetic" belong to opposite mood clusters with zero adjacency,
    # so the mood+energy weights (4.5 total) beat the genre weight (3.0), and
    # Overdrive Protocol (electronic/energetic) outscores the only reggae track.
    # The system recommends a genre the user never asked for at rank #1.
    mood_override = {
        "genre": "reggae",
        "mood": "energetic",
        "energy": 0.92,
        "likes_acoustic": False,
    }

    # Adversarial 3: Knife Edge
    # Classical music is inherently low-energy (Morning Prelude: energy=0.18, mood=
    # peaceful). The user's high energy target and energetic mood pull the score away
    # from the only classical song — while "likes_acoustic=True" pulls back toward it.
    # The forces nearly cancel: Overdrive Protocol (electronic) edges out Morning
    # Prelude (classical) by ~0.3 percentage points, burying the genre match at #2.
    knife_edge = {
        "genre": "classical",
        "mood": "energetic",
        "energy": 0.90,
        "likes_acoustic": True,
    }

    profiles = [
        ("Gym Warrior", gym_warrior),
        ("Late-Night Study Session", study_session),
        ("Late-Night Driver", late_night_driver),
        ("Soul & Warmth Seeker", acoustic_soul),
        ("Adversarial 1 - Catalog Cliff", catalog_cliff),
        ("Adversarial 2 - Mood Override", mood_override),
        ("Adversarial 3 - Knife Edge", knife_edge),
    ]

    for name, user_prefs in profiles:
        print(f"\n{'=' * 50}")
        print(f"Profile: {name}")
        print(f"{'=' * 50}")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for i, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            bar_filled = round(score * 20)
            bar = "#" * bar_filled + "-" * (20 - bar_filled)
            print(f"  #{i}  {song['title']} - {song['artist']}")
            print(f"       Score: {score * 100:.1f}%  [{bar}]")
            for reason in explanation.split("; "):
                print(f"       > {reason}")
            print()


if __name__ == "__main__":
    main()
