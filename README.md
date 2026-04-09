# Mental Health Language Analysis
Analysing how mental health coverage in The Guardian evolved from clinical to humanized language (1998-2025).

## What it does
   - Scrapes articles via Guardian API
   - Analyses language using spaCy NLP
   - Categorises medical vs. human-centered terminology
   - Visualises trends over time
   
## Key findings
   - Over time, I observed that the relative frequency of human/emotional language has decreased since 2000, although there was a new peak at 2022. 
   - I had originally aimed to cover more years but there is a lack of data from the years before the internet 'boom'.
   - 
## Tech stack
   Python, spaCy, matplotlib, Guardian API
   
## Setup
1. Install dependencies:
   pip install -r requirements.txt
2. Download the language model:
   python -m spacy download en_core_web_sm
