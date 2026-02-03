import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import sys
import warnings
warnings.simplefilter(action='ignore')
import spacy
from nltk.stem import SnowballStemmer

def main():
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("SpaCy model 'en_core_web_sm' not found. Install it using:")
        print("python -m spacy download en_core_web_sm")
        sys.exit(1)

    stemmer = SnowballStemmer(language='english')

    try:
        filename = input("Enter text file name: ")
        print()
    except EOFError:
        return

    file_path = os.path.join(sys.path[0], filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    print("Original Text Sample:")
    print(content[:300])
    print()

    doc = nlp(content)
    tokens = [token for token in doc if not token.is_space]
    print(f"Total Tokens Count: {len(tokens)}")
    print()

    lemmas = [token.lemma_ for token in tokens]
    print("=== Lemmatized Sample (First 20 tokens) ===")
    print(lemmas[:20])
    print()

    print("Word --> Lemma")
    for token, lemma in zip(tokens[:30], lemmas[:30]):
        print(f"{token.text} --> {lemma}")
    print()

    stems = [stemmer.stem(token.text.lower()) for token in tokens]
    print("=== Stemmed Sample (First 20 tokens) ===")
    print(stems[:20])
    print()

    print("Word --> Stem")
    for token, stem in zip(tokens[:30], stems[:30]):
        print(f"{token.text} --> {stem}")
    print()

    print("=== Comparison: Lemmatization vs Stemming ===")
    print("Word\t\tLemma\t\tStem")
    print("-" * 42)
    for token, lemma, stem in zip(tokens[:30], lemmas[:30], stems[:30]):
        print(f"{token.text}\t\t{lemma}\t\t{stem}")
    print()

    print("Conclusion:")
    print("Lemmatization produces dictionary-based meaningful root words, while stemming may distort words by chopping suffixes. For NLP tasks like search, topic modeling, and information retrieval, lemmatization gives better and cleaner output.")

if __name__ == "__main__":
    main()
