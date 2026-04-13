# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a classroom simulation, not a production recommender. It is designed to show how a content-based scoring system turns structured song data and a user preference profile into a ranked list of suggestions. The system assumes the user can describe what they want in four fields — a preferred genre, a mood, a target energy level, and whether they like acoustic or produced sounds — and it treats those as fixed inputs rather than learning from behavior over time. It is intended for students exploring how recommender systems work under the hood, not for real listeners who expect the nuance of something like Spotify or Apple Music.

---

## 3. How the Model Works

Every song in the catalog gets a score between 0 and 1 based on how closely it matches the user's stated preferences. The score is built from five ingredients: genre match, mood match, energy closeness, valence closeness, and a texture preference for acoustic vs produced sound. Genre and mood are not treated as binary yes-or-no — they use a tiered partial credit system. An exact genre match scores full credit, a close neighbor like rock and metal scores partial credit, and a more distant relative scores a small amount. Mood works the same way: chill and relaxed are adjacent and share partial credit, while chill and moody are only distantly related and share less. Energy and valence are scored by proximity — the closer the song's value is to what the user asked for, the higher the score. Acousticness is directional: if the user likes acoustic sounds, songs with high acousticness score better; if they prefer produced sounds, the scoring flips. Each ingredient is multiplied by a weight that reflects how important it is — genre carries the most weight, then mood, then energy, then valence, then acousticness. The five weighted scores are added up and divided by the total possible weight to produce a final percentage. Songs are sorted by that percentage and the top five are returned with a plain-language breakdown of what drove each score.

---

## 4. Data

The catalog contains 20 songs across 17 genres and 15 moods. The original starter catalog had 10 songs focused on a handful of genres — pop, lofi, rock, ambient, jazz, synthwave, and indie pop. I expanded it by adding 10 songs covering genres that were completely absent: hip-hop, r&b, classical, country, electronic, metal, folk, soul, reggae, and blues. I also added moods that had no representation: confident, romantic, peaceful, nostalgic, energetic, angry, melancholic, uplifting, and sad. Each song has ten attributes: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. Despite the expansion, the catalog is still very small and unevenly distributed. Some genres like lofi have three songs while others like classical, reggae, and synthwave have only one each. Songs with rare moods like confident or nostalgic are also singletons with no catalog neighbors, which limits the system's ability to serve users who prefer them.

---

## 5. Strengths

The system works best when the user's genre and mood are well represented in the catalog. Profiles like Gym Warrior (metal/angry) and Late-Night Study Session (lofi/chill) both scored above 96% for their top result, and the top several recommendations felt genuinely appropriate. The tiered partial credit for genre and mood neighborhoods is one of the better design choices — it means a lofi listener gets Spacewalk Thoughts as a reasonable ambient suggestion rather than the system hard-cutting at the genre boundary. The scoring is also fully transparent: every result shows exactly how much each feature contributed, which makes it easy to understand why something ranked where it did. For users whose preferences align with a well-populated corner of the catalog, VibeFinder behaves like a sensible, explainable recommender.

---

## 6. Limitations and Bias

Three specific biases surfaced during testing. First, the valence feature carries a weight of 1.5 but is effectively wasted in every profile tested, because none of the user preference dicts include a `target_valence` key and the scorer silently defaults to 0.5. This gives an unearned advantage to any song whose valence happens to sit near the middle of the scale — Overdrive Protocol (valence 0.66) benefits from this every time it appears in results, regardless of what the user actually asked for. Second, the moods `confident`, `nostalgic`, and `romantic` exist as isolated nodes with zero adjacency connections in the mood neighborhood map, which means the songs carrying those moods — Block Party Anthem, Dust Road Memory, and Velvet Nights — score 0.0 on mood for every user who did not ask for them exactly; they can only surface by coincidence through energy and acousticness proximity, which has nothing to do with why a listener would want them. Third, Overdrive Protocol acts as a free rider throughout the catalog: its energy of 0.95 sits at the ceiling, its acousticness of 0.04 sits at the produced-sound floor, and its valence of 0.66 is close enough to the default 0.5 to collect partial valence credit — this combination lets it accumulate enough continuous-feature points to appear in the top five for profiles that asked for reggae, classical, or soul, none of which have any genre or mood connection to electronic music. Together these three biases mean the system silently rewards songs that happen to fit the scoring machinery's blind spots rather than the user's actual taste.

---

## 7. Evaluation

Seven profiles were tested in total: four standard listeners (Gym Warrior: metal/angry/0.95 energy, Late-Night Study Session: lofi/chill/0.38, Late-Night Driver: synthwave/moody/0.75, Soul & Warmth Seeker: soul/uplifting/0.62) and three adversarial cases designed to stress-test the scoring (Catalog Cliff: hip-hop/confident with no neighborhood connections; Mood Override: reggae/energetic where the only reggae song has an opposing mood; Knife Edge: classical/energetic where contradictory preferences nearly cancel). The standard profiles all produced sensible rank-1 results with scores above 88%, confirming that the scorer works when genre and mood signals are strong. The adversarial profiles revealed real failures: Mood Override caused the system to recommend an electronic track to a reggae fan at rank 1 (66.6%) while the only reggae song placed second (56.7%), and Knife Edge produced a 0.3-percentage-point margin where an electronic track edged out the only classical song despite scoring zero on genre. A weight experiment was also run: genre weight was halved from 3.0 to 1.5, energy weight was doubled from 2.0 to 4.0, and the normalizer was updated to 11.0. No rank-1 result changed for any of the seven profiles, but the adversarial failures worsened — the Mood Override winner's score rose from 66.6% to 78.2% and the Knife Edge margin widened from 0.3 points to roughly 12 points. The most surprising finding was that the adversarial failures are not caused by bad weight calibration: they stem from catalog sparsity and isolated mood nodes, and no weight adjustment fixes them without also degrading the standard profiles.

---

## 8. Future Work

The most impactful near-term improvement would be adding adjacency connections for the orphaned moods. Linking `confident` to `energetic` and `uplifting`, `nostalgic` to `melancholic` and `sad`, and `romantic` to `uplifting` and `peaceful` would immediately fix the Catalog Cliff failure mode and let those songs surface for users whose taste sits near them. A close second would be letting users specify a `target_valence` in their profile — right now the 1.5 valence weight is essentially dead weight because every profile defaults to 0.5, and actually using it would both reduce the free-rider advantage for mid-valence songs and make the scoring more personalized. Beyond fixing the current gaps, it would be interesting to add a diversity penalty so the top-five results are forced to span at least two different genres, which would reduce the filter bubble effect where one genre dominates all five slots. Finally, replacing the hardcoded genre and mood tiers with a learned similarity matrix — even just a small one built from the 20-song catalog using feature distances — would let the neighborhood relationships emerge from the data rather than requiring manual curation every time a new genre is added.

---

## 9. Personal Reflection

**Biggest learning moment**

The weight experiment was the most clarifying thing I did in this project. I expected that halving genre and doubling energy would produce noticeably different results, but every rank-1 winner stayed exactly the same. That forced me to understand that the standard profiles were not passing because of careful weight design — they were passing because the catalog happened to have exactly the right song in the right genre, so almost any weights would produce the same answer. The adversarial profiles were the ones that actually tested the model, and tuning weights did nothing to help them.

**How AI tools helped and when I had to double check them**

Claude helped me move fast in ways that would have taken hours manually — generating realistic song data for 10 new catalog entries, drafting the genre and mood neighborhood maps, and running the adversarial profiles through the scorer to verify scores before I wrote about them. Where I had to be more careful was in the analysis. When I ran the Knife Edge profile and saw Overdrive Protocol at 57.0% beating Morning Prelude at 56.7%, I initially thought the scorer had a bug. I had to trace through the score breakdown line by line to confirm the math was right and the issue was structural. AI tools surface results quickly but they don't tell you whether those results mean what you think they mean.

**What surprised me about how simple algorithms can still feel like recommendations**

I was surprised by how convincing the output felt for the well-matched profiles. When the Late-Night Driver profile returned Night Drive Loop at 97.6% with a full breakdown of exactly why each feature contributed, it genuinely looked like a smart recommendation — even though the underlying logic is just arithmetic. The explanation format did a lot of that work. Seeing `genre match: synthwave -> synthwave (+3.00)` next to the score made the system feel intentional and accountable in a way that a bare percentage score would not. A lot of what makes a recommendation feel trustworthy is not the algorithm itself but how the result is presented.

**What I would try next**

The thing I want to try most is replacing the static preference profile with something dynamic — even just a simple session model where the user's preferences shift slightly each time they accept or skip a recommendation. The current system is stateless: it gives the same answer every time you ask with the same inputs. A real recommender gets more interesting over time, and even a toy version of that loop — where clicking thumbs up bumps the genre and mood weights slightly toward that song's values — would start to capture the feedback cycle that makes production recommenders feel personal rather than mechanical.
