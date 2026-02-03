import os
import sys
import warnings

# Suppress warnings and TensorFlow logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.simplefilter(action='ignore')

import spacy

def solve():
    # Prompt for filename
    try:
        filename = input("Enter text file name: ")
    except EOFError:
        return
        
    # The expected output shows a newline after the prompt
    print()
    
    filepath = os.path.join(sys.path[0], filename)
    
    if not os.path.exists(filepath):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Original Text Sample (First 300 characters)
    print("=== Original Text Sample (First 300 chars) ===")
    print(content[:300])
    print()
    
    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        print("SpaCy model 'en_core_web_sm' not found. Install it using:")
        print("python -m spacy download en_core_web_sm")
        sys.exit(1)
    
    # Process text with default stop words
    doc = nlp(content)
    # Using lowercase check against nlp.Defaults.stop_words for consistency
    tokens_no_stop = [token.text for token in doc if token.text.lower() not in nlp.Defaults.stop_words and not token.is_space]
    
    # 2. Text After Stop Word Removal (Sample) - First 50 valid tokens
    print("=== Text After Stop Word Removal (Sample) ===")
    print(" ".join(tokens_no_stop[:50]))
    print()
    
    # 3. Custom stop words modification
    print("Custom stop words added: {'set', 'example', 'whenever', 'whatever'}")
    
    custom_words = {'set', 'example', 'whenever', 'whatever'}
    for word in custom_words:
        nlp.vocab[word].is_stop = True
        nlp.Defaults.stop_words.add(word)
    
    print(f"Is 'example' a stop word? {nlp.vocab['example'].is_stop}")
    # Display the count after addition
    print(f"Total Stop Words Now: {len(nlp.Defaults.stop_words)}")
    print()
    
    # Remove 'example'
    nlp.vocab['example'].is_stop = False
    if 'example' in nlp.Defaults.stop_words:
        nlp.Defaults.stop_words.remove('example')
    
    print("Removed stop word: {'example'}")
    print(f"Is 'example' a stop word now? {nlp.vocab['example'].is_stop}")
    # Display the count after removal
    print(f"Total Stop Words After Removal: {len(nlp.Defaults.stop_words)}")
    print()
    
    # 4. Stop Word Removal Examples
    print("=== Stop Word Removal Examples ===")
    print()
    
    examples = [
        "The quick brown fox jumps over the lazy dog.",
        "I am learning Natural Language Processing with Python.",
        "What is the best way to learn natural language processing?"
    ]
    
    for i, ex in enumerate(examples, 1):
        print(f"Input {i}: {ex}")
        doc_ex = nlp(ex)
        # Using updated stop words
        filtered = [token.text for token in doc_ex if token.text.lower() not in nlp.Defaults.stop_words and not token.is_space]
        print(f"After Stop Word Removal: {' '.join(filtered)}")
        # No trailing blank line after the last example
        if i < len(examples):
            print()

if __name__ == "__main__":
    solve()