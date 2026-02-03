import os
import sys
import warnings

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
# Suppress spaCy warnings
warnings.simplefilter(action='ignore')

import spacy

def solve():
    try:
        filename = input().strip()
        filepath = os.path.join(sys.path[0], filename)
        
        if not os.path.exists(filepath):
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
            
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model 'en_core_web_sm' not found.")
            print("Run: python -m spacy download en_core_web_sm")
            sys.exit(1)
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. First 10 lines
        lines = content.splitlines()
        print("First 10 lines from the file:")
        for line in lines[:10]:
            print(line)
        print()
        
        # 2. First 20 tokens
        doc = nlp(content)
        tokens = [token.text for token in doc[:20]]
        print("First 20 tokens:")
        print(tokens)
        print()
        
        # 3. POS Tagging Output
        print("POS Tagging Output:")
        print("Word\tPOS\tTag")
        print("-" * 30)
        for token in doc:
            print(f"{token.text} \t {token.pos_} \t {token.tag_}")
            
    except EOFError:
        pass

if __name__ == "__main__":
    solve()
