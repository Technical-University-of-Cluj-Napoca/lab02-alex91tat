import urllib.request

class Node:
    def __init__(self, word: str):
        self.word = word
        self.left = None
        self.right = None

class BST:
    def __init__(self, source: str, **kwargs):
        self.results = []
        file = kwargs.get("file", False)
        url = kwargs.get("url", False)

        if file and url:
            raise ValueError("file and url can't be both true!")
        
        words = []
        if url:
            words = self._read_from_url(source)
        elif file:
            words = self._read_from_file(source)

        self.root = self._build_from_sorted_list(words)

    def _build_from_sorted_list(self, sorted_words: list[str]) -> Node | None:
        if not sorted_words:
            return None
        
        mid_index = len(sorted_words) // 2
        root_node = Node(sorted_words[mid_index])
        
        root_node.left = self._build_from_sorted_list(sorted_words[:mid_index])
        root_node.right = self._build_from_sorted_list(sorted_words[mid_index + 1:])
        
        return root_node

    def _read_from_url(self, url: str) -> list[str]:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode("utf-8")
        words = [word.strip().lower() for word in content.split() if word.strip()]
        return words

    def _read_from_file(self, path: str) -> list[str]:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        words = [word.strip().lower() for word in content.split() if word.strip()]
        return words
    
    def autocomplete(self, prefix: str) -> list[str]:
        self.results = []         
        if not prefix:
            return self.results 
        
        self._collect(self.root, prefix.lower())
        
        return self.results

    def _collect(self, node: Node, prefix: str):
        """
        A correct iterative (non-recursive) in-order traversal
        with pruning.
        """
        stack = []
        current = node

        while stack or current:
            if current:       
                if prefix < current.word or current.word.startswith(prefix):
                    stack.append(current)
                    current = current.left
                elif prefix > current.word:
                    current = current.right
                else:
                    current = None
            else:
                if not stack:
                    break 
                
                popped_node = stack.pop()
                
                if popped_node.word.startswith(prefix):
                    self.results.append(popped_node.word)
                    
                if prefix > popped_node.word or popped_node.word.startswith(prefix):
                    current = popped_node.right
                else:
                    current = None