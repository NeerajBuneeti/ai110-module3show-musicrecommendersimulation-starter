# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

Three specific biases surfaced during testing. First, the valence feature carries a weight of 1.5 but is effectively wasted in every profile tested, because none of the user preference dicts include a `target_valence` key and the scorer silently defaults to 0.5. This gives an unearned advantage to any song whose valence happens to sit near the middle of the scale — Overdrive Protocol (valence 0.66) benefits from this every time it appears in results, regardless of what the user actually asked for. Second, the moods `confident`, `nostalgic`, and `romantic` exist as isolated nodes with zero adjacency connections in the mood neighborhood map, which means the songs carrying those moods — Block Party Anthem, Dust Road Memory, and Velvet Nights — score 0.0 on mood for every user who did not ask for them exactly; they can only surface by coincidence through energy and acousticness proximity, which has nothing to do with why a listener would want them. Third, Overdrive Protocol acts as a free rider throughout the catalog: its energy of 0.95 sits at the ceiling, its acousticness of 0.04 sits at the produced-sound floor, and its valence of 0.66 is close enough to the default 0.5 to collect partial valence credit — this combination lets it accumulate enough continuous-feature points to appear in the top five for profiles that asked for reggae, classical, or soul, none of which have any genre or mood connection to electronic music. Together these three biases mean the system silently rewards songs that happen to fit the scoring machinery's blind spots rather than the user's actual taste.

---

## 7. Evaluation

Seven profiles were tested in total: four standard listeners (Gym Warrior: metal/angry/0.95 energy, Late-Night Study Session: lofi/chill/0.38, Late-Night Driver: synthwave/moody/0.75, Soul & Warmth Seeker: soul/uplifting/0.62) and three adversarial cases designed to stress-test the scoring (Catalog Cliff: hip-hop/confident with no neighborhood connections; Mood Override: reggae/energetic where the only reggae song has an opposing mood; Knife Edge: classical/energetic where contradictory preferences nearly cancel). The standard profiles all produced sensible rank-1 results with scores above 88%, confirming that the scorer works when genre and mood signals are strong. The adversarial profiles revealed real failures: Mood Override caused the system to recommend an electronic track to a reggae fan at rank 1 (66.6%) while the only reggae song placed second (56.7%), and Knife Edge produced a 0.3-percentage-point margin where an electronic track edged out the only classical song despite scoring zero on genre. A weight experiment was also run: genre weight was halved from 3.0 to 1.5, energy weight was doubled from 2.0 to 4.0, and the normalizer was updated to 11.0. No rank-1 result changed for any of the seven profiles, but the adversarial failures worsened — the Mood Override winner's score rose from 66.6% to 78.2% and the Knife Edge margin widened from 0.3 points to roughly 12 points. The most surprising finding was that the adversarial failures are not caused by bad weight calibration: they stem from catalog sparsity and isolated mood nodes, and no weight adjustment fixes them without also degrading the standard profiles.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
