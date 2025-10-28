import sys
from BST import BST  
from search_engine import search_loop 

if __name__ == "__main__":
    WORDLIST_URL = "https://raw.githubusercontent.com/davidxbors/romanian_wordlists/refs/heads/master/wordlists/ro_50k.txt"
    
    try:
        print(f"Loading dictionary...")
        dictionary_bst = BST(WORDLIST_URL, url=True)
        search_loop(dictionary_bst)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}", file=sys.stderr)
        sys.exit(1)