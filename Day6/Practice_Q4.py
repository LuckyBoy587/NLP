import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import sys
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

def solve():
    try:
        filename = input("Enter text file name: ")
    except EOFError:
        return

    file_path = os.path.join(sys.path[0], filename)
    
    if not os.path.exists(file_path):
        print("Error: File not found")
        sys.exit(1)
        
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception:
        print("Error: File not found")
        sys.exit(1)

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content)

    stop_words = set(STOP_WORDS)
    stop_words.update(["officially", "announced", "present", "run"])
    stop_words.difference_update(["hence", "every", "he"])

    filtered_tokens = []
    for token in doc:
        if (token.text.lower() not in stop_words and 
            not token.is_punct and 
            not token.is_space):
            filtered_tokens.append(token.lemma_.lower())

    print("Filtered Tokens (First 20):")
    print(filtered_tokens[:20])
    print()

    cleaned_text = " ".join(filtered_tokens)
    print("Cleaned Text Sample:")
    print(cleaned_text[:200])

if __name__ == "__main__":
    solve()
