
import re


class Lexer:
    TOKENS = {
        'NULL': r'null',
        'TRUE': r'true',
        'FALSE': r'false',
        'DIGIT': r'[0-9]+',
        'DASH': r'\-',
        'STRING': r'"([^"\\]|\\.)*"',
        'LBRACE': r'\{',
        'RBRACE': r'\}',
        'LBRACKET': r'\[',
        'RBRACKET': r'\]',
        'COLON': r':',
        'COMMA': r',',
        'DOT': r'\.',
    }
    
    def __init__(self):
        self.draft = ""
        
        
    def add(self, sequence: str, logprob: float):
        self.draft += sequence
        self.draft = re.sub(r'^\s+', '', self.draft)
        tokens = []
        
        match = True
        while self.draft and match:
            match = False
            self.draft = re.sub(r'^\s+', '', self.draft)
            
            for token_type, pattern in self.TOKENS.items():
                regex = re.compile(pattern)
                match = regex.match(self.draft)
                if match:
                    token_value = match.group(0)
                    tokens.append((token_type, token_value, logprob))
                    self.draft = self.draft[len(token_value):]
                    match = True
                    break
                
            if not match:
                tokens.append((None, self.draft, logprob))
            
        return tokens
                
                


# #test_json = '{"key": -3.2, "key2": [1, 2, 3], "key3": {"key4": "value4"}}'
# test_json = '{"key": 3.2, "key2": [1, 2, 3], "key3": {"key4": "value4"}}'

# sequences = [test_json[i:i+4] for i in range(0, len(test_json), 4)]
# logprobs = [i for i, _ in enumerate(range(len(sequences)))]

# lexer = Lexer()

# for seq, prob in zip(sequences, logprobs):
#     tokens = lexer.add(seq, prob)
#     print(tokens)
#     print("===")