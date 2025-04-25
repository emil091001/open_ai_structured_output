
import json
import math
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from metrics2 import Metric
from parser.lexer import Lexer
from parser.parser import Parser
from structure import Structure
from transformers import GPT2TokenizerFast
from tqdm import tqdm

class ConfidenceFilter:
    tables = [
        'environmental_impact',
        'additional_environmental_impact',
        'resource_use',
        'end_of_life_waste',
        'end_of_life_flow']
    
    def __init__(self, parser: Parser, threshold: float = 0):
        self.log_threshold = math.log(threshold) if threshold > 0 else -math.inf
        self.parser = parser
  
    def __call__(self, logprobs_dict: dict) -> list:
        """Filter the data based on the confidence threshold."""
        sequences, logprobs = self.preprocess(logprobs_dict)
        
        raw_output = json.loads("".join(sequences))
        prob_output = self.parser.parse(sequences, logprobs)
        
        filtered_output = self.prune(raw_output, prob_output)
        
        return filtered_output
    
    def prune(self, raw_output, prob_output) -> dict:
        """Prune the output based on the confidence threshold."""
        for table in self.tables:
            for parameter, prob_parameter in zip(raw_output[table], prob_output[table]):
                new_values = []
                for value, prob_value in zip(parameter['values'], prob_parameter['values']):
                    logprob = (prob_value['value'] + prob_value['module'] + prob_value['scenario']) / 3
                    if logprob >= self.log_threshold:
                        new_values.append(value)
                        
                parameter['values'] = new_values
        
        return raw_output
    
    @staticmethod
    def preprocess(logprobs_data: dict):
        logprobs = []
        sequences = []
        for entry in logprobs_data['content']:
            logprobs.append(entry['logprob'])
            sequences.append(entry['token'])
            
        return sequences, logprobs
    

lexer = Lexer()
parser = Parser(lexer)

threshold = 0
confidence_filter = ConfidenceFilter(parser, threshold=threshold)

for file_name in tqdm(os.listdir('data/output')):
    if not file_name.endswith('.json'):
        continue
    
    with open(os.path.join('data/output', file_name), 'r') as f:
        logprobs_data = json.load(f)
        
    filtered_output = confidence_filter(logprobs_data)
    
    output_path = os.path.join('data/filtered_output', str(threshold))
    os.makedirs(output_path, exist_ok=True)
    
    with open(os.path.join(output_path, file_name), 'w') as f:
        json.dump(filtered_output, f, indent=4)
        