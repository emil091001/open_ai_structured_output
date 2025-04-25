
import json
from parser.lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.tokens = []
        self.prev_logprobs = []
        
        
    def parse(self, sequences, logprobs):
        for sequence, logprob in zip(sequences, logprobs):
            self.tokens.extend(self.lexer.add(sequence, logprob))
        
        self.tokens = self.tokens[::-1]    

        return self.value()
    
    
    def value(self):
        while self.peak() is None:
            token_type, token_value, logprob = self.tokens.pop()
            self.prev_logprobs.append(logprob)
            
        if self.peak() in ['STRING', 'NULL', 'TRUE', 'FALSE']:
            token_type, token_value, logprob = self.tokens.pop()
            self.prev_logprobs.append(logprob)
            return self.avg_logprob()
        
        if self.peak() in ['DIGIT', 'DASH']:
            return self.number()
        
        if self.peak() == 'LBRACE':
            self.expect('LBRACE')
            obj = self.properties()
            self.expect('RBRACE')
            return obj
        
        if self.peak() == 'LBRACKET':
            self.expect('LBRACKET')
            arr = self.elements()
            self.expect('RBRACKET')
            return arr
        
        raise ValueError(f"Unexpected token for value: {token_type}: {token_value}")
            
        
    def number(self):
        while self.peak() in ['DIGIT', 'DASH', 'DOT']:
            _, _, logprob = self.tokens.pop()
            self.prev_logprobs.append(logprob)
        
        return self.avg_logprob()
    
    def properties(self):
        if self.peak() == 'RBRACE':
            return {}

        obj = self.first_property()
        
        while self.peak() != 'RBRACE':
            obj.update(self.next_property())
            self.remove_nones()
    
        return obj
    
    
    def first_property(self):
        _, key, _ = self.expect('STRING')
        self.expect('COLON')
        value = self.value()
        
        return {key.replace('"', ''): value}
    
    
    def next_property(self):
        self.expect('COMMA')
        _, key, _ = self.expect('STRING')
        self.expect('COLON')
        value = self.value()
        self.remove_nones()
        
        return {key.replace('"', ''): value}
    
    
    def elements(self):
        if self.peak() == 'RBRACKET':
            return []

        arr = [self.first_element()]
        
        while self.peak() != 'RBRACKET':
            arr.append(self.next_element())
            self.remove_nones()
    
        return arr
    
    
    def first_element(self):
        value = self.value()
        
        return value
    
    
    def next_element(self):
        self.expect('COMMA')
        value = self.value()
        
        return value
        
        
    def avg_logprob(self):
        avg = sum(self.prev_logprobs) / len(self.prev_logprobs)
        self.prev_logprobs = []
        return avg
    
    
    def peak(self):
        return self.tokens[-1][0]


    def remove_nones(self):
        while self.peak() is None:
            _, _, logprob = self.tokens.pop()


    def expect(self, token_type):
        self.remove_nones()
        if self.peak() != token_type:
            raise ValueError(f"Expected {token_type}, got {self.tokens[-1][0]}: {self.tokens[-1][1]}")
        return self.tokens.pop()




# test_json = '{"key": 3.2, "key2": [1, 2, 3], "key3": {"key4": "value4"}}'

# sequences = [test_json[i:i+4] for i in range(0, len(test_json), 4)]
# logprobs = [i for i, _ in enumerate(range(len(sequences)))]

# logprob_data = json.loads(open("/Users/emilschneiderlorentzen/UNI/6sm/project/open_ai_structured_output/data/logprobs/test_real.json", "r").read())

# parser = Parser(Lexer())

# dud = parser.parse(logprob_data)

# print(json.dumps(dud, indent=4))
        

        