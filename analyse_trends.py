import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import glob
import spacy

nlp = spacy.load("en_core_web_sm")

# Helper function to process text again
def preprocess(text):
    doc = nlp(text.lower())
    return [t.lemma_ for t in doc if t.is_alpha and not t.is_stop]

def load_and_process(path_pattern):
    tokens = []
    for fname in glob.glob(path_pattern):
        with open(fname, encoding="utf-8") as f:
            tokens += preprocess(f.read())
    return Counter(tokens)

# Lexicons
medical_terms = ["disorder","diagnosis","symptom","treatment","therapy","medication","clinical","patient"]
human_terms   = ["sadness","grief","stress","loneliness","coping","support","friend","community","love",""]

# Load and count per decade
decades = ["1990s","2000s","2010s","2020s"]
med_freqs, hum_freqs = [], []


for decade in decades:
    counts = load_and_process(f"data/{decade}/*.txt")
    total = sum(counts.values())
    med_count = sum(counts[w] for w in medical_terms)
    hum_count = sum(counts[w] for w in human_terms)
    med_freqs.append(med_count/total)
    hum_freqs.append(hum_count/total)

# Plot
plt.plot(decades, med_freqs, label="Medicalised")
plt.plot(decades, hum_freqs, label="Human/Emotional")
plt.xlabel("Decade")
plt.ylabel("Relative Frequency")
plt.title("Language of Mental Health in the Media Over Time")
plt.legend()
plt.show()
