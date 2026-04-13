from src.recommender import Song, UserProfile, Recommender, load_songs, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_count():
    songs = load_songs("data/songs.csv")
    assert len(songs) == 20


def test_score_song_exact_match():
    user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True}
    song = {"genre": "lofi", "mood": "chill", "energy": 0.35, "valence": 0.50, "acousticness": 0.86}
    score, reasons = score_song(user_prefs, song)
    assert score > 0.9


def test_score_song_partial_genre_credit():
    user_prefs = {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False}
    song = {"genre": "metal", "mood": "intense", "energy": 0.9, "valence": 0.50, "acousticness": 0.06}
    score, reasons = score_song(user_prefs, song)
    # genre component should be 0.6 * 3.0 = 1.8 out of 10.0
    genre_reason = [r for r in reasons if r.startswith("genre match")][0]
    assert "+1.80" in genre_reason


def test_score_song_no_genre_match():
    user_prefs = {"genre": "classical", "mood": "peaceful", "energy": 0.2, "likes_acoustic": True}
    song = {"genre": "hip-hop", "mood": "confident", "energy": 0.88, "valence": 0.72, "acousticness": 0.08}
    score, reasons = score_song(user_prefs, song)
    genre_reason = [r for r in reasons if r.startswith("genre match")][0]
    assert "+0.00" in genre_reason


def test_recommend_songs_returns_k_results():
    songs = load_songs("data/songs.csv")
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}
    results = recommend_songs(user_prefs, songs, k=3)
    assert len(results) == 3
