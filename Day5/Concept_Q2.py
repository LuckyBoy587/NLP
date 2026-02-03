import os
import sys
import warnings

# Suppress warnings and TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.simplefilter(action='ignore')

import spacy
from nltk.stem import SnowballStemmer

def solve():
    # Input file name
    try:
        filename = input("Enter text file name for full text processing: ")
        filepath = os.path.join(sys.path[0], filename)
        
        if not os.path.exists(filepath):
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
    except EOFError:
        return

    # Original Text Sample
    print("Original Text Sample:")
    print(content[:300])
    print()

    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("SpaCy model 'en_core_web_sm' not found. Install it using:")
        print("python -m spacy download en_core_web_sm")
        sys.exit(1)

    # 1. Lemmatization: Individual Words
    sample_words_str = "friendship studied was am is organizing matches"
    sample_words = sample_words_str.split()
    
    print("=== Lemmatization: Individual Words ===")
    doc_sample = nlp(sample_words_str)
    # Using doc_sample tokens might include punctuation or split differently if not careful.
    # The requirement says "Process a sample set of words ... using spaCy".
    # Sample output shows:
    # friendship -> friendship
    # studied -> study
    # was -> be
    # am -> be
    # is -> be
    # organizing -> organize
    # matches -> match
    for word in sample_words:
        token = nlp(word)[0]
        print(f"{word} -> {token.lemma_}")
    print()

    # 2. Stemming: Individual Words
    stemmer = SnowballStemmer(language='english')
    print("=== Stemming: Individual Words ===")
    for word in sample_words:
        stem = stemmer.stem(word)
        print(f"{word} --> {stem}")
    print()

    # 3. Lemmatization: Full Text
    doc_full = nlp(content)
    tokens_full = [token for token in doc_full if not token.is_space]
    
    print("=== Lemmatization: Full Text ===")
    for token in tokens_full[:50]:
        print(f"{token.text} --> {token.lemma_}")
    print()

    # 4. Stemming: Full Text
    print("=== Stemming: Full Text ===")
    for token in tokens_full[:50]:
        stem = stemmer.stem(token.text.lower())
        print(f"{token.text} --> {stem}")
    print()

    # 5. Practice Comparison Table
    practice_words_str = "running good universities flies fairer is"
    practice_words = practice_words_str.split()
    
    print("=== Practice 6.2: Lemmatization vs Stemming ===")
    print("Word\t\tLemma\t\tStem")
    print("-" * 42)
    for word in practice_words:
        lemma = nlp(word)[0].lemma_
        stem = stemmer.stem(word)
        print(f"{word}\t\t{lemma}\t\t{stem}")
    print()

    # 6. Conclusion
    print("Conclusion:")
    print("Lemmatization produces dictionary-based meaningful root words, while stemming may distort words by chopping suffixes. For NLP tasks like search, topic modeling, and information retrieval, lemmatization gives better and cleaner output.")

if __name__ == "__main__":
    solve()
